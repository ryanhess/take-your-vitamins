from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Literal

app = FastAPI()


class IngredientInternal(BaseModel):
    name: str
    take_not_with: list["IngredientInternal"] = []
    before_after_food: Literal["before", "after"]


class IngredientInPlanRequest(BaseModel):
    name: str


class SupplimentPlanResponse(BaseModel):
    before_breakfast: list[IngredientInPlanRequest] = []
    after_breakfast: list[IngredientInPlanRequest] = []
    before_lunch: list[IngredientInPlanRequest] = []
    after_lunch: list[IngredientInPlanRequest] = []
    before_dinner: list[IngredientInPlanRequest] = []
    after_dinner: list[IngredientInPlanRequest] = []


@app.post("/")
async def make_viamin_schedule(
    suppliment_data: list[IngredientInPlanRequest],
) -> SupplimentPlanResponse:
    if suppliment_data == []:
        return SupplimentPlanResponse()

    print(suppliment_data)

    response_schedule = SupplimentPlanResponse(
        before_breakfast=[
            IngredientInPlanRequest(name="Vitamin B12"),
            IngredientInPlanRequest(name="Mugwort"),
        ],
        after_breakfast=[IngredientInPlanRequest(name="Vitamin C")],
        before_lunch=[
            IngredientInPlanRequest(name="Alpha-lipoic acid"),
            IngredientInPlanRequest(name="Mugwort"),
            IngredientInPlanRequest(name="Apple Cider Vinegar"),
        ],
        after_lunch=[IngredientInPlanRequest(name="Omega-3")],
        before_dinner=[IngredientInPlanRequest(name="B3")],
        after_dinner=[
            IngredientInPlanRequest(name="Mugwort"),
            IngredientInPlanRequest(name="Lion's Mane"),
        ],
    )

    return response_schedule
