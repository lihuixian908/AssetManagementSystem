from fastapi import APIRouter, Query
from sqlalchemy.orm import Session

from app.api.deps import SessionDep
from app.schemas.common import Response

router = APIRouter(prefix="/reports", tags=["报表"])


@router.get("/asset-stats", response_model=Response)
def get_asset_stats(db: SessionDep):
    from app.models.asset import Asset
    from sqlalchemy import select, func
    
    total_query = select(func.count(Asset.id))
    total = db.execute(total_query).scalar_one() or 0

    normal_query = select(func.count(Asset.id)).where(Asset.status == "normal")
    normal = db.execute(normal_query).scalar_one() or 0

    borrowed_query = select(func.count(Asset.id)).where(Asset.status == "borrowed")
    borrowed = db.execute(borrowed_query).scalar_one() or 0

    scrapped_query = select(func.count(Asset.id)).where(Asset.status == "scrapped")
    scrapped = db.execute(scrapped_query).scalar_one() or 0

    return Response(data={
        "total": total,
        "by_status": {
            "normal": normal,
            "borrowed": borrowed,
            "scrapped": scrapped,
        },
    })


@router.get("/recent-activities", response_model=Response)
def get_recent_activities(db: SessionDep, limit: int = Query(10, ge=1, le=50)):
    from app.models.asset import Asset
    from app.models.record import AssetRecord
    from sqlalchemy import select

    activities = []

    # 操作记录
    try:
        query = (
            select(
                AssetRecord.created_at.label("time"),
                AssetRecord.type.label("type"),
                AssetRecord.description.label("description"),
                AssetRecord.operator.label("operator"),
                Asset.name.label("asset_name"),
            )
            .join(Asset, AssetRecord.asset_id == Asset.id, isouter=True)
            .order_by(AssetRecord.created_at.desc())
            .limit(limit)
        )
        for row in db.execute(query).all():
            type_map = {
                "create": "设备入库", "assign": "资产领用", "return": "资产归还",
                "transfer": "资产调拨", "maintenance": "设备维修", "scrap": "设备报废",
                "update": "设备更新", "scan": "扫码查看", "borrow": "设备出借",
            }
            activities.append({
                "time": str(row.time),
                "title": type_map.get(row.type, row.type),
                "description": row.description or "",
                "asset_name": row.asset_name or "",
                "operator": row.operator,
            })
    except Exception:
        pass

    # 变动记录
    try:
        from app.models.asset_change_record import AssetChangeRecord
        from app.models.user import User as UserModel
        change_label = {"owner": "负责人变更", "dept": "部门变更", "location": "位置变更", "category": "分类变更"}

        # 收集所有 owner 变更涉及的 user_id 以便批量查姓名
        owner_ids: set[int] = set()
        pre_query = (
            select(AssetChangeRecord.old_value, AssetChangeRecord.new_value)
            .where(AssetChangeRecord.change_type == "owner")
            .order_by(AssetChangeRecord.created_at.desc())
            .limit(limit)
        )
        for row in db.execute(pre_query).all():
            for val in (row[0], row[1]):
                if val and val.isdigit():
                    owner_ids.add(int(val))

        user_map: dict[int, str] = {}
        if owner_ids:
            user_query = select(UserModel.id, UserModel.real_name).where(UserModel.id.in_(list(owner_ids)))
            for row in db.execute(user_query).all():
                user_map[row[0]] = row[1]

        query = (
            select(
                AssetChangeRecord.created_at.label("time"),
                AssetChangeRecord.change_type.label("type"),
                AssetChangeRecord.old_value.label("old_val"),
                AssetChangeRecord.new_value.label("new_val"),
                AssetChangeRecord.operator.label("operator"),
                Asset.name.label("asset_name"),
            )
            .join(Asset, AssetChangeRecord.asset_id == Asset.id, isouter=True)
            .order_by(AssetChangeRecord.created_at.desc())
            .limit(limit)
        )

        def format_val(change_type: str, val: str | None) -> str:
            if not val:
                return "无"
            if change_type == "owner" and val.isdigit():
                return user_map.get(int(val), val)
            return val

        for row in db.execute(query).all():
            activities.append({
                "time": str(row.time),
                "title": change_label.get(row.type, row.type),
                "description": f"{format_val(row.type, row.old_val)} → {format_val(row.type, row.new_val)}",
                "asset_name": row.asset_name or "",
                "operator": row.operator,
            })
    except Exception:
        pass

    activities.sort(key=lambda x: x["time"], reverse=True)
    return Response(data=activities[:limit])


@router.get("/asset-trend", response_model=Response)
def get_asset_trend(
    db: SessionDep,
    days: int = Query(30, ge=1, le=365),
):
    from app.models.asset import Asset
    from app.models.record import AssetRecord
    from sqlalchemy import select, func
    from datetime import datetime, timedelta
    
    start_date = datetime.now() - timedelta(days=days)
    
    query = (
        select(AssetRecord.type, func.count(AssetRecord.id))
        .where(AssetRecord.created_at >= start_date)
        .group_by(AssetRecord.type)
    )
    result = db.execute(query).all()
    
    return Response(data={
        "period": f"最近{days}天",
        "records": {row[0]: row[1] for row in result},
    })


@router.get("/overdue", response_model=Response)
def get_overdue_borrows(db: SessionDep):
    from datetime import date
    from app.models.asset import Asset
    from app.models.asset_borrow_record import AssetBorrowRecord
    from sqlalchemy import select

    today = date.today()
    query = (
        select(AssetBorrowRecord, Asset.name, Asset.asset_code)
        .join(Asset, AssetBorrowRecord.asset_id == Asset.id)
        .where(
            AssetBorrowRecord.status == "borrowed",
            AssetBorrowRecord.expected_return_date.isnot(None),
            AssetBorrowRecord.expected_return_date < today,
        )
        .order_by(AssetBorrowRecord.borrow_date.asc())
    )
    rows = db.execute(query).all()
    return Response(data=[{
        "record_id": r[0].id,
        "asset_id": r[0].asset_id,
        "asset_name": r[1],
        "asset_code": r[2],
        "borrower": r[0].borrower,
        "borrow_date": str(r[0].borrow_date) if r[0].borrow_date else None,
        "expected_return_date": str(r[0].expected_return_date) if r[0].expected_return_date else None,
    } for r in rows])