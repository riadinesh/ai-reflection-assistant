from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import datetime

from app.database import get_db
from app import models
from app.ai_summary import generateContent
from app.notification import sendEmail, createMessage
from app.auth_helpers import _get_current_user


router = APIRouter()

def getDate():
    today = datetime.date.today()
    monday = today - datetime.timedelta(days=today.weekday())
    week_start = monday.isoformat()
    week_end = (monday + datetime.timedelta(days=6)).isoformat()
    return week_start, week_end

@router.post("/summarize")
def summarize(db: Session = Depends(get_db), current_user = Depends(_get_current_user)):
    goals = db.query(models.Goal).filter(models.Goal.user_id == current_user.id).all() 
    week_start, week_end = getDate()

    reflections = db.query(models.Reflection).filter(models.Reflection.week_start == week_start and models.Reflection.user_id == current_user.id).all()
    goals_list = []
    reflections_list = []
    for goal in goals:
        goals_list.append(f"{goal.title}: {goal.description}") 
    for reflection in reflections:
        reflections_list.append(f"{reflection.day}: {reflection.content}")


    summary = generateContent(goals_list, reflections_list, week_start, week_end)
    newSummary = createMessage(summary)
    # print(newSummary)
    # sendEmail(newSummary, week_start, week_end)

    db_summary = models.Summary(week_start=week_start, user_id=current_user.id, content=summary['summary_text'], created_at=datetime.date.today().isoformat())
    db.add(db_summary)
    db.commit()
    return summary
