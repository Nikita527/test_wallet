import asyncio
from logging.config import fileConfig

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import pool
from alembic import context

from app.core.config import settings
from app.models.base import Base
import app.models  # noqa: F401

# Настраиваем логирование из файла alembic.ini, если есть.
if context.config.config_file_name is not None:
    fileConfig(context.config.config_file_name)

# Устанавливаем URL подключения
config = context.config
config.set_main_option("sqlalchemy.url", settings.database_url)

# Это metadata, содержащая все модели
target_metadata = Base.metadata


def do_run_migrations(connection) -> None:
    # Здесь используем синхронный объект подключения для конфигурации миграций.
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    # Создаём асинхронный движок.
    engine = create_async_engine(
        settings.database_url, poolclass=pool.NullPool
    )
    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await engine.dispose()


if context.is_offline_mode():
    # Offline-режим работает синхронно.
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()
else:
    # В онлайн-режиме запускаем асинхронные миграции, используя asyncio.run()
    asyncio.run(run_async_migrations())
