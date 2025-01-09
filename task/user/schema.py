from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import List
import uuid
from typing import Optional

class UserBase(BaseModel):
    id:int
    name: str
    email: EmailStr
    age: Optional[int] = None
    gender: Optional[str] = None

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    password: Optional[str] = None


class UserResponse(UserBase):
    id: int
    is_deleted: bool

    class Config:
        orm_mode = True

class CompetitionBase(BaseModel):
    competition_name: str
    competition_date: datetime
    duration: int
    user_capacity: int

    class Config:
        orm_mode = True


class CompetitionCreate(CompetitionBase):
    pass


class CompetitionUpdate(BaseModel):
    competition_name: Optional[str] = None
    competition_date: Optional[datetime] = None
    duration: Optional[int] = None
    user_capacity: Optional[int] = None


class CompetitionEntryBase(BaseModel):
    user_id: int
    competition_id: int
    is_deleted: Optional[bool] = False

    class Config:
        orm_mode = True


class CompetitionEntryCreate(CompetitionEntryBase):
    pass


class CompetitionEntryUpdate(BaseModel):
    is_deleted: Optional[bool] = None
