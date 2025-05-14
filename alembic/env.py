import asyncio
import os
import sys
from logging.config import fileConfig

from dotenv import load_dotenv

from alembic import context
from app.core.config import settings
from app.db.session import engine  # Async engine
from app.models.base import Base
from app.models.task import Task  # noqa

# Add app to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Load env vars
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

# Alembic config setup
config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

if config.config_file_name:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

# Debug output (optional)
print(f"Connecting to DB URL: {config.get_main_option('sqlalchemy.url')}")
print(f"Tables in Base.metadata: {Base.metadata.tables.keys()}")


def run_migrations_online() -> None:
    """Run migrations in 'online' mode using async SQLAlchemy engine."""

    async def do_run_migrations():
        async with engine.connect() as connection:
            # THIS IS THE KEY
            async with connection.begin():
                await connection.run_sync(setup_context_and_run_migrations)

    def setup_context_and_run_migrations(sync_connection):
        context.configure(
            connection=sync_connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
            dialect_opts={"paramstyle": "named"},
        )
        context.run_migrations()

    asyncio.run(do_run_migrations())


run_migrations_online()
