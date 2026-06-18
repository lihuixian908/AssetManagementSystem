from sqlalchemy import Column, Integer, String, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="主键")
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="用户名")
    password: Mapped[str] = mapped_column(String(255), nullable=False, comment="密码(加密)")
    real_name: Mapped[str] = mapped_column(String(50), nullable=False, comment="真实姓名")
    department: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="所属部门")
    role: Mapped[str] = mapped_column(String(20), nullable=False, default="user", comment="角色(admin/user)")
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True, comment="手机号")
    email: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="邮箱")
    status: Mapped[int] = mapped_column(SmallInteger, default=1, comment="状态(0禁用/1启用)")