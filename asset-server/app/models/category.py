from sqlalchemy import Column, Integer, String, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class Category(Base, TimestampMixin):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="主键")
    name: Mapped[str] = mapped_column(String(100), nullable=False, comment="分类名称")
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="分类编码")
    parent_id: Mapped[int] = mapped_column(Integer, default=0, comment="父分类ID")
    sort_order: Mapped[int] = mapped_column(Integer, default=0, comment="排序")
    status: Mapped[int] = mapped_column(SmallInteger, default=1, comment="状态")