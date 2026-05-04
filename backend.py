from database import AsyncDb
from fastapi import FastAPI, HTTPException
from exceptions import ResourceNotFound
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


async def _get_schedule_id_for_user_or_error(user_id: int, db: AsyncDb) -> int:
    query = select(SupplementSchedule.id).where(SupplementSchedule.user_id == 1)
    result = await db.execute(query)
    schedule_id = result.scalar_one_or_none()
    if schedule_id is None:
        raise ResourceNotFound(resource_type=SupplementSchedule, resource_ids=user_id)

    return schedule_id


@app.post("/")
async def make_viamin_schedule(
    supplement_data: ScheduleRequest, db: AsyncDb
) -> SupplementPlanResponse:
    if supplement_data == []:
        return SupplementPlanResponse()

    supplement_set = supplement_data.supplements
    response_schedule = await scheduler.create_schedule(supplement_set, db)

    return response_schedule


@app.get("/schedule/{user_id}/get")
async def get_schedule(user_id: int, db: AsyncDb) -> SupplementPlanResponse:
    schedule_id = await _get_schedule_id_for_user_or_error(user_id=user_id, db=db)
    response_schedule = await Schedule.get(sched_id=schedule_id, db=db)
    response = SupplementPlanResponse(schedule=response_schedule)
    return response


@app.put(
    "/schedule/{user_id}/update",
    status_code=204,
    responses={
        404: {"description": "Schedule not found OR Ingredient in schedule not found."},
        422: {"description": "Validation error"},
    },
)
async def update_schedule(
    user_id: int, updated_schedule: SupplementPlanResponse, db: AsyncDb
) -> None:
    """
    Replaces the schedule for the user with an updated one. Returns 204 on successful update.
    """

    sched_id = await _get_schedule_id_for_user_or_error(user_id=user_id, db=db)
    new_sched = updated_schedule.schedule
    await Schedule.update(sched_id=sched_id, updated_sched=new_sched, db=db)
