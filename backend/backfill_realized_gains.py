"""
Backfill realized_gain_loss for existing sell transactions
This script recalculates realized gains/losses for all sell transactions
based on the current average_buy_price of their associated assets.
"""

import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models.transaction import Transaction, TransactionType
from app.models.asset import Asset

def backfill_realized_gains():
    db = SessionLocal()
    try:
        # Get all sell transactions
        sell_transactions = db.query(Transaction).filter(
            Transaction.transaction_type == TransactionType.SELL
        ).all()

        print(f"Found {len(sell_transactions)} sell transactions to process")

        updated_count = 0
        for txn in sell_transactions:
            # Get the associated asset
            asset = db.query(Asset).filter(Asset.id == txn.asset_id).first()

            if not asset:
                print(f"Warning: Asset {txn.asset_id} not found for transaction {txn.id}")
                continue

            # Calculate realized gain/loss
            # Formula: (sell_price - average_buy_price) * quantity
            calculated_gain = (txn.price_per_unit - asset.average_buy_price) * txn.quantity

            # Update if different from current value
            if txn.realized_gain_loss != calculated_gain:
                old_value = txn.realized_gain_loss
                txn.realized_gain_loss = calculated_gain
                updated_count += 1
                print(f"Transaction {txn.id} (Asset: {asset.symbol}): {old_value} -> {calculated_gain}")

        # Commit all changes
        db.commit()
        print(f"\nSuccessfully updated {updated_count} transactions")

    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("Starting backfill of realized_gain_loss values...")
    backfill_realized_gains()
    print("Backfill complete!")
