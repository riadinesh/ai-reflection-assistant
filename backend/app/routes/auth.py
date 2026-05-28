from fastapi import APIRouter, Depends
import bcrypt
from datetime import timedelta
from sqlalchemy.orm import Session

from app.database import *
from app.models import User
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.schema import UserCreate, UserLogin
from app.auth_helpers import _create_access_token


router = APIRouter()

@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    print(user.username, user.password, user.email)
    if user.username == "" or user.password == "":
        return {"message": "Please provide a username or password"}
    if len(user.password) < 8 or user.password.isalnum():
        return {"message": "Password must be at least 8 characters and must contain a special character"}
    
    password = user.password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password, salt).decode("utf-8")

    db_user = User(username=user.username, email=user.email, password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = _create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    # return {"message": "Successfully signed up"}
    return {"message": "Successfully signed up", "access_token": access_token}



@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user:
        return {"message": "User not found."}
    if not bcrypt.checkpw(user.password.encode("utf-8"), db_user.password.encode("utf-8")):
        return {"message": "Incorrect password. Try again."}

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = _create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"message": "Successfully logged in", "access_token": access_token}