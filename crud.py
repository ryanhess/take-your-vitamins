from models import TimeSlots
from sqlalchemy.ext.asyncio import AsyncSession


class Schedule:
    @staticmethod
    async def get(sched_id: int, db: AsyncSession) -> TimeSlots:
        return TimeSlots()

    @staticmethod
    async def update(sched_id: int, updated_sched: TimeSlots, db: AsyncSession) -> None:
        return None
