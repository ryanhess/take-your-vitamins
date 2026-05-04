from database import AsyncDb
from fastapi import FastAPI, HTTPException
from models import ScheduleRequest, SupplementPlanResponse, SupplementSchedule
from fastapi.middleware.cors import CORSMiddleware
import scheduler
from sqlalchemy import select
from crud import Schedule


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/")
async def make_viamin_schedule(
    supplement_data: ScheduleRequest, db: AsyncDb
) -> SupplementPlanResponse:
    if supplement_data == []:
        return SupplementPlanResponse()

    supplement_set = supplement_data.supplements
    response_schedule = await scheduler.create_schedule(supplement_set, db)

    return response_schedule


@app.get("/schedule/get")
async def get_schedule_handler(user_id: int, db: AsyncDb) -> SupplementPlanResponse:
    query = select(SupplementSchedule.id).where(SupplementSchedule.user_id == 1)
    result = await db.execute(query)
    schedule_id = result.scalar_one_or_none()
    if schedule_id is None:
        raise HTTPException(status_code=404, detail="Schedule not found for user")

    response_schedule = await Schedule.get(sched_id=schedule_id, db=db)
    response = SupplementPlanResponse(schedule=response_schedule)
    return response
