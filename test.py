import asyncio
from database import async_session
from models import IngredientOrm
from sqlalchemy import select


async def main():
    async with async_session() as session:
        result = await session.execute(select(IngredientOrm))
        ingredients = result.scalars().all()

        for ing in ingredients:
            conflicts = await ing.take_not_with()
            print(f"{ing.name} (id={ing.id}): conflicts={conflicts}")


asyncio.run(main())
