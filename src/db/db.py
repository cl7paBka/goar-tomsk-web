from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from src.utils.config import settings
import logging

# Database configuration for connection
DATABASE_URL = f"postgresql+asyncpg://{settings.db.DB_USER}:{settings.db.DB_PASSWORD}@{settings.db.DB_HOST}:{settings.db.DB_PORT}/{settings.db.DB_NAME}"

# Async engine for PostgreSQL
engine = create_async_engine(DATABASE_URL)

# Async sessions
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


# Base class for models in src/models/models.py
class Base(DeclarativeBase):
    pass


# Database initialization and table creating
async def init_db():
    async with engine.begin() as conn:
        logging.info("Creating tables POSTGRESQL!")
        await conn.run_sync(Base.metadata.create_all)
    logging.info("Tables created!")


# Async sessions generator
async def get_async_session():
    async with async_session_maker() as session:
        yield session
