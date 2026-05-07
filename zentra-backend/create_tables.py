"""
Utility script to create database tables based on SQLAlchemy models.
Run this script to sync your database schema with your models.
"""
import asyncio
from app.db.database import engine, Base
from app.db import models  # Import models to register them


async def create_tables():
    """Create all database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Tables created successfully")
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(create_tables())
