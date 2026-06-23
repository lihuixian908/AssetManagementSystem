from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import SessionDep, get_current_active_user
from app.models.asset import Asset
from app.models.asset_borrow_record import AssetBorrowRecord
from app.models.user import User
from app.schemas.borrow import BorrowCreate
from app.schemas.common import Response

router = APIRouter(prefix="/borrow", tags=["设备出借"])


@router.post("", response_model=Response)
def create_borrow(
    borrow_in: BorrowCreate,
    db: SessionDep,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    asset = db.get(Asset, borrow_in.asset_id)
    if not asset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="设备不存在")
    if asset.status != "normal":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="仅可在库设备出借")

    record = AssetBorrowRecord(
        asset_id=borrow_in.asset_id,
        borrower=borrow_in.borrower,
        department=borrow_in.department,
        borrow_date=borrow_in.borrow_date or date.today(),
        expected_return_date=borrow_in.expected_return_date,
        status="pending",
        location=borrow_in.location,
        photo_url=borrow_in.photo_url,
        remark=borrow_in.remark,
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return Response(data={"id": record.id, "status": "pending"}, message="申请已提交，等待审批")


@router.get("/pending", response_model=Response)
def get_pending(db: SessionDep):
    from sqlalchemy import select
    query = select(AssetBorrowRecord, Asset.name, Asset.asset_code).join(Asset, AssetBorrowRecord.asset_id == Asset.id).where(AssetBorrowRecord.status == "pending").order_by(AssetBorrowRecord.created_at.desc())
    rows = db.execute(query).all()
    return Response(data=[{"id": r[0].id, "asset_id": r[0].asset_id, "asset_name": r[1], "asset_code": r[2], "borrower": r[0].borrower, "department": r[0].department, "location": r[0].location, "remark": r[0].remark, "created_at": str(r[0].created_at)} for r in rows])


@router.post("/{record_id}/approve", response_model=Response)
def approve_borrow(record_id: int, db: SessionDep, current_user: Annotated[User, Depends(get_current_active_user)]):
    if current_user.role not in ("admin", "asset_admin"): raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足")
    record = db.get(AssetBorrowRecord, record_id)
    if not record or record.status != "pending": raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="申请不存在或已处理")
    asset = db.get(Asset, record.asset_id)
    if not asset or asset.status != "normal": raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="设备已被借出")
    record.status = "borrowed"; asset.status = "borrowed"
    db.add(record); db.add(asset); db.commit()
    return Response(message="审批通过")


@router.post("/{record_id}/reject", response_model=Response)
def reject_borrow(record_id: int, db: SessionDep, current_user: Annotated[User, Depends(get_current_active_user)]):
    if current_user.role not in ("admin", "asset_admin"): raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足")
    record = db.get(AssetBorrowRecord, record_id)
    if not record or record.status != "pending": raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="申请不存在或已处理")
    record.status = "rejected"; db.add(record); db.commit()
    return Response(message="已拒绝")


@router.post("/return", response_model=Response)
def return_borrow(
    asset_id: int,
    return_photo_url: str | None = None,
    db: SessionDep = None,
    current_user: Annotated[User, Depends(get_current_active_user)] = None,
):
    asset = db.get(Asset, asset_id)
    if not asset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="设备不存在")
    if asset.status != "borrowed":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="该设备未处于出借状态")

    from sqlalchemy import select

    query = select(AssetBorrowRecord).where(
        AssetBorrowRecord.asset_id == asset_id,
        AssetBorrowRecord.status == "borrowed",
    ).order_by(AssetBorrowRecord.created_at.desc()).limit(1)
    record = db.execute(query).scalar_one_or_none()

    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="未找到出借记录")

    # 普通用户只能归还自己借出的设备，管理员可直接归还
    is_admin = current_user.role in ("admin", "asset_admin")
    if not is_admin and record.borrower != current_user.real_name:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="只能归还自己借出的设备")

    record.actual_return_date = date.today()
    record.status = "returned"
    if return_photo_url:
        record.return_photo_url = return_photo_url
    asset.status = "normal"
    db.add(record)
    db.add(asset)
    db.commit()

    return Response(data={"status": "normal"}, message="归还成功")


@router.delete("/{record_id}", response_model=Response)
def cancel_borrow(
    record_id: int,
    db: SessionDep,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    record = db.get(AssetBorrowRecord, record_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="出借记录不存在")
    if record.status != "borrowed":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="该记录已归还，无法取消")

    asset = db.get(Asset, record.asset_id)
    if asset:
        asset.status = "normal"
        db.add(asset)
    db.delete(record)
    db.commit()
    return Response(message="出借已取消")


@router.get("/history/{asset_id}", response_model=Response)
def get_borrow_history(asset_id: int, db: SessionDep):
    from sqlalchemy import select

    query = (
        select(AssetBorrowRecord)
        .where(AssetBorrowRecord.asset_id == asset_id)
        .order_by(AssetBorrowRecord.created_at.desc())
    )
    records = list(db.execute(query).scalars().all())

    return Response(data=[
        {
            "id": r.id,
            "asset_id": r.asset_id,
            "borrower": r.borrower,
            "department": r.department,
            "borrow_date": str(r.borrow_date) if r.borrow_date else None,
            "expected_return_date": str(r.expected_return_date) if r.expected_return_date else None,
            "actual_return_date": str(r.actual_return_date) if r.actual_return_date else None,
            "location": r.location,
            "photo_url": r.photo_url,
            "return_photo_url": r.return_photo_url,
            "status": r.status,
            "remark": r.remark,
            "created_at": str(r.created_at),
        }
        for r in records
    ])
