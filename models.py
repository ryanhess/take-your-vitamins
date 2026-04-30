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


class IngredientInRequest(BaseModel):
    name: str


class IngredientResponse(BaseModel):
    name: str
    before_after_food: BeforeAfterFood
    take_not_with: set[str] = set()
    DEV_conflict_count: int = 0

    class Config:
        from_attributes = True

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        result = isinstance(other, IngredientResponse) and self.name == other.name
        return result


class TimeSlots(BaseModel):
    before_breakfast: list[IngredientResponse] = []
    after_breakfast: list[IngredientResponse] = []
    before_lunch: list[IngredientResponse] = []
    after_lunch: list[IngredientResponse] = []
    before_dinner: list[IngredientResponse] = []
    after_dinner: list[IngredientResponse] = []


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


class TimeSlotNames(str, Enum):
    before_breakfast = "before_breakfast"
    after_breakfast = "after_breakfast"
    before_lunch = "before_lunch"
    after_lunch = "after_lunch"
    before_dinner = "before_dinner"
    after_dinner = "after_dinner"


class IngredientInSchedule(OrmBase):
    __tablename__ = "ingredients_in_schedule"
    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    ingredient_id: Mapped[int] = mapped_column(
        ForeignKey("ingredients.id", ondelete="CASCADE"), nullable=False
    )
    schedule_id: Mapped[int] = mapped_column(
        ForeignKey("schedules.id", ondelete="CASCADE"), nullable=False
    )
    slot: Mapped[TimeSlotNames] = mapped_column(SqlAlchEnum(TimeSlotNames))


class SupplementSchedule(OrmBase):
    __tablename__ = "schedules"
    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    user_id: Mapped[int] = mapped_column(default=1)
