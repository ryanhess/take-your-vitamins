from database import AsyncDb
from fastapi import FastAPI
from models import IngredientInRequest, SupplementPlanResponse
import scheduler


app = FastAPI()


@app.post("/")
async def make_viamin_schedule(
    supplement_data: list[IngredientInRequest], db: AsyncDb
) -> SupplementPlanResponse:
    if supplement_data == []:
        return SupplementPlanResponse()

    response_schedule = await scheduler.create_schedule(supplement_data, db)

    return response_schedule
