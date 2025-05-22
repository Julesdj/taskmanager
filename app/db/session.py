from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.config import settings

# Async Engine
engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)

# Async SessionMaker
async_session = async_sessionmaker(engine, expire_on_commit=False)
