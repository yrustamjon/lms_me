from fastapi import APIRouter, Depends, Request
from api.security import verify_token
from fastapi import Header

from api.schemas import *
from models.user import User
from api.jwt import *

app = APIRouter(dependencies=[Depends(verify_token)])



@app.get("/api/users")
async def users():
    user=User.objects.all()
    print(user)
    return {"users": list(user)}

# @app.post("/api/users")
# async def create_user(user:  UserCreate):
#     user=User.objects.create(name=user.name,email=user.email,hashed_password=user.password,role=user.role)
#     return {"user": user.name}




@app.get("/api/auth/me/")
async def get_me(request: Request):
    user = request.state.user
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role
    }


@app.put("/api/auth/me/", response_model=UserOut)
async def update_me(user_data: UserMeUpdate, request: Request):

    user = request.state.user

    if not user:
        return {"error": "Not authenticated"}
    update_data = user_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(user, key, value)
    


    if user_data.password:
        user.hashed_password = user_data.password

    user.save()

    return user