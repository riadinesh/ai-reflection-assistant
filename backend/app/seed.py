from app.database import SessionLocal, init_db
from app import models
import datetime 

init_db()

goals = [
    models.Goal(title="Enhance my full stack and backend engineering skills.", description="It's hard for me to be competitve in this job market if I don't have these skills. It's important that I sharpen them so that I can be more prepared for interviews and the roles that I'm applying for.", created_at=datetime.date.fromisoformat("2026-02-19")),
    models.Goal(title="Make the most of my role as a QA and still learn.", description="I was moved to a role I really did not want to be in, where I'm not developing features, just writing test cases for months. I want to still learn something that will be helpful for me in this industry, given the QA role is slowly dying. ", created_at=datetime.date.fromisoformat("2026-02-19")),
    models.Goal(title="Say yes to more dance opportunities.", description="Dancing has been a big part of my life and I'd love to keep particpating in heels/hip hop/cheer opportunities.", created_at=datetime.date.fromisoformat("2026-02-19")),
    models.Goal(title="Spend time nurturing my female friendships.", description="It's very important to me now that I'm in a relationship to still maintain my female friendships. This will help me feel more fulfilled in the friendship space.", created_at=datetime.date.fromisoformat("2026-02-19")),
    models.Goal(title="Get better at corporate networking.", description="I'd love to feel more confident selling myself and also learniing about what other people do. I want to ask the right questions, and hopefully land a new job.", created_at=datetime.date.fromisoformat("2026-02-19")),
]
db = SessionLocal()
db.add_all(goals)
db.commit()
db.close()
print("Seeded 5 goals!")
