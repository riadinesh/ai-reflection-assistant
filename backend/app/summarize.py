from app.database import SessionLocal, init_db
from app import models
import datetime 
from app.ai_summary import generateContent


init_db()
db = SessionLocal()

goals = db.query(models.Goal).all() 

today = datetime.date.today()
monday = today - datetime.timedelta(days=today.weekday())
week_start = monday.isoformat()

reflections = db.query(models.Reflection).filter(models.Reflection.week_start == week_start).all()
goals_list = []
reflections_list = []
for goal in goals:
    goals_list.append(f"{goal.title}: {goal.description}") 
for reflection in reflections:
    reflections_list.append(f"{reflection.day}: {reflection.content}")

summary = generateContent(goals_list, reflections_list)
print(summary)

db_summary = models.Summary(week_start=week_start, content=summary, created_at=datetime.date.today().isoformat())
db.add(db_summary)
db.commit()
db.close()