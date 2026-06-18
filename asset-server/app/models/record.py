from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class AssetRecord(Base, TimestampMixin):
    __tablename__ = "asset_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="主键")
    asset_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="资产ID")
    user_id: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="操作人ID")
    type: Mapped[str] = mapped_column(String(20), nullable=False, comment="操作类型")
    description: Mapped[str | None] = mapped_column(Text, nullable=True, comment="操作描述")
    operator: Mapped[str] = mapped_column(String(50), nullable=False, comment="操作人")