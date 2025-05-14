from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db


def create_app() -> FastAPI:
    app = FastAPI(title="Task manager APi")

    @app.get("/healthcheck")
    async def healthcheck(db: AsyncSession = Depends(get_db)):
        # Simple DB connection test
        result = await db.execute(text("SELECT 1"))
        return {"db_staus": result.scalar()}

    return app


app = create_app()
