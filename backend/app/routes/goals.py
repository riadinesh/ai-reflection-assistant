from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schema import GoalCreate, GoalUpdate
from app import models
from app.database import get_db
from app.auth_helpers import _get_current_user

router = APIRouter()



@router.get("/goals")
def get_goals(db: Session = Depends(get_db), current_user = Depends(_get_current_user)):
    print("current user: ", current_user)
    goals = db.query(models.Goal).filter(models.Goal.user_id == current_user.id).all()
    return [{"id": g.id, "title": g.title, "description": g.description or ""} for g in goals]

@router.post("/goals")
def create_goal(goal: GoalCreate, db: Session = Depends(get_db), current_user = Depends(_get_current_user)):
    print("THIS IS CURRENT USER: ", current_user.id)
    db_goal = models.Goal(**goal.model_dump(), user_id=current_user.id)
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return {"id": db_goal.id, "user_id": current_user.id, "title": db_goal.title, "description": db_goal.description or ""}

@router.delete("/goals/{goal_id}")
def delete_goal(goal_id: int, db: Session = Depends(get_db), current_user = Depends(_get_current_user)):
    db_goal = db.query(models.Goal).filter(models.Goal.id == goal_id, models.Goal.user_id == current_user.id).first()
    db.delete(db_goal)
    db.commit()
    return {"ok": True}

@router.put("/goals/{goal_id}")
def update_goal(goal_id: int, goal: GoalUpdate, db: Session = Depends(get_db), current_user = Depends(_get_current_user)):
    db_goal = db.query(models.Goal).filter(models.Goal.id == goal_id, models.Goal.user_id == current_user.id).first()
    db_goal.title = goal.title
    if goal.description is not None:
        db_goal.description = goal.description
    db.commit()
    return {"id": db_goal.id, "title": db_goal.title, "description": db_goal.description or ""}
