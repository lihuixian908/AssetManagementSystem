from datetime import date, datetime

from sqlalchemy import Column, Date, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class AssetBorrowRecord(Base):
    __tablename__ = "asset_borrow_record"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="主键")
    asset_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="资产ID")
    borrower: Mapped[str] = mapped_column(String(50), nullable=False, comment="借用人")
    department: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="借用人部门")
    borrow_date: Mapped[date] = mapped_column(Date, nullable=False, comment="借出日期")
    expected_return_date: Mapped[date | None] = mapped_column(Date, nullable=True, comment="预计归还日期")
    actual_return_date: Mapped[date | None] = mapped_column(Date, nullable=True, comment="实际归还日期")
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="borrowed", comment="状态: borrowed/returned")
    location: Mapped[str | None] = mapped_column(String(200), nullable=True, comment="使用地点")
    photo_url: Mapped[str | None] = mapped_column(String(500), nullable=True, comment="出借照片")
    return_photo_url: Mapped[str | None] = mapped_column(String(500), nullable=True, comment="归还照片")
    remark: Mapped[str | None] = mapped_column(Text, nullable=True, comment="备注")
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now, comment="创建时间")
