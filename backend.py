from fastapi import FastAPI, HTTPException
from models import IngredientAttributes, IngredientInRequest, SupplimentPlanResponse
import scheduler


app = FastAPI()


@app.post("/")
async def make_viamin_schedule(
    supplement_data: list[IngredientInRequest],
) -> SupplimentPlanResponse:
    if supplement_data == []:
        return SupplimentPlanResponse()

    response_schedule = scheduler.create_schedule(supplement_data)

    return response_schedule
