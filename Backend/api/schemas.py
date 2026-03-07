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
    

class UserResponse(UserCreate):
    id: int
    is_active: bool
    create_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True

class RefreshSchema(BaseModel):
    refresh_token: str