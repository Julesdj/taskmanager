from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Create Async Engine
engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)

# Create session maker factory
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
