from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AssetBase(BaseModel):
    symbol: str
    name: str
    quantity: float
    average_buy_price: float
    asset_type: str
    asset_category: Optional[str] = 'stock-etf'  # stock-etf, cic, foundation, crypto, currency-metal, other
    currency: str = 'USD'
    remarks: Optional[str] = None
    purchase_date: datetime

class AssetCreate(AssetBase):
    pass

class AssetUpdate(BaseModel):
    symbol: Optional[str] = None
    name: Optional[str] = None
    quantity: Optional[float] = None
    average_buy_price: Optional[float] = None
    asset_type: Optional[str] = None
    asset_category: Optional[str] = None
    currency: Optional[str] = None
    remarks: Optional[str] = None
    purchase_date: Optional[datetime] = None

class AssetResponse(AssetBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    current_value: Optional[float] = None
    profit_loss: Optional[float] = None
    profit_loss_percentage: Optional[float] = None

    class Config:
        from_attributes = True
