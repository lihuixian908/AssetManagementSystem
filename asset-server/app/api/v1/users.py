from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import SessionDep, require_admin
from app.models.user import User
from app.schemas.common import PaginationResponse, Response
from app.schemas.user import UserCreate, UserInDB, UserUpdate, ResetPasswordRequest
from app.services import user_service

router = APIRouter(prefix="/users", tags=["用户管理"])


@router.get("", response_model=Response)
def get_users(
    db: SessionDep,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    keyword: str | None = None,
):
    result = user_service.get_user_list(db, page, page_size, keyword)
    return Response(data=result)


@router.get("/{user_id}", response_model=Response)
def get_user(user_id: int, db: SessionDep):
    user = user_service.get_current_user(db, user_id)
    return Response(data=UserInDB.model_validate(user).model_dump())


@router.post("", response_model=Response)
def create_user(
    user_in: UserCreate,
    db: SessionDep,
    current_user: Annotated[User, Depends(require_admin)],
):
    result = user_service.create_user(db, user_in)
    return Response(data=result.model_dump())


@router.put("/{user_id}", response_model=Response)
def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: SessionDep,
    current_user: Annotated[User, Depends(require_admin)],
):
    result = user_service.update_user(db, user_id, user_in)
    return Response(data=result.model_dump())


def _check_last_admin(db: Session, user_ids: set[int]):
    from sqlalchemy import select, func
    from fastapi import HTTPException as HttpErr
    total_admins = db.execute(select(func.count(User.id)).where(User.role == "admin")).scalar_one() or 0
    deleting_admins = db.execute(select(func.count(User.id)).where(User.id.in_(user_ids), User.role == "admin")).scalar_one() or 0
    if deleting_admins > 0 and total_admins - deleting_admins < 1:
        raise HttpErr(status_code=400, detail="至少保留一名管理员")


@router.delete("/{user_id}", response_model=Response)
def delete_user(
    user_id: int,
    db: SessionDep,
    current_user: Annotated[User, Depends(require_admin)],
):
    _check_last_admin(db, {user_id})
    user_service.delete_user(db, user_id)
    return Response(message="删除成功")


@router.post("/batch-delete", response_model=Response)
def batch_delete_users(
    ids: list[int],
    db: SessionDep,
    current_user: Annotated[User, Depends(require_admin)],
):
    from sqlalchemy import select
    _check_last_admin(db, set(ids))
    users = db.execute(select(User).where(User.id.in_(ids))).scalars().all()
    for u in users:
        db.delete(u)
    db.commit()
    return Response(data={"deleted": len(users)}, message=f"已删除{len(users)}名用户")


@router.post("/{user_id}/reset-password", response_model=Response)
def reset_password(
    user_id: int,
    body: ResetPasswordRequest,
    db: SessionDep,
    current_user: Annotated[User, Depends(require_admin)],
):
    user_service.reset_password(db, user_id, body.new_password)
    return Response(message="密码重置成功")