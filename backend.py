from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class SupplimentInPlan(BaseModel):
    name: str


class SupplimentPlanResponse(BaseModel):
    before_breakfast: list[SupplimentInPlan] = []
    after_breakfast: list[SupplimentInPlan] = []
    before_lunch: list[SupplimentInPlan] = []
    after_lunch: list[SupplimentInPlan] = []
    before_dinner: list[SupplimentInPlan] = []
    after_dinner: list[SupplimentInPlan] = []


@app.post("/")
async def make_viamin_schedule(
    suppliment_data: list[SupplimentInPlan],
) -> SupplimentPlanResponse:
    if suppliment_data == []:
        return SupplimentPlanResponse()

    print(suppliment_data)

    response_schedule = SupplimentPlanResponse(
        before_breakfast=[
            SupplimentInPlan(name="Vitamin B12"),
            SupplimentInPlan(name="Mugwort"),
        ],
        after_breakfast=[SupplimentInPlan(name="Vitamin C")],
        before_lunch=[
            SupplimentInPlan(name="Alpha-lipoic acid"),
            SupplimentInPlan(name="Mugwort"),
            SupplimentInPlan(name="Apple Cider Vinegar"),
        ],
        after_lunch=[SupplimentInPlan(name="Omega-3")],
        before_dinner=[SupplimentInPlan(name="B3")],
        after_dinner=[
            SupplimentInPlan(name="Mugwort"),
            SupplimentInPlan(name="Lion's Mane"),
        ],
    )

    return response_schedule
