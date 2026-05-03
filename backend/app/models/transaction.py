from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import enum

class TransactionType(str, enum.Enum):
    BUY = "buy"
    SELL = "sell"

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    quantity = Column(Float, nullable=False)
    price_per_unit = Column(Float, nullable=False)
    total_amount = Column(Float, nullable=False)  # quantity * price_per_unit
    transaction_date = Column(DateTime, nullable=False)  # Required manual timestamp
    notes = Column(Text, nullable=True)

    # Relationships
    user = relationship("User", back_populates="transactions")
    asset = relationship("Asset", back_populates="transactions")
