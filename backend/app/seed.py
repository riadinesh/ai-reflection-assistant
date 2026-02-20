from app.database import SessionLocal, init_db
from app import models

init_db()

goals = [
    models.Goal(title="Goal1", description="desc1", created_at="2026-02-19"),
    models.Goal(title="Goal2", description="desc2", created_at="2026-02-19"),
    models.Goal(title="Goal3", description="desc3", created_at="2026-02-19"),
    models.Goal(title="Goal4", description="desc4", created_at="2026-02-19"),
    models.Goal(title="Goal5", description="desc5", created_at="2026-02-19"),
]
db = SessionLocal()
db.add_all(goals)
db.commit()
db.close()
print("Seeded 5 goals!")
