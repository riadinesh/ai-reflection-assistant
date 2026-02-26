from app.database import SessionLocal, init_db
from app import models
import datetime 
from app.ai_summary import generateContent
from app.notification import sendEmail, createMessage

init_db()
db = SessionLocal()

goals = db.query(models.Goal).all() 

today = datetime.date.today()
monday = today - datetime.timedelta(days=today.weekday())
week_start = monday.isoformat()
week_end = (monday + datetime.timedelta(days=6)).isoformat()

reflections = db.query(models.Reflection).filter(models.Reflection.week_start == week_start).all()
# reflections = db.query(models.Reflection).filter(models.Reflection.week_start == "2026-02-16").all()
goals_list = []
reflections_list = []
for goal in goals:
    goals_list.append(f"{goal.title}: {goal.description}") 
for reflection in reflections:
    reflections_list.append(f"{reflection.day}: {reflection.content}")


summary = generateContent(goals_list, reflections_list, week_start, week_end)
newSummary = createMessage(summary)
print(newSummary)
sendEmail(newSummary, week_start, week_end)

db_summary = models.Summary(week_start=week_start, content=summary['summary_text'], created_at=datetime.date.today().isoformat())
db.add(db_summary)
db.commit()
db.close()
