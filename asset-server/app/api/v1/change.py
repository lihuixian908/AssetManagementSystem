from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import SessionDep, get_current_active_user
from app.models.asset import Asset
from app.models.asset_change_record import AssetChangeRecord
from app.models.user import User
from app.schemas.change import ChangeCreate
from app.schemas.common import Response

router = APIRouter(prefix="/change", tags=["设备变动"])

CHANGE_FIELD_MAP = {
    "owner": "user_id",
    "dept": "department",
    "location": "location",
    "category": "category_id",
}

CHANGE_TYPE_LABEL = {
    "owner": "负责人变更",
    "dept": "部门变更",
    "location": "位置变更",
    "category": "分类变更",
}


@router.post("", response_model=Response)
def create_change(
    change_in: ChangeCreate,
    db: SessionDep,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    asset = db.get(Asset, change_in.asset_id)
    if not asset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="设备不存在")

    if change_in.change_type not in CHANGE_FIELD_MAP:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"不支持的变动类型: {change_in.change_type}",
        )

    field_name = CHANGE_FIELD_MAP[change_in.change_type]
    old_value = str(getattr(asset, field_name, "") or "")

    # 更新资产字段
    if change_in.change_type == "category":
        setattr(asset, field_name, int(change_in.new_value))
    elif change_in.change_type == "owner":
        setattr(asset, field_name, int(change_in.new_value) if change_in.new_value.isdigit() else change_in.new_value)
    else:
        setattr(asset, field_name, change_in.new_value)

    record = AssetChangeRecord(
        asset_id=change_in.asset_id,
        change_type=change_in.change_type,
        old_value=old_value,
        new_value=change_in.new_value,
        operator=current_user.real_name,
        remark=change_in.remark,
    )
    db.add(record)
    db.add(asset)
    db.commit()
    db.refresh(record)

    return Response(
        data={"id": record.id, "change_type": CHANGE_TYPE_LABEL.get(change_in.change_type, change_in.change_type)},
        message="变动成功",
    )


@router.get("/history/{asset_id}", response_model=Response)
def get_change_history(asset_id: int, db: SessionDep):
    from sqlalchemy import select

    query = (
        select(AssetChangeRecord)
        .where(AssetChangeRecord.asset_id == asset_id)
        .order_by(AssetChangeRecord.created_at.desc())
    )
    records = list(db.execute(query).scalars().all())

    return Response(data=[
        {
            "id": r.id,
            "asset_id": r.asset_id,
            "change_type": r.change_type,
            "change_type_label": CHANGE_TYPE_LABEL.get(r.change_type, r.change_type),
            "old_value": r.old_value,
            "new_value": r.new_value,
            "operator": r.operator,
            "remark": r.remark,
            "created_at": str(r.created_at),
        }
        for r in records
    ])
