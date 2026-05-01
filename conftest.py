import pytest
from alembic.config import Config
from alembic import command
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from database import OrmBase
from config import env_vars


TEST_DB_URL = env_vars.TEST_DATABASE_URL


@pytest.fixture(scope="session")
async def engine():
    eng = create_async_engine(TEST_DB_URL)

    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", TEST_DB_URL)
    command.upgrade(alembic_cfg, "head")

    yield eng
    await eng.dispose()


@pytest.fixture
async def db(engine):
    async with engine.connect() as conn:
        await conn.begin()
        session = AsyncSession(bind=conn, join_transaction_mode="create_savepoint")
        yield session
        await conn.rollback()
