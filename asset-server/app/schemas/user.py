from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    real_name: str
    department: str | None = None
    role: str = "user"
    phone: str | None = None
    email: str | None = None
    status: int = 1


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    real_name: str | None = None
    department: str | None = None
    role: str | None = None
    phone: str | None = None
    email: str | None = None
    status: int | None = None


class UserInDB(UserBase):
    id: int

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username: str
    password: str


class ChangePassword(BaseModel):
    old_password: str
    new_password: str


class ResetPasswordRequest(BaseModel):
    new_password: str