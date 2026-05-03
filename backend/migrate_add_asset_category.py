"""
Database migration script to add asset_category column to assets table.
Run this script to update your existing database schema.
"""

import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from app.database import engine

def migrate_database():
    """Add asset_category column to the assets table"""

    print("Starting database migration: Adding asset_category column...")

    # SQL statements to add new columns
    migrations = [
        "ALTER TABLE assets ADD COLUMN IF NOT EXISTS asset_category VARCHAR DEFAULT 'stock-etf';",
    ]

    try:
        with engine.connect() as connection:
            for migration in migrations:
                print(f"Executing: {migration}")
                connection.execute(text(migration))
                connection.commit()

        print("✓ Database migration completed successfully!")
        return True

    except Exception as e:
        print(f"✗ Error during migration: {str(e)}")
        return False

if __name__ == "__main__":
    success = migrate_database()
    sys.exit(0 if success else 1)

