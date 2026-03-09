from pydantic import BaseModel
import datetime

class UserLogin(BaseModel):
    email: str
    password: str
    
class UserCreate(BaseModel):
    name: str
    email: str
    role: str
    password: str

class UserMe(BaseModel):
    id: int
    name: str
    email: str
    role: str

class UserMeUpdate(BaseModel):
    name: str
    email: str
    role: str
    password: str


class UserOut(BaseModel):
    id: int
    name: str
    email: str
    role: str
    hashed_password: str
    is_active: bool
    is_verified: bool
    is_superuser: bool



class RefreshSchema(BaseModel):
    refresh_token: str

class AccessSchema(BaseModel):
    access_token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str


class StudentOut(BaseModel):
    id: int
    name: str
    phone: str
    email: str
    is_active: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime

class GroupOut(BaseModel):
    id: int
    name: str
    description: str
    teacher_id: int
    students: list[StudentOut]
    created_at: datetime.datetime
    updated_at: datetime.datetime
