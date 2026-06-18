from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class AssetChangeRecord(Base):
    __tablename__ = "asset_change_record"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="主键")
    asset_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="资产ID")
    change_type: Mapped[str] = mapped_column(String(20), nullable=False, comment="变动类型: owner/dept/location/category")
    old_value: Mapped[str | None] = mapped_column(String(200), nullable=True, comment="旧值")
    new_value: Mapped[str] = mapped_column(String(200), nullable=False, comment="新值")
    operator: Mapped[str] = mapped_column(String(50), nullable=False, comment="操作人")
    remark: Mapped[str | None] = mapped_column(Text, nullable=True, comment="备注")
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now, comment="创建时间")
