"""
Migration script to add remarks and purchase_date columns to assets table
"""
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def migrate():
    with engine.connect() as conn:
        # Add remarks column to assets table
        try:
            conn.execute(text("ALTER TABLE assets ADD COLUMN remarks TEXT"))
            print("✓ Added remarks column to assets table")
        except Exception as e:
            print(f"Note: remarks column might already exist - {e}")

        # Add purchase_date column to assets table
        try:
            conn.execute(text("ALTER TABLE assets ADD COLUMN purchase_date TIMESTAMP"))
            print("✓ Added purchase_date column to assets table")
        except Exception as e:
            print(f"Note: purchase_date column might already exist - {e}")

        conn.commit()
        print("\n✓ Migration completed successfully!")

if __name__ == "__main__":
    migrate()
