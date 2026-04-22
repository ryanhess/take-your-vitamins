from pydantic import BaseModel
from typing import Literal

from enum import Enum

from database import OrmBase
from sqlalchemy import (
    Identity,
    Enum as SqlAlchEnum,
    ForeignKey,
    PrimaryKeyConstraint,
    CheckConstraint,
    UniqueConstraint,
    text,
)
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


def _query_take_not_with(id: int, db_session) -> set[int]:
    result = (
        db_session.execute(
            text("""
            SELECT id_b FROM take_not_with WHERE id_a = :id \
            UNION \
            SELECT id_a FROM take_not_with WHERE id_b = :id;
        """),
            {"id": id},
        )
        .scalars()
        .all()
    )
    return set(result)


class IngredientOrm(OrmBase):
    __tablename__ = "ingredients"
    __table_args__ = (UniqueConstraint("name", name="ingredient_name_unique"),)
    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    name: Mapped[str] = mapped_column()
    before_after_food: Mapped[BeforeAfterFood] = mapped_column(
        SqlAlchEnum(BeforeAfterFood)
    )


class IngredientConflicts(OrmBase):
    __tablename__ = "ingredient_conflicts"
    __table_args__ = (
        PrimaryKeyConstraint("id_a", "id_b"),
        CheckConstraint("id_a != id_b", name="id_a_not_equal_to_id_b"),
        CheckConstraint("id_a < id_b", name="id_a_less_than_id_b"),
    )

    id_a: Mapped[int] = mapped_column(
        ForeignKey("ingredients.id", ondelete="CASCADE"), nullable=False
    )

    id_b: Mapped[int] = mapped_column(
        ForeignKey("ingredients.id", ondelete="CASCADE"), nullable=False
    )
