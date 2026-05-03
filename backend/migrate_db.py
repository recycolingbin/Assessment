"""
Database migration script to add new fields for email verification, OAuth, and profile features.
Run this script to update your existing database schema.
"""

import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from app.database import Base, engine
from app.models.user import User

def migrate_database():
    """Add new columns to the users table"""

    print("Starting database migration...")

    # SQL statements to add new columns
    migrations = [
        # Email verification fields
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS is_verified BOOLEAN DEFAULT FALSE;",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS verification_token VARCHAR;",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS verification_token_expires TIMESTAMP;",

        # OAuth fields
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS google_id VARCHAR UNIQUE;",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS oauth_provider VARCHAR;",

        # Profile fields
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS full_name VARCHAR;",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS phone VARCHAR;",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS avatar_url VARCHAR;",

        # WebAuthn/Passkey fields
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS webauthn_credentials TEXT;",

        # Make hashed_password nullable for OAuth users
        "ALTER TABLE users ALTER COLUMN hashed_password DROP NOT NULL;",

        # Create index on google_id
        "CREATE INDEX IF NOT EXISTS idx_users_google_id ON users(google_id);",
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
        print("  - is_verified (email verification status)")
        print("  - verification_token (email verification token)")
        print("  - verification_token_expires (token expiry)")
        print("  - google_id (Google OAuth ID)")
        print("  - oauth_provider (OAuth provider name)")
        print("  - full_name (user's full name)")
        print("  - phone (user's phone number)")
        print("  - avatar_url (profile picture URL)")
        print("  - webauthn_credentials (passkey credentials)")
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
