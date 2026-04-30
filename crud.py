from models import TimeSlots, IngredientResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class Schedule:
    @staticmethod
    async def get(sched_id: int, db: AsyncSession) -> TimeSlots:
        query = """
        """

        query_result = await db.execute(text(query), {"id": sched_id})
        rows = query_result.mappings().all()
        schedule_slots = TimeSlots()

        for row in rows:
            ingredient = IngredientResponse(
                name=row["ingredient_name"], before_after_food=row["before_after_food"]
            )
            slot_name = row["slot"]
            slot_in_schedule = getattr(schedule_slots, slot_name)
            slot_in_schedule.append(ingredient)

        return schedule_slots
