from models import TimeSlots, IngredientResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class Schedule:
    @staticmethod
    async def get(sched_id: int, db: AsyncSession) -> TimeSlots:
        query = """
            WITH schedule_entries AS (
                SELECT
                    s.id as schedule_id,
                    i.name as ingredient_name,
                    i.before_after_food as before_after_food,
                    iis.slot as slot
                FROM schedules s
                JOIN ingredients_in_schedule iis ON s.id = iis.schedule_id
                JOIN ingredients i ON i.id = iis.ingredient_id
            )
            SELECT ingredient_name, before_after_food, slot
            FROM schedule_entries
            WHERE schedule_id = :id
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
