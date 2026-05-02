from models import (
    IngredientInSchedule,
    SupplementSchedule,
    TimeSlots,
)
from sqlalchemy import text, delete
from sqlalchemy.ext.asyncio import AsyncSession


class Schedule:
    @staticmethod
    async def get(sched_id: int, db: AsyncSession) -> TimeSlots:
        return TimeSlots()

    @staticmethod
    async def update(sched_id: int, updated_sched: TimeSlots, db: AsyncSession) -> None:
        sched = await db.get(SupplementSchedule, sched_id)

        if sched is None:
            return None

        ingreds_in_new_sched = []

        for slot in updated_sched.__dict__.items():
            for ingred in slot[1]:
                # fmt: off
                new_sched_entry = IngredientInSchedule(
                    ingredient_id=ingred.id,
                    schedule_id=sched_id,
                    slot=slot[0]
                )
                # fmt: on

                ingreds_in_new_sched.append(new_sched_entry)

        del_stmt = delete(IngredientInSchedule).where(
            IngredientInSchedule.schedule_id == sched_id
        )
        await db.execute(del_stmt)
        db.add_all(ingreds_in_new_sched)
        await db.commit()
