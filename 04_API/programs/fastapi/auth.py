from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

SECRET_KEY = "secret-key"
ALGORITHM = "HS256"

security = HTTPBearer()

def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        subject = payload.get("sub")

        if subject is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return subject

    except JWTError as e:
        print(e)
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )