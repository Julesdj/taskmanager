from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Async Engine
engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)

# Async SessionMaker
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
