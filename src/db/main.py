from sqlmodel import SQLModel, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config import Config

database_url = Config.DATABASE_URL

# create async engine
async_engine = AsyncEngine(create_engine(
    url=database_url,
    echo=True,
    future=True
))

# initialize db
async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

# get session
async def get_session() -> AsyncSession: # type: ignore
    async_session = sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    async with async_session() as session:
        yield session
    