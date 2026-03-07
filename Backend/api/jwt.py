from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
SECRET_KEY="Rustamjon"
ALGORITHM="HS256"
secund=10
minute=60
hour=0
day=7

def create_access_token(data: dict ):
    expire = datetime.now(timezone.utc) + timedelta(seconds=1)
    data.update({"exp":expire})
    return jwt.encode(data,SECRET_KEY,algorithm=ALGORITHM)

def create_refresh_token(data: dict):
    expire = datetime.now(timezone.utc) + timedelta(seconds=1)
    data.update({"exp":expire})
    return jwt.encode(data,SECRET_KEY,algorithm=ALGORITHM)    

class AuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        # public endpointlar
        if request.url.path.startswith("/api/auth"):
            return await call_next(request)

        auth = request.headers.get("Authorization")

        if not auth:
            raise HTTPException(status_code=401, detail="Token missing")

        try:
            scheme, token = auth.split()
            jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        response = await call_next(request)
        return response
