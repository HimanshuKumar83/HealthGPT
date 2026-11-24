from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.config import settings #type: ignore

# Ensure the database URL uses the async driver (psycopg for PostgreSQL, aiosqlite for SQLite)
raw_url = str(settings.DATABASE_URL)
if raw_url.startswith("postgres://"):
    DATABASE_URL = raw_url.replace("postgres://", "postgresql+psycopg://", 1)
elif raw_url.startswith("postgresql://") and not raw_url.startswith("postgresql+psycopg://"):
    DATABASE_URL = raw_url.replace("postgresql://", "postgresql+psycopg://", 1)
elif raw_url.startswith("sqlite://") and not raw_url.startswith("sqlite+aiosqlite://"):
    DATABASE_URL = raw_url.replace("sqlite://", "sqlite+aiosqlite://", 1)
else:
    DATABASE_URL = raw_url


engine = create_async_engine(
    DATABASE_URL,
    echo=False if settings.ENVIRONMENT == "production" else True,
    future=True
)


AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)


Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

