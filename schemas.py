from pydantic import BaseModel, Field # pyright: ignore[reportMissingImports]
from typing import Optional

class UserInput(BaseModel):
    height: float = Field(..., gt=0)
    weight: float = Field(..., gt=0)
    age: int = Field(..., gt=0)
    gender: int = Field(..., ge=0, le=1) # 0 female, 1 male
    activity_level: float = Field(...)
    goal: Optional[str] = None
    body_fat: Optional[float] = None
    bmi: Optional[float] = None

class PredictionOut(BaseModel):
    plan: str
    bmi: float
    tdee: float
    calories: int
    macros: dict
    notes: Optional[str]

