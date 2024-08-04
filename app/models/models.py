from typing import Optional

from pydantic import BaseModel, EmailStr, HttpUrl
from sqlmodel import Field, SQLModel
from typing_extensions import List


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr
    first_name: str
    last_name: str
    avatar: str


class UserCreate(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    avatar: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar: Optional[str] = None


class PaginatedResponse(BaseModel):
    items: List[User]
    total: int
    page: int
    size: int
    pages: int
