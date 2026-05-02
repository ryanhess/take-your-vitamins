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
async def seeded_db(seeded_db: AsyncSession) -> AsyncGenerator[AsyncSession, None]:
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
        seeded_db.add(IngredientOrm(name=name, before_after_food=before_after))
    await seeded_db.flush()

    result = await seeded_db.execute(select(IngredientOrm))
    name_to_id = {row.name: row.id for row in result.scalars().all()}

    schedule = SupplementSchedule(user_id=1)
    seeded_db.add(schedule)
    await seeded_db.flush()

    for name, slot in schedule_entries:
        seeded_db.add(
            IngredientInSchedule(
                ingredient_id=name_to_id[name],
                schedule_id=schedule.id,
                slot=slot,
            )
        )

    await seeded_db.flush()

    yield seeded_db


async def get_test_schedule_entries_from_db(
    id: int, db: AsyncSession
) -> list[IngredientInSchedule]:
    result = await db.execute(
        select(IngredientInSchedule).where(IngredientInSchedule.schedule_id == id)
    )
    entries = result.scalars().all()
    entries_list = list(entries)
    return entries_list


@fixture
async def id_of_test_sched(seeded_db: AsyncSession) -> AsyncGenerator[int | None, None]:
    result = await seeded_db.execute(select(SupplementSchedule))
    test_sched = result.scalar_one_or_none()
    test_sched_id = getattr(test_sched, "id", None)
    print(test_sched_id)

    # This is testing the seeding, not the crud operations,
    # but it is justified because:
    #   1) it offers a quick diagnosis if seeding should fail
    #   2) the seeding is specific to this test file
    #      and this allows a quick verification that things are working.
    assert id_of_test_sched is not None

    yield test_sched_id


@fixture
async def dummy_sched_and_test_ingred_id(
    seeded_db: AsyncSession, id_of_test_sched: int
) -> AsyncGenerator[tuple[TimeSlots, int], None]:
    test_ingred_name = "L-Theanine"
    result = await seeded_db.execute(
        select(IngredientOrm).where(IngredientOrm.name == test_ingred_name)
    )
    test_ingred = result.scalar_one_or_none()

    # This is testing the seeding, not the crud operations,
    # but it is justified because:
    #   1) it offers a quick diagnosis if seeding should fail
    #   2) the seeding is specific to this test file
    #      and this allows a quick verification that things are working.
    assert test_ingred

    new_sched = TimeSlots(
        before_breakfast=[
            IngredientResponse(
                id=test_ingred.id,
                name=test_ingred_name,
                before_after_food=test_ingred.before_after_food,
            )
        ]
    )

    yield new_sched, test_ingred.id


def entries_from_schedule(
    sched_id: int, schedule: TimeSlots
) -> list[IngredientInSchedule]:
    entries_in_sched = []

    for slot in schedule.__dict__.items():
        for ingred in slot[1]:
            # fmt: off
            new_sched_entry = IngredientInSchedule(
                ingredient_id=ingred.id,
                schedule_id=sched_id,
                slot=slot[0]
            )
            # fmt: on

            entries_in_sched.append(new_sched_entry)

    return entries_in_sched


class TestUpdateSchedule:
    async def test_raises_for_not_found(
        self, seeded_db: AsyncSession, id_of_test_sched: int
    ) -> None:
        assert id_of_test_sched is not None
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
                    id=1000,
                    name="not in the database",
                    before_after_food=BeforeAfterFood.before,
                )
            ]
        )

        with raises(ResourceNotFound):
            await Schedule.update(
                sched_id=id_of_test_sched, updated_sched=new_sched, db=seeded_db
            )

    async def test_update_with_empty_clears_schedule(
        self, seeded_db: AsyncSession, id_of_test_sched: int
    ) -> None:
        new_sched = TimeSlots()
        await Schedule.update(
            sched_id=id_of_test_sched, updated_sched=new_sched, db=seeded_db
        )

        test_sched_entries = await get_test_schedule_entries_from_db(
            id=id_of_test_sched, db=seeded_db
        )

        assert len(test_sched_entries) == 0

    async def test_idempotent(
        self,
        id_of_test_sched: int,
        dummy_sched_and_test_ingred_id: tuple[TimeSlots, int],
        seeded_db: AsyncSession,
    ) -> None:
        results = []
        for _ in range(2):
            await Schedule.update(
                sched_id=id_of_test_sched,
                updated_sched=dummy_sched_and_test_ingred_id[0],
                db=seeded_db,
            )

            new_sched_in_db = await get_test_schedule_entries_from_db(
                id=id_of_test_sched, db=seeded_db
            )
            results.append(new_sched_in_db)

        assert all(
            first_time.id == second_time.id
            for first_time, second_time in zip(results[0], results[1])
        )

    async def test_updates_schedule_in_db(
        self,
        seeded_db: AsyncSession,
        dummy_sched_and_test_ingred_id: tuple[TimeSlots, int],
        id_of_test_sched: int,
    ) -> None:
        await Schedule.update(
            sched_id=id_of_test_sched,
            updated_sched=dummy_sched_and_test_ingred_id[0],
            db=seeded_db,
        )

        entries = await get_test_schedule_entries_from_db(
            id=id_of_test_sched, db=seeded_db
        )

        assert len(entries) == 1
        assert entries[0].ingredient_id == dummy_sched_and_test_ingred_id[1]
