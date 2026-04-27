from database import AsyncDb
from fastapi import FastAPI
from models import IngredientInRequest, SupplementPlanResponse
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
    supplement_data: list[IngredientInRequest], db: AsyncDb
) -> SupplementPlanResponse:
    if supplement_data == []:
        return SupplementPlanResponse()

    response_schedule = await scheduler.create_schedule(supplement_data, db)

    return response_schedule
