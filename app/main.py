from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import tasks, users
from app.db.deps import get_db


def create_app() -> FastAPI:
    app = FastAPI(title="Task Manager API")

    @app.get("/healthcheck")
    async def healthcheck(db: AsyncSession = Depends(get_db)):
        result = await db.execute(text("SELECT 1"))
        return {"db_status": "ok" if result.scalar() == 1 else "fail"}

    app.include_router(tasks.router)
    app.include_router(users.router)
    return app


app = create_app()
