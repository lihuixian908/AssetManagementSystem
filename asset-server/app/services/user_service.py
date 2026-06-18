from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserCreate, UserUpdate, UserInDB


user_repo = UserRepository()


def authenticate_user(db: Session, username: str, password: str) -> User | None:
    user = user_repo.get_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


def login(db: Session, username: str, password: str) -> dict:
    user = authenticate_user(db, username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
        )
    if user.status == 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="账号已被禁用",
        )
    access_token = create_access_token(subject=user.id, extra={"role": user.role})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserInDB.model_validate(user),
    }


def get_current_user(db: Session, user_id: int) -> User:
    user = user_repo.get(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在",
        )
    return user


def create_user(db: Session, user_in: UserCreate) -> UserInDB:
    existing = user_repo.get_by_username(db, user_in.username)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在",
        )
    user_data = user_in.model_dump()
    user_data["password"] = hash_password(user_data["password"])
    user = user_repo.create(db, obj_in=UserCreate(**user_data))
    return UserInDB.model_validate(user)


def update_user(db: Session, user_id: int, user_in: UserUpdate) -> UserInDB:
    user = user_repo.get(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在",
        )
    user = user_repo.update(db, db_obj=user, obj_in=user_in)
    return UserInDB.model_validate(user)


def delete_user(db: Session, user_id: int) -> bool:
    return user_repo.delete(db, id=user_id)


def reset_password(db: Session, user_id: int, new_password: str) -> None:
    user = user_repo.get(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在",
        )
    user.password = hash_password(new_password)
    db.add(user)
    db.commit()


def get_user_list(
    db: Session,
    page: int = 1,
    page_size: int = 10,
    keyword: str | None = None,
) -> dict:
    skip = (page - 1) * page_size
    filters = {}
    if keyword:
        from app.models.user import User
        from sqlalchemy import or_, select
        query = select(User).where(
            or_(
                User.username.contains(keyword),
                User.real_name.contains(keyword),
            )
        )
        count_query = select(
            __import__('sqlalchemy', fromlist=['func']).func.count(User.id)
        ).where(
            or_(
                User.username.contains(keyword),
                User.real_name.contains(keyword),
            )
        )
        total = db.execute(count_query).scalar_one()
        query = query.offset(skip).limit(page_size)
        users = list(db.execute(query).scalars().all())
    else:
        users = user_repo.get_multi(db, skip=skip, limit=page_size)
        total = user_repo.count(db)
    
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": [UserInDB.model_validate(u).model_dump() for u in users],
    }