from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user import User
from app.models.asset import Asset
from app.schemas.asset import AssetCreate, AssetUpdate, AssetResponse
from app.auth import get_current_user
from app.redis_client import invalidate_user_caches
from app.utils.stock_data import auto_fill_asset

router = APIRouter(prefix="/assets", tags=["Assets"])

@router.post("/", response_model=AssetResponse, status_code=status.HTTP_201_CREATED)
def create_asset(
    asset: AssetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if asset already exists for this user
    existing_asset = db.query(Asset).filter(
        Asset.user_id == current_user.id,
        Asset.symbol == asset.symbol
    ).first()

    if existing_asset:
        # Combine with existing asset - calculate new average price
        total_cost = (existing_asset.quantity * existing_asset.average_buy_price) + (asset.quantity * asset.average_buy_price)
        new_quantity = existing_asset.quantity + asset.quantity
        existing_asset.average_buy_price = total_cost / new_quantity if new_quantity > 0 else 0
        existing_asset.quantity = new_quantity

        # Update other fields if provided
        if asset.remarks:
            existing_asset.remarks = asset.remarks

        db.commit()
        db.refresh(existing_asset)

        # Invalidate cache
        invalidate_user_caches(current_user.id)

        return existing_asset

    new_asset = Asset(
        user_id=current_user.id,
        symbol=asset.symbol,
        name=asset.name,
        quantity=asset.quantity,
        average_buy_price=asset.average_buy_price,
        asset_type=asset.asset_type,
        asset_category=asset.asset_category or 'stock-etf',
        currency=asset.currency,
        remarks=asset.remarks,
        purchase_date=asset.purchase_date
    )
    db.add(new_asset)
    db.commit()
    db.refresh(new_asset)

    # Invalidate cache
    invalidate_user_caches(current_user.id)

    return new_asset

@router.get("/", response_model=List[AssetResponse])
def get_assets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    assets = db.query(Asset).filter(Asset.user_id == current_user.id).all()
    return assets

@router.get("/{asset_id}", response_model=AssetResponse)
def get_asset(
    asset_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    asset = db.query(Asset).filter(
        Asset.id == asset_id,
        Asset.user_id == current_user.id
    ).first()

    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    return asset

@router.put("/{asset_id}", response_model=AssetResponse)
def update_asset(
    asset_id: int,
    asset_update: AssetUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    asset = db.query(Asset).filter(
        Asset.id == asset_id,
        Asset.user_id == current_user.id
    ).first()

    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    update_data = asset_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(asset, key, value)

    db.commit()
    db.refresh(asset)

    # Invalidate cache
    invalidate_user_caches(current_user.id)

    return asset

@router.delete("/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_asset(
    asset_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    asset = db.query(Asset).filter(
        Asset.id == asset_id,
        Asset.user_id == current_user.id
    ).first()

    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    db.delete(asset)
    db.commit()

    # Invalidate cache
    invalidate_user_caches(current_user.id)

    return None

@router.get("/auto-fill/{symbol}")
def get_auto_fill_data(symbol: str = Path(..., min_length=1, description="Asset symbol")):
    """Get auto-fill data for an asset symbol"""
    data = auto_fill_asset(symbol)
    if not data:
        raise HTTPException(status_code=404, detail=f"No data found for symbol: {symbol}")
    return data
