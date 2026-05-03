from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List
from datetime import datetime

from app.database import get_db
from app.models.user import User
from app.models.asset import Asset
from app.models.transaction import Transaction, TransactionType
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.auth import get_current_user
from app.redis_client import delete_cache

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verify asset belongs to user
    asset = db.query(Asset).filter(
        Asset.id == transaction.asset_id,
        Asset.user_id == current_user.id
    ).first()

    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    # Calculate total amount
    total_amount = transaction.quantity * transaction.price_per_unit

    # Create transaction with custom date if provided
    new_transaction = Transaction(
        user_id=current_user.id,
        asset_id=transaction.asset_id,
        transaction_type=transaction.transaction_type,
        quantity=transaction.quantity,
        price_per_unit=transaction.price_per_unit,
        total_amount=total_amount,
        transaction_date=transaction.transaction_date if transaction.transaction_date else datetime.utcnow(),
        notes=transaction.notes
    )
    db.add(new_transaction)

    # Update asset quantity and average buy price
    if transaction.transaction_type == TransactionType.BUY:
        # Calculate new average buy price
        total_cost = (asset.quantity * asset.average_buy_price) + total_amount
        new_quantity = asset.quantity + transaction.quantity
        asset.average_buy_price = total_cost / new_quantity if new_quantity > 0 else 0
        asset.quantity = new_quantity
    elif transaction.transaction_type == TransactionType.SELL:
        if asset.quantity < transaction.quantity:
            raise HTTPException(status_code=400, detail="Insufficient asset quantity")
        asset.quantity -= transaction.quantity

    db.commit()
    db.refresh(new_transaction)

    # Invalidate cache
    delete_cache(f"portfolio:{current_user.id}")

    return new_transaction

@router.get("/", response_model=List[TransactionResponse])
def get_transactions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    transactions = db.query(Transaction).options(joinedload(Transaction.asset)).filter(
        Transaction.user_id == current_user.id
    ).order_by(Transaction.transaction_date.desc()).offset(skip).limit(limit).all()
    return transactions

@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    transaction = db.query(Transaction).options(joinedload(Transaction.asset)).filter(
        Transaction.id == transaction_id,
        Transaction.user_id == current_user.id
    ).first()

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return transaction
