from pydantic import BaseModel
from typing import Literal

from enum import Enum

from database import OrmBase
from sqlalchemy import Identity, Enum as SqlAlchEnum
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


class BeforeAfterFood(str, Enum):
    before = "before"
    after = "after"


class IngredientOrm(OrmBase):
    __tablename__ = "ingredients"
    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    name: Mapped[str]
    before_after_food: Mapped[BeforeAfterFood] = mapped_column(
        SqlAlchEnum(BeforeAfterFood)
    )
