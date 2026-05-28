from pydantic import BaseModel
from datetime import date
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class ReflectionCreate(BaseModel):
    week_start: str
    day: str
    content: str
    created_at: str = date.today().isoformat()

class GoalCreate(BaseModel):
    title: str
    description: str = ""
    created_at: str = date.today().isoformat()

class GoalUpdate(BaseModel):
    title: str
    description: Optional[str] = None