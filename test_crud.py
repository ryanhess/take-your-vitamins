from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from crud import Schedule
import pytest
from models import (
    IngredientInSchedule,
    IngredientOrm,
    SupplementSchedule,
    TimeSlotNames,
    BeforeAfterFood,
)


@pytest.fixture
async def seeded_db(db: AsyncSession) -> AsyncGenerator[AsyncSession, None]:
    ingredients = {
        "Vitamin C": BeforeAfterFood.before,
        "Vitamin B12": BeforeAfterFood.before,
        "Folate": BeforeAfterFood.before,
        "Vitamin B6": BeforeAfterFood.before,
        "Niacin": BeforeAfterFood.before,
        "Vitamin D": BeforeAfterFood.after,
        "Vitamin A": BeforeAfterFood.after,
        "Vitamin E": BeforeAfterFood.after,
        "Vitamin K2": BeforeAfterFood.after,
        "Retinol": BeforeAfterFood.after,
        "Calcium": BeforeAfterFood.after,
        "Iron": BeforeAfterFood.before,
        "Zinc": BeforeAfterFood.before,
        "Magnesium": BeforeAfterFood.after,
        "Copper": BeforeAfterFood.before,
        "Manganese": BeforeAfterFood.before,
        "Green Tea Extract": BeforeAfterFood.before,
        "Turmeric": BeforeAfterFood.after,
        "Quercetin": BeforeAfterFood.before,
        "Ashwagandha": BeforeAfterFood.after,
        "Mugwort": BeforeAfterFood.after,
        "NAC": BeforeAfterFood.before,
        "L-Theanine": BeforeAfterFood.before,
        "Beta-Alanine": BeforeAfterFood.before,
        "Taurine": BeforeAfterFood.after,
        "Creatine": BeforeAfterFood.after,
        "Caffeine": BeforeAfterFood.before,
        "Probiotics": BeforeAfterFood.before,
        "Collagen": BeforeAfterFood.after,
        "Fish Oil": BeforeAfterFood.after,
    }

    schedule_entries = [
        ("Vitamin C", TimeSlotNames.before_breakfast),
        ("Vitamin B12", TimeSlotNames.before_breakfast),
        ("Probiotics", TimeSlotNames.before_breakfast),
        ("Vitamin D", TimeSlotNames.after_breakfast),
        ("Vitamin A", TimeSlotNames.after_breakfast),
        ("Magnesium", TimeSlotNames.after_lunch),
        ("Turmeric", TimeSlotNames.after_lunch),
        ("Zinc", TimeSlotNames.before_dinner),
        ("Fish Oil", TimeSlotNames.after_dinner),
        ("Ashwagandha", TimeSlotNames.after_dinner),
    ]

    for name, before_after in ingredients.items():
        db.add(IngredientOrm(name=name, before_after_food=before_after))
    await db.flush()

    result = await db.execute(select(IngredientOrm))
    name_to_id = {row.name: row.id for row in result.scalars().all()}

    schedule = SupplementSchedule(user_id=1)
    db.add(schedule)
    await db.flush()

    for name, slot in schedule_entries:
        db.add(
            IngredientInSchedule(
                ingredient_id=name_to_id[name],
                schedule_id=schedule.id,
                slot=slot,
            )
        )

    await db.flush()

    yield db


class TestUpdateSchedule:
    async def test_raises_for_not_found(self) -> None:
        pass

    async def test_raises_for_ingred_not_found(self) -> None:
        pass

    async def test_update_with_empty_clears_schedule(self) -> None:
        pass

    async def test_idempotent(self) -> None:
        pass

    async def test_updates_schedule_in_db(self, seeded_db: AsyncSession) -> None:
        pass
