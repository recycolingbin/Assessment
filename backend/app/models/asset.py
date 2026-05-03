from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    symbol = Column(String, nullable=False, index=True)  # e.g., AAPL, BTC
    name = Column(String, nullable=False)  # e.g., Apple Inc., Bitcoin
    quantity = Column(Float, nullable=False, default=0.0)
    average_buy_price = Column(Float, nullable=False)  # Average purchase price
    asset_type = Column(String, nullable=False)  # stock, etf, crypto, bond, etc.
    asset_category = Column(String, nullable=False, default='stock-etf')  # stock-etf, cic, foundation, crypto, currency-metal, other
    currency = Column(String, nullable=False, default='USD')  # USD, EUR, GBP, JPY, CAD, AUD, HKD, CNY
    remarks = Column(Text, nullable=True)  # User notes/remarks
    purchase_date = Column(DateTime, nullable=False)  # When the asset was purchased
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    owner = relationship("User", back_populates="assets")
    transactions = relationship("Transaction", back_populates="asset", cascade="all, delete-orphan")
