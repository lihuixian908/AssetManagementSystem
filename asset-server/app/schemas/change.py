from pydantic import BaseModel


class ChangeCreate(BaseModel):
    asset_id: int
    change_type: str
    new_value: str
    remark: str | None = None
