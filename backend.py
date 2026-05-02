from database import AsyncDb
from fastapi import FastAPI
from models import ScheduleRequest, SupplementPlanResponse
from fastapi.middleware.cors import CORSMiddleware
import scheduler


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
