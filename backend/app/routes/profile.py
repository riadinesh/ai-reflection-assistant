from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schema import ProfileUpdate
from app import models
from app.database import get_db
from app.auth_helpers import _get_current_user

router = APIRouter()


@router.get("/me")
def get_me(db: Session = Depends(get_db), current_user = Depends(_get_current_user)):
    username = current_user.username
    email = current_user.email
    return {"username": username, "email": email}

@router.put("/settings")
def change_username(profile: ProfileUpdate, db: Session = Depends(get_db), current_user = Depends(_get_current_user)):
    db_user = db.query(models.User).filter(models.User.id == current_user.id).first()
    if db_user.username != profile.username:
        db_user.username = profile.username
    if db_user.email != profile.email:
        db_user.email = profile.email
    db.commit()
    return {"message": "username/emailchanged"}





