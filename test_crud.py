from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from crud import Schedule
from pytest import fixture, raises
from models import (
    IngredientInSchedule,
    IngredientOrm,
    IngredientResponse,
    SupplementSchedule,
    TimeSlotNames,
    BeforeAfterFood,
    TimeSlots,
)
from exceptions import ResourceNotFound


@fixture
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


@fixture
async def id_of_test_sched(db: AsyncSession) -> AsyncGenerator[int | None, None]:
    result = await db.execute(select(SupplementSchedule))
    test_sched = result.scalar_one_or_none()
    test_sched_id = getattr(test_sched, "id", None)
    print(test_sched_id)
    yield test_sched_id


class TestUpdateSchedule:
    async def test_raises_for_not_found(
        self, seeded_db: AsyncSession, id_of_test_sched: int
    ) -> None:
        assert id_of_test_sched
        with raises(ResourceNotFound):
            await Schedule.update(
                sched_id=id_of_test_sched + 1, updated_sched=TimeSlots(), db=seeded_db
            )

    async def test_raises_for_ingred_not_found(
        self, seeded_db: AsyncSession, id_of_test_sched: int
    ) -> None:
        new_sched = TimeSlots(
            before_breakfast=[
                IngredientResponse(
                    name="not in the database", before_after_food=BeforeAfterFood.before
                )
            ]
        )

        with raises(ResourceNotFound):
            await Schedule.update(
                sched_id=id_of_test_sched, updated_sched=new_sched, db=seeded_db
            )

    async def test_update_with_empty_clears_schedule(self) -> None:
        pass

    async def test_idempotent(self) -> None:
        pass

    async def test_updates_schedule_in_db(
        self, seeded_db: AsyncSession, id_of_test_sched: int
    ) -> None:
        test_ingred_name = "L-Theanine"
        result = await seeded_db.execute(
            select(IngredientOrm).where(IngredientOrm.name == test_ingred_name)
        )
        test_ingred = result.scalar_one_or_none()
        assert test_ingred

        test_sched_id = id_of_test_sched
        assert test_sched_id

        new_sched = TimeSlots(
            before_breakfast=[
                IngredientResponse(
                    name=test_ingred_name, before_after_food=BeforeAfterFood.before
                )
            ]
        )
        await Schedule.update(
            sched_id=test_sched_id, updated_sched=new_sched, db=seeded_db
        )

        result = await seeded_db.execute(
            select(IngredientInSchedule).where(
                IngredientInSchedule.schedule_id == test_sched_id
            )
        )
        entries = result.scalars().all()

        assert len(entries) == 1
        assert entries[0].ingredient_id == test_ingred.id
