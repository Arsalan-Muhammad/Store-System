from datetime import datetime, timedelta
from pickletools import read_uint1
from fastapi import Depends, HTTPException, status
from jose import jwt , JWTError
from fastapi.security import OAuth2PasswordBearer
from jwt import JWT
import schemas
from schemas import TokenData
from routes import auths
SECRET_KEY = "sgi3w976s4wedfidfghjfgharsalan"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1080


oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data : dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expire})

    encoded_jwt = jwt.encode(to_encode , SECRET_KEY , algorithm=ALGORITHM)

    return encoded_jwt

def verify_token(token:str , credentials_exceptions):
    try:
        payload = jwt.decode(token , SECRET_KEY , algorithms=[ALGORITHM])

        id : int = payload.get("user_id") #pyright:ignore

        if id is None:
            raise credentials_exceptions
        
        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise credentials_exceptions
    
    return token_data

def get_current_user(token: str = Depends(oauth_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return verify_token(token, credentials_exception)