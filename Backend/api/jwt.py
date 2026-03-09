from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from models.user import *
SECRET_KEY="Rustamjon"
ALGORITHM="HS256"
secund=10
minute=60
hour=0
day=7

def create_access_token(data: dict ):
    expire = datetime.now(timezone.utc) + timedelta(minutes=minute)
    data.update({"exp":expire})
    return jwt.encode(data,SECRET_KEY,algorithm=ALGORITHM)

def create_refresh_token(data: dict):
    expire = datetime.now(timezone.utc) + timedelta(days=day)
    data.update({"exp":expire})
    return jwt.encode(data,SECRET_KEY,algorithm=ALGORITHM)    

from starlette.responses import JSONResponse

PUBLIC_PATHS = [
    "/docs",
    "/redoc",
    "/openapi.json",
    "/api/auth/login/",
    "/api/auth/refresh/",
    "/api/users"
]



class AuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        if request.url.path in PUBLIC_PATHS:
            return await call_next(request)


        # CORS preflight request
        if request.method == "OPTIONS":
            return await call_next(request)

        auth_header = request.headers.get("Authorization")

        # if ! not auth_header:
        #     return JSONResponse(
        #         status_code=401,
        #         content={"detail": "Authorization token required"}
        #     )

        # try:
        #     token = auth_header.split(" ")[1]

        #     payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        #     user_id = payload.get("user_id")

        #     user = User.objects.get(id=user_id)
        #     request.state.user = user

        # except JWTError:
        #     return JSONResponse(
        #         status_code=401,
        #         content={"detail": "Invalid token"}
        #     )


        request.state.user =User.objects.get(role="admin")
        return await call_next(request)