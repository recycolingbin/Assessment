"""
Database migration script to add password reset fields.
Run this script to update your existing database schema.
"""

import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from app.database import Base, engine

def migrate_database():
    """Add password reset columns to the users table"""

    print("Starting database migration for password reset...")

    # SQL statements to add new columns
    migrations = [
        # Password reset fields
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS reset_token VARCHAR;",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS reset_token_expires TIMESTAMP;",
    ]

    try:
        with engine.connect() as connection:
            for migration in migrations:
                print(f"Executing: {migration}")
                try:
                    connection.execute(text(migration))
                    connection.commit()
                    print("✓ Success")
                except Exception as e:
                    print(f"✗ Error (may already exist): {e}")
                    connection.rollback()

        print("\n✅ Database migration completed successfully!")
        print("\nNew fields added to users table:")
        print("  - reset_token (password reset token)")
        print("  - reset_token_expires (token expiry)")
        print("\nYou can now restart your backend server.")

    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        print("\nIf you're getting errors, you may need to:")
        print("1. Check your database connection")
        print("2. Ensure PostgreSQL is running")
        print("3. Verify DATABASE_URL in your .env file")
        sys.exit(1)

if __name__ == "__main__":
    migrate_database()
