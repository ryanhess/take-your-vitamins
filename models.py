from pydantic import BaseModel
from typing import Literal

from database import OrmBase
from sqlalchemy import Identity
from sqlalchemy.orm import Mapped, mapped_column


class IngredientAttributes(BaseModel):
    take_not_with: set[str] = set()
    before_after_food: Literal["before", "after"]


class IngredientInRequest(BaseModel):
    name: str


class IngredientInResponse(BaseModel):
    name: str
    constraints: IngredientAttributes
    DEV_conflict_count: int = 0


class TimeSlots(BaseModel):
    before_breakfast: list[IngredientInResponse] = []
    after_breakfast: list[IngredientInResponse] = []
    before_lunch: list[IngredientInResponse] = []
    after_lunch: list[IngredientInResponse] = []
    before_dinner: list[IngredientInResponse] = []
    after_dinner: list[IngredientInResponse] = []


class SupplementPlanResponse(BaseModel):
    DEV_total_conflict_count: int = 0
    schedule: TimeSlots = TimeSlots()
    supplements_not_found: list[str] = []
