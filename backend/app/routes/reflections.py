from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.schema import ReflectionCreate
from app import models
from app.database import get_db
from app.auth_helpers import _get_current_user

router = APIRouter()

@router.get("/reflections")
def get_reflections(week_start: str, db: Session = Depends(get_db), current_user = Depends(_get_current_user)):
    print("current user ID: ", current_user.id)
    reflections = db.query(models.Reflection).filter(
        models.Reflection.week_start == week_start, models.Reflection.user_id == current_user.id
    ).all()
    return [{"id": r.id, "day": r.day, "content": r.content} for r in reflections]

@router.post("/reflections")
def upsert_reflection(reflection: ReflectionCreate, db: Session = Depends(get_db), current_user = Depends(_get_current_user)):
    print("THIS IS CURRENT USER: ", current_user.id)
    existing = db.query(models.Reflection).filter(
        models.Reflection.week_start == reflection.week_start,
        models.Reflection.day == reflection.day,
        models.Reflection.user_id == current_user.id
    ).first()
    if existing:
        existing.content = reflection.content
        db.commit()
        db.refresh(existing)
        return existing
    else:
        db_reflection = models.Reflection(**reflection.model_dump(), user_id=current_user.id)
        db.add(db_reflection)
        db.commit()
        db.refresh(db_reflection)
        return db_reflection
