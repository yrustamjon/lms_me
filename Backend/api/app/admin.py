from fastapi import APIRouter, Depends, Request
from api.security import verify_token
from fastapi import Header
from sqlalchemy.exc import IntegrityError

from api.schemas import *
from models.user import User
from api.jwt import *

app = APIRouter(dependencies=[Depends(verify_token)],tags=["Admin"],prefix="/api/admin")

@app.get("/teachers/", response_model=list[UserOut])
async def teacher(request: Request):
    user=request.state.user
    if user.role!="admin":
        return {"error": "Unauthorized"}
    
    teachers=User.objects.filter(role="teacher")
    return teachers


@app.post("/teachers", response_model=UserOut)
async def create_teacher(user:  UserCreate,request: Request):
    u=request.state.user
    if u.role!="admin":
        return {"error": "Unauthorized"}
    
    try:
        teacher=User.objects.create(name=user.name,email=user.email,hashed_password=user.password,role=user.role)
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )
    return teacher


@app.delete("/teachers/{teacher_id}/")
async def delete_teacher(teacher_id: int,request: Request):
    u=request.state.user
    if u.role!="admin":
        return {"error": "Unauthorized"}
    
    teacher=User.objects.get(id=teacher_id)
    if teacher is None:
        return {"error": "Teacher not found"}
    
    teacher.delete()
    return {"message": "Teacher deleted successfully"}