"""
Script to drop all existing tables and recreate them with UUID.
This is a clean slate approach for migrating from Integer to UUID IDs.
"""
import asyncio
import sys

# Fix for Windows async event loop
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from app.db.database import engine, Base
from app.db import models  # Import all models


async def recreate_tables():
    """Drop all tables and recreate them with UUID schema."""
    print("🔄 Dropping all existing tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    print("✅ All tables dropped successfully!")
    
    print("\n🔄 Creating new tables with UUID schema...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ All tables created successfully with UUID!")
    
    print("\n🎉 Database migration complete!")
    print("All tables now use UUID for primary keys and foreign keys.")


if __name__ == "__main__":
    print("=" * 60)
    print("DATABASE RECREATION SCRIPT")
    print("=" * 60)
    print("\n⚠️  WARNING: This will DELETE ALL existing data!")
    print("All tables will be dropped and recreated with UUID schema.\n")
    
    # response = input("Are you sure you want to continue? (yes/no): ")
    
    # if response.lower() == 'yes':
    #     asyncio.run(recreate_tables())
    # else:
    #     print("\n❌ Operation cancelled.")
    #     sys.exit(0)
    asyncio.run(recreate_tables())
