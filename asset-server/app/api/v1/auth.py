from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import SessionDep, get_current_active_user
from app.core.security import create_access_token, verify_password, hash_password
from app.models.user import User
from app.schemas.common import Response
from app.schemas.token import Token
from app.schemas.user import UserInDB, UserLogin, ChangePassword
from app.services import user_service

router = APIRouter(prefix="/auth", tags=["认证"])


@router.post("/login", response_model=Response)
def login(user_in: UserLogin, db: SessionDep):
    result = user_service.login(db, user_in.username, user_in.password)
    return Response(data=result)


@router.post("/logout", response_model=Response)
def logout(current_user: Annotated[User, Depends(get_current_active_user)]):
    return Response(message="退出登录成功")


@router.get("/me", response_model=Response)
def get_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return Response(data=UserInDB.model_validate(current_user).model_dump())


@router.put("/password", response_model=Response)
def change_password(
    password_data: ChangePassword,
    db: SessionDep,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    if not verify_password(password_data.old_password, current_user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="旧密码错误",
        )
    current_user.password = hash_password(password_data.new_password)
    db.add(current_user)
    db.commit()
    return Response(message="密码修改成功")