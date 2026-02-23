from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app import models
from app.database import SessionLocal, init_db
from pydantic import BaseModel
from datetime import date

init_db()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model 
# Validates the data that the API expects to receive. FastAPI uses this to check 
# class GoalCreate(BaseModel):
#     title: str
#     description: str
#     created_at: str

class GoalUpdate(BaseModel):
    title: str

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
    return [{"id": g.id, "title": g.title} for g in goals]


# Function is never used (not creating a goal from scratch)
# @app.post("/goals")
# def create_goal(goal: GoalCreate, db: Session = Depends(get_db)): 
#     db_goal = models.Goal(**goal.dict()) #converts validated Pydantic data into dict and wraps it in a SQLAlchemy object via models.py
#     db.add(db_goal) #writes to DB file
#     db.commit()
#     db.refresh(db_goal)
#     return db_goal


# Update goal
@app.put("/goals/{goal_id}")
def update_goal(goal_id: int, goal: GoalUpdate, db: Session = Depends(get_db)): 
    # print("inside pythong script PUT", goal_id)
    db_goal = db.query(models.Goal).filter(models.Goal.id == goal_id).first()
    db_goal.title = goal.title
    db.commit()
    return db_goal

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


# @app.post("/summary")
# def insertsummary(summary: SummaryCreate, db: Session - Depends(get_db)):
#     db_summary = models.Summary(**summary.dict())
#     db.add(db_summary)
#     db.commit()
#     db.refresh(db_summary)
#     return db_summary