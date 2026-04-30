from models import TimeSlots


class Schedule:
    @staticmethod
    async def get(userid: int) -> TimeSlots:
        return TimeSlots()
