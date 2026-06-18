from pydantic import BaseModel


class Response(BaseModel):
    code: int = 200
    message: str = "success"
    data: object = None


class PaginationResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: list