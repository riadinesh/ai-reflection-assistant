from app.database import SessionLocal, init_db
from app import models
import datetime 
from ai_summary.py import generateContent


init_db()
db = SessionLocal()

goals = db.query(models.Goal).all() 

today = datetime.date.today()
monday = today - datetime.timedelta(days=today.weekday())
week_start = monday.isoformat()

reflections = db.query(models.Reflection).filter(models.Reflection.week_start == week_start).all()

summary = generateContent(goals, reflections)

# for goal in goals:
#     summary += f"{goal.title}: {goal.description}\n"
# for reflection in reflections:
#     summary += f"{reflection.day}: {reflection.content}\n"

db_summary = models.Summary(week_start=week_start, content=summary, created_at=datetime.date.today().isoformat())
db.add(db_summary)
db.commit()
db.close()