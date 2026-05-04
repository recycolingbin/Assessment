#!/usr/bin/env python3
"""Migration: Add realized_gain_loss column to transactions table"""

import os
import sys
from sqlalchemy import create_engine, text

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/portfolio")

def run_migration():
    """Run the migration"""
    engine = create_engine(DATABASE_URL)
    
    try:
        with engine.connect() as connection:
            # Start transaction
            trans = connection.begin()
            try:
                print("Starting database migration...")
                
                # Add realized_gain_loss column if it doesn't exist
                migration_sql = """
                ALTER TABLE transactions 
                ADD COLUMN IF NOT EXISTS realized_gain_loss FLOAT DEFAULT 0.0;
                """
                
                print(f"Executing: {migration_sql.strip()}")
                connection.execute(text(migration_sql))
                print("✓ Success")
                
                trans.commit()
                print("\n✅ Database migration completed successfully!")
                
            except Exception as e:
                trans.rollback()
                print(f"❌ Error during migration: {e}")
                sys.exit(1)
                
    except Exception as e:
        print(f"❌ Failed to connect to database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_migration()
