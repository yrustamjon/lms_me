from fastapi import FastAPI, Depends
from .security import verify_token
from fastapi.middleware.cors import CORSMiddleware
from .schemas import *
from models.user import User
from .jwt import *

from api.app.base import app as base_app
from api.app.admin import app as admin_app


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_middleware(AuthMiddleware)


@app.post("/api/auth/login/")
async def login(user : UserLogin):
    print(user)
    u=User.objects.get(email=user.email)
    if u is None:
        return {"error": "User not found"}
    if u.hashed_password!=user.password:
        return {"error": "Invalid password"}
    
    access_token=create_access_token({'user_id':u.id})
    refresh_token=create_refresh_token({'user_id':u.id})
    
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        'user':
            {
                "id": u.id,
                "name": u.name,
                "email": u.email,
                "role": u.role
            },
    }


from fastapi import HTTPException

@app.post("/api/auth/refresh/")
async def refresh(data: RefreshSchema):
    try:
        payload = jwt.decode(data.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        new_access_token = create_access_token({"user_id": user_id})

        return {"access_token": new_access_token}

    except JWTError:
        raise HTTPException(status_code=401, detail="Refresh token expired")

app.include_router(base_app)
app.include_router(admin_app)