from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app import models
from app.database import SessionLocal, init_db
from pydantic import BaseModel
from datetime import date
from typing import Optional

init_db()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class GoalCreate(BaseModel):
    title: str
    description: str = ""
    created_at: str = date.today().isoformat()

class GoalUpdate(BaseModel):
    title: str
    description: Optional[str] = None

class ReflectionCreate(BaseModel):
    week_start: str
    day: str
    content: str
    created_at: str = date.today().isoformat()

class SummaryCreate(BaseModel):
    week_start: str
    content: str
    created_at: str = date.today().isoformat()
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/goals")
def get_goals(db: Session = Depends(get_db)):
    goals = db.query(models.Goal).all()
    return [{"id": g.id, "title": g.title, "description": g.description or ""} for g in goals]

@app.post("/goals")
def create_goal(goal: GoalCreate, db: Session = Depends(get_db)):
    db_goal = models.Goal(**goal.dict())
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return {"id": db_goal.id, "title": db_goal.title, "description": db_goal.description or ""}

@app.delete("/goals/{goal_id}")
def delete_goal(goal_id: int, db: Session = Depends(get_db)):
    db_goal = db.query(models.Goal).filter(models.Goal.id == goal_id).first()
    db.delete(db_goal)
    db.commit()
    return {"ok": True}

# Update goal
@app.put("/goals/{goal_id}")
def update_goal(goal_id: int, goal: GoalUpdate, db: Session = Depends(get_db)):
    db_goal = db.query(models.Goal).filter(models.Goal.id == goal_id).first()
    db_goal.title = goal.title
    if goal.description is not None:
        db_goal.description = goal.description
    db.commit()
    return {"id": db_goal.id, "title": db_goal.title, "description": db_goal.description or ""}

# Render reflections
@app.get("/reflections")
def get_reflections(week_start: str, db: Session = Depends(get_db)):
    reflections = db.query(models.Reflection).filter(
        models.Reflection.week_start == week_start
    ).all()
    return [{"id": r.id, "day": r.day, "content": r.content} for r in reflections]

# Create/update reflections
@app.post("/reflections")
def upsert_reflection(reflection: ReflectionCreate, db: Session = Depends(get_db)):
    print("inside pythong script POST", reflection)
    existing = db.query(models.Reflection).filter(
        models.Reflection.week_start == reflection.week_start,
        models.Reflection.day == reflection.day
    ).first()
    # Update reflection
    if existing:
        existing.content = reflection.content
        db.commit()
        db.refresh(existing)
        return existing
    # Create reflection
    else:
        db_reflection = models.Reflection(**reflection.dict())
        db.add(db_reflection)
        db.commit()
        db.refresh(db_reflection)
        return db_reflection
