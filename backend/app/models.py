from app.database import Base
from sqlalchemy import Column, Integer, String, Date

class Goal(Base):
    __tablename__ = "goals"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    created_at = Column(String)

class Reflection(Base):
    __tablename__ = "reflections"
    id = Column(Integer, primary_key=True, index=True)
    week_start = Column(String)
    day = Column(String)
    content = Column(String)
    created_at = Column(String)