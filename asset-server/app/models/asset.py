from datetime import date
from decimal import Decimal

from sqlalchemy import Column, Date, DateTime, Float, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class Asset(Base, TimestampMixin):
    __tablename__ = "assets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="主键")
    asset_code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="资产编号")
    company_code: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="公司编号")
    sn: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="SN号")
    name: Mapped[str] = mapped_column(String(200), nullable=False, comment="资产名称")
    category_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="分类ID")
    department: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="所属部门")
    user_id: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="使用人")
    location: Mapped[str | None] = mapped_column(String(200), nullable=True, comment="存放位置")
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="normal", comment="状态: normal/borrowed/scrapped")
    price: Mapped[Decimal | None] = mapped_column(Float, nullable=True, comment="购买价格")
    purchase_date: Mapped[date | None] = mapped_column(Date, nullable=True, comment="购买日期")
    description: Mapped[str | None] = mapped_column(Text, nullable=True, comment="描述")
    images: Mapped[list | None] = mapped_column(JSON, nullable=True, comment="图片列表")
    qr_code_url: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="二维码图片地址")
    inventory_status: Mapped[str] = mapped_column(String(20), nullable=False, default="未盘点", comment="盘点状态: 未盘点/已盘点/异常")
    inventory_image: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="盘点照片URL")