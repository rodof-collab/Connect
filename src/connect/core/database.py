from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from connect.core.config import settings

engine = create_async_engine(settings.database_url, pool_pre_ping=True)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    """Предок всех моделей: реестр всех таблиц живёт в Base.metadata."""


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Сессия для FastAPI (Depends) и middleware бота: открыл → отдал → закрыл."""
    async with AsyncSessionLocal() as session:
        yield session
