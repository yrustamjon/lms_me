from fastapi.security import HTTPBearer
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from .jwt import SECRET_KEY, ALGORITHM

security = HTTPBearer()

async def verify_token(credentials = Depends(security)):
    
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")