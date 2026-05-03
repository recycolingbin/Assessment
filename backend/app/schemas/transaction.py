from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.transaction import TransactionType

class TransactionBase(BaseModel):
    asset_id: int
    transaction_type: TransactionType
    quantity: float
    price_per_unit: float
    notes: Optional[str] = None
    transaction_date: datetime

class TransactionCreate(TransactionBase):
    pass

class AssetSummary(BaseModel):
    id: int
    symbol: str
    name: str
    asset_type: str

    class Config:
        from_attributes = True

class TransactionResponse(TransactionBase):
    id: int
    user_id: int
    total_amount: float
    transaction_date: datetime
    asset: Optional[AssetSummary] = None

    class Config:
        from_attributes = True

class PortfolioOverview(BaseModel):
    total_value: float
    total_invested: float
    total_profit_loss: float
    total_profit_loss_percentage: float
    assets_count: int
    assets: list
