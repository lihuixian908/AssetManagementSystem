from datetime import date

from pydantic import BaseModel


class BorrowCreate(BaseModel):
    asset_id: int
    borrower: str
    department: str | None = None
    borrow_date: date | None = None
    expected_return_date: date | None = None
    location: str | None = None
    photo_url: str | None = None
    remark: str | None = None
