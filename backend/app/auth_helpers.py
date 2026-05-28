from fastapi import Depends, HTTPException
from pydantic import BaseModel
from app.database import *
from app.models import User
from jose import jwt
from datetime import datetime, timedelta, timezone, date
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.config import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def _get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except:
        raise HTTPException(status_code=401)

    user = db.query(User).filter(User.username == username).first()
    if user is None:
          raise HTTPException(status_code=401, detail="User not found")
    return user
 
def _create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt