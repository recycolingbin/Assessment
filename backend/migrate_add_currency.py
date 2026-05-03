"""
Migration script to add currency column to assets table
"""
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def migrate():
    with engine.connect() as conn:
        # Add currency column to assets table
        try:
            conn.execute(text("ALTER TABLE assets ADD COLUMN currency VARCHAR DEFAULT 'USD'"))
            print("✓ Added currency column to assets table")
        except Exception as e:
            print(f"Note: currency column might already exist - {e}")

        # Update existing records to have USD as default currency
        try:
            conn.execute(text("UPDATE assets SET currency = 'USD' WHERE currency IS NULL"))
            print("✓ Updated existing assets with default USD currency")
        except Exception as e:
            print(f"Note: Could not update existing records - {e}")

        conn.commit()
        print("\n✓ Migration completed successfully!")

if __name__ == "__main__":
    migrate()
