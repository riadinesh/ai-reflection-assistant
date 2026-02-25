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

# reflections = db.query(models.Reflection).filter(models.Reflection.week_start == week_start).all()
reflections = db.query(models.Reflection).filter(models.Reflection.week_start == "2026-02-16").all()
goals_list = []
reflections_list = []
for goal in goals:
    goals_list.append(f"{goal.title}: {goal.description}") 
for reflection in reflections:
    reflections_list.append(f"{reflection.day}: {reflection.content}")


summary = generateContent(goals_list, reflections_list, week_start, week_end)
# summary = {'summary_text': "This was a week of meaningful progress across multiple areas of your life, even when it didn't always feel that way. You stayed consistent with your technical growth by debugging your reflection app and improving your project's code structure, showing real dedication despite the frustration of your QA role. A successful coffee chat boosted your networking confidence, and you made time for both dance and friendships — including the meaningful milestone of introducing your partner to your best friends. Your mood followed a natural rhythm of highs and lows, but a strong pattern emerged: whenever you took intentional action toward something that matters to you, you felt more grounded and hopeful.", 'goals_worked_on': ['Enhance my full stack and backend engineering skills.', 'Make the most of my role as a QA and still learn.', 'Say yes to more dance opportunities.', 'Spend time nurturing my female friendships.', 'Get better at corporate networking.'], 'next_steps': ['Define the next specific feature or improvement you want to build in your personal project and set a small, concrete goal to complete by next Sunday — consistency compounds over time.', 'Reach out to one or two more people for coffee chats this week while your Tuesday conversation is fresh and your confidence is up; try to connect with someone in a backend or full stack role specifically.', 'Look up one dance class or open opportunity for next week and put it on your calendar now — protecting that time will help you stay balanced during stressful work weeks.', 'Plan a low-key hangout or even a voice call with one of your female friends this week to keep that momentum going, especially since nurturing those connections is a clear source of joy for you.', "Use any slow moments at work to explore QA automation tools like Playwright or Cypress — these are in-demand technical skills that bridge QA and engineering and can strengthen your resume while you're in this role."], 'week_start': '2026-02-16', 'week_end': '2026-02-22'}
newSummary = createMessage(summary)
print(newSummary)
sendEmail(newSummary, week_start, week_end)

db_summary = models.Summary(week_start=week_start, content=summary['summary_text'], created_at=datetime.date.today().isoformat())
db.add(db_summary)
db.commit()
db.close()
