from app.database import Base
from sqlalchemy import Column, Integer, String, Date

class Goal(Base):
    __tablename__ = "goals"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    title = Column(String)
    description = Column(String)
    created_at = Column(String)

class Reflection(Base):
    __tablename__ = "reflections"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    week_start = Column(String)
    day = Column(String)
    content = Column(String)
    created_at = Column(String)

class Summary(Base):
    __tablename__ = "summaries"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    week_start = Column(String)
    content = Column(String)
    created_at = Column(String)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    created_at = Column(String)