from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel


class AssetBase(BaseModel):
    asset_code: str
    company_code: str | None = None
    sn: str | None = None
    name: str
    category_id: int
    department: str | None = None
    user_id: int | None = None
    location: str | None = None
    status: str = "normal"
    price: Decimal | None = None
    purchase_date: date | None = None
    description: str | None = None
    images: list | None = None
    qr_code_url: str | None = None
    inventory_status: str = "未盘点"
    inventory_image: str | None = None


class AssetCreate(AssetBase):
    pass


class AssetUpdate(BaseModel):
    name: str | None = None
    company_code: str | None = None
    sn: str | None = None
    category_id: int | None = None
    department: str | None = None
    user_id: int | None = None
    location: str | None = None
    status: str | None = None
    price: Decimal | None = None
    purchase_date: date | None = None
    description: str | None = None
    images: list | None = None
    qr_code_url: str | None = None


class AssetInDB(AssetBase):
    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class AssetAction(BaseModel):
    description: str | None = None