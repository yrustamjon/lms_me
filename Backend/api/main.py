from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .schemas import *
from models.user import User
from .jwt import *


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

@app.get("/api/users")
async def users():
    user=User.objects.all()
    print(user)
    return {"users": list(user)}

@app.post("/api/users")
async def create_user(user:  UserCreate):
    user=User.objects.create(name=user.name,email=user.email,hashed_password=user.password,role=user.role)
    return {"user": user.name}


@app.post("/api/auth/login")
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


@app.post("/api/auth/refresh")
async def refresh(data: RefreshSchema):
    try:
        from .jwt import SECRET_KEY, ALGORITHM
        payload = jwt.decode(data.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            return {"error": "Invalid token"}
        
        new_access_token = create_access_token({"user_id": user_id})
        return {"access_token": new_access_token}
    except JWTError:
        return {"error": "Invalid token"}


@app.post("/api/admin/students/")
async def admin_student_create():
    return [
  {
    "id": 1,
    "full_name": "Ali Valiyev",
    "phone": "+998901234567",
    "status": "active"
  }
]

@app.get("/api/admin/students/")
async def admin_student():
    return [
  {
    "id": 1,
    "full_name": "Ali Valiyev",
    "phone": "+998901234567",
    "status": "active"
  }
]
