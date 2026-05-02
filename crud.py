from exceptions import ResourceNotFound
from models import (
    IngredientInSchedule,
    IngredientOrm,
    SupplementSchedule,
    TimeSlots,
)
from sqlalchemy import text, select, delete
from sqlalchemy.ext.asyncio import AsyncSession


def _ingreds_from_time_slots(
    sched_id: int, slots: TimeSlots
) -> list[IngredientInSchedule]:
    ingredients = []
    for slot in slots.__dict__.items():
        for ingred in slot[1]:
            # fmt: off
            new_sched_entry = IngredientInSchedule(
                ingredient_id=ingred.id,
                schedule_id=sched_id,
                slot=slot[0]
            )
            # fmt: on

            ingredients.append(new_sched_entry)

    return ingredients


def _ingred_id_set_from_ingreds(ingreds: list[IngredientInSchedule]) -> set[int]:
    return set()


class Schedule:
    @staticmethod
    async def get(sched_id: int, db: AsyncSession) -> TimeSlots:
        return TimeSlots()

    @staticmethod
    async def update(sched_id: int, updated_sched: TimeSlots, db: AsyncSession) -> None:
        sched = await db.get(SupplementSchedule, sched_id)

        if sched is None:
            raise ResourceNotFound(
                resource_type=SupplementSchedule, resource_ids=sched_id
            )

        ingreds_in_new_sched = _ingreds_from_time_slots(
            sched_id=sched_id, slots=updated_sched
        )

        ingred_ids_in_req = _ingred_id_set_from_ingreds(ingreds_in_new_sched)
        query = select(IngredientOrm.id).where(IngredientOrm.id.in_(ingred_ids_in_req))

        result = await db.execute(query)
        ingred_ids_in_db = set(result.scalars().all())
        # ingred_ids_in_db = set()
        if len(ingred_ids_in_req) != len(ingred_ids_in_db):
            ingreds_not_found = ingred_ids_in_req - ingred_ids_in_db
            raise ResourceNotFound(IngredientOrm, list(ingreds_not_found))

        del_stmt = delete(IngredientInSchedule).where(
            IngredientInSchedule.schedule_id == sched_id
        )
        await db.execute(del_stmt)

        db.add_all(ingreds_in_new_sched)
        await db.commit()
