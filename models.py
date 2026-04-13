from pydantic import BaseModel
from typing import Literal


class IngredientAttributes(BaseModel):
    take_not_with: list[str] = []
    before_after_food: Literal["before", "after"]


class IngredientInRequest(BaseModel):
    name: str


class IngredientInResponse(BaseModel):
    name: str
    DEV__conflict_count: int = 0


class TimeSlots(BaseModel):
    before_breakfast: list[IngredientInResponse] = []
    after_breakfast: list[IngredientInResponse] = []
    before_lunch: list[IngredientInResponse] = []
    after_lunch: list[IngredientInResponse] = []
    before_dinner: list[IngredientInResponse] = []
    after_dinner: list[IngredientInResponse] = []


class SupplimentPlanResponse(BaseModel):
    DEV_total_conflict_count: int = 0
    schedule: TimeSlots
