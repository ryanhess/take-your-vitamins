from database import AsyncDb
from fastapi import FastAPI
from models import IngredientInRequest, SupplementPlanResponse
from models import TestOrm
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


@app.get("/test-orm", response_model=None)
async def add_test_orm(name: str, age: int, db: AsyncDb) -> TestOrm:
    new_test = TestOrm(name=name, age=age)
    db.add(new_test)
    await db.flush()
    await db.commit()
    return new_test