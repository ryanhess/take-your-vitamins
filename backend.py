from fastapi import FastAPI
from models import IngredientInRequest, SupplementPlanResponse
import scheduler


app = FastAPI()


@app.post("/")
async def make_viamin_schedule(
    supplement_data: list[IngredientInRequest],
) -> SupplementPlanResponse:
    if supplement_data == []:
        return SupplementPlanResponse()

    response_schedule = scheduler.create_schedule(supplement_data)

    return response_schedule
