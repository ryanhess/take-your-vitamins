from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from collections.abc import AsyncGenerator
from config import env_vars
from fastapi import Depends
from typing import Annotated

database_url = env_vars.DATABASE_URL

engine = create_async_engine(database_url)
async_session = async_sessionmaker(engine, expire_on_commit=False)


class OrmBase(DeclarativeBase):
    pass


async def _get_db() -> AsyncGenerator[AsyncSession]:
    async with async_session() as session:
        yield session


AsyncDb = Annotated[AsyncSession, Depends(_get_db)]
