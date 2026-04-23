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
    Row,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession, async_object_session


class BeforeAfterFood(str, Enum):
    before = "before"
    after = "after"


class IngredientAttributes(BaseModel):
    take_not_with: set[str] = set()
    before_after_food: Literal["before", "after"]


class IngredientInRequest(BaseModel):
    name: str


class IngredientResponse(BaseModel):
    name: str
    before_after_food: BeforeAfterFood
    take_not_with: set[str] = set()
    DEV_conflict_count: int = 0

    class Config:
        from_attributes = True


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


async def _query_take_not_with(id: int, db_session: AsyncSession) -> set[Row]:
    result = await db_session.execute(
        text("""
            WITH conflict_ids AS (
                SELECT id_b as id FROM ingredient_conflicts WHERE id_a = :id
                UNION
                SELECT id_a FROM ingredient_conflicts WHERE id_b = :id
            )
            SELECT i.* 
            FROM ingredients i
            JOIN conflict_ids c
            ON c.id = i.id;
        """),
        {"id": id},
    )
    result_list = result.all()
    return set(result_list)


class IngredientOrm(OrmBase):
    __tablename__ = "ingredients"
    __table_args__ = (UniqueConstraint("name", name="ingredient_name_unique"),)
    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    name: Mapped[str] = mapped_column()
    before_after_food: Mapped[BeforeAfterFood] = mapped_column(
        SqlAlchEnum(BeforeAfterFood)
    )

    async def take_not_with(self) -> set["IngredientOrm"]:
        session = async_object_session(self)
        if session is None:
            return set()
        else:
            result = await _query_take_not_with(id=self.id, db_session=session)
            ingredients_list = {
                IngredientOrm(id=res[0], name=res[1], before_after_food=res[2])
                for res in result
            }
            return ingredients_list


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
