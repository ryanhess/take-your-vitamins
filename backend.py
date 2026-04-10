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
    print(suppliment_data)
    raise HTTPException(status_code=500, detail="test error response")
