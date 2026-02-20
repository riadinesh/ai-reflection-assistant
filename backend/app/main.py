from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app import models
from app.database import SessionLocal, init_db
from pydantic import BaseModel

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
class GoalCreate(BaseModel):
    title: str
    description: str
    created_at: str

class GoalUpdate(BaseModel):
    title: str
    
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

@app.post("/goals")
def create_goal(goal: GoalCreate, db: Session = Depends(get_db)): 
    db_goal = models.Goal(**goal.dict()) #converts validated Pydantic data into dict and wraps it in a SQLAlchemy object via models.py
    db.add(db_goal) #writes to DB file
    db.commit()
    db.refresh(db_goal)
    return db_goal

@app.put("/goals/{goal_id}")
def update_goal(goal_id: int, goal: GoalUpdate, db: Session = Depends(get_db)): 
    # print("inside pythong script PUT", goal_id)
    db_goal = db.query(models.Goal).filter(models.Goal.id == goal_id).first()
    db_goal.title = goal.title
    db.commit()
    return db_goal

