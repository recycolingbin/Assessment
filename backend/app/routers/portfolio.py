from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from typing import List, Dict

from app.database import get_db
from app.models.user import User
from app.models.asset import Asset
from app.models.transaction import Transaction, TransactionType
from app.schemas.transaction import PortfolioOverview
from app.auth import get_current_user
from app.redis_client import get_cache, set_cache
from app.utils.stock_search import search_stocks

router = APIRouter(prefix="/portfolio", tags=["Portfolio"])

@router.get("/overview", response_model=PortfolioOverview)
def get_portfolio_overview(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check cache first
    cache_key = f"portfolio:{current_user.id}"
    cached_data = get_cache(cache_key)
    if cached_data:
        return cached_data

    # Get all user assets
    assets = db.query(Asset).filter(Asset.user_id == current_user.id).all()

    total_invested = 0
    assets_data = []

    for asset in assets:
        invested_value = asset.quantity * asset.average_buy_price
        total_invested += invested_value

        assets_data.append({
            "id": asset.id,
            "symbol": asset.symbol,
            "name": asset.name,
            "quantity": asset.quantity,
            "average_buy_price": asset.average_buy_price,
            "invested_value": invested_value,
            "asset_type": asset.asset_type
        })

    result = {
        "total_invested": total_invested,
        "assets_count": len(assets),
        "assets": assets_data
    }

    # Cache the result for 5 minutes
    set_cache(cache_key, result, ttl=300)

    return result

@router.get("/performance-history")
def get_performance_history(
    days: int = 30,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get historical performance data for line chart"""
    # Check cache first
    cache_key = f"performance:{current_user.id}:{days}"
    cached_data = get_cache(cache_key)
    if cached_data:
        return cached_data

    # Get all user assets
    assets = db.query(Asset).filter(Asset.user_id == current_user.id).all()

    if not assets:
        return {"dates": [], "assets": []}

    # Generate date range
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    date_range = []
    current = start_date
    while current <= end_date:
        date_range.append(current.strftime("%Y-%m-%d"))
        current += timedelta(days=1)

    # Build performance data for each asset
    assets_performance = []

    for asset in assets:
        # Get all transactions for this asset up to end_date
        transactions = db.query(Transaction).filter(
            Transaction.asset_id == asset.id,
            Transaction.user_id == current_user.id,
            Transaction.transaction_date <= end_date
        ).order_by(Transaction.transaction_date).all()

        # Calculate daily values
        daily_values = []
        cumulative_quantity = 0
        total_invested = 0

        for date_str in date_range:
            date = datetime.strptime(date_str, "%Y-%m-%d")

            # Process transactions up to this date
            for txn in transactions:
                if txn.transaction_date.date() <= date.date():
                    if txn.transaction_type == TransactionType.BUY:
                        cumulative_quantity += txn.quantity
                        total_invested += txn.total_amount
                    elif txn.transaction_type == TransactionType.SELL:
                        if cumulative_quantity > 0:
                            # Reduce invested proportionally
                            ratio = txn.quantity / cumulative_quantity
                            total_invested -= total_invested * ratio
                            cumulative_quantity -= txn.quantity

            # Calculate current value (mock price movement)
            # In production, you'd use historical price data
            days_since_start = (date - start_date).days
            price_multiplier = 1 + (days_since_start * 0.002)  # Mock 0.2% daily growth
            current_price = asset.average_buy_price * price_multiplier
            current_value = cumulative_quantity * current_price

            # Calculate profit/loss
            profit_loss = current_value - total_invested if total_invested > 0 else 0

            daily_values.append({
                "date": date_str,
                "value": round(current_value, 2),
                "profit_loss": round(profit_loss, 2)
            })

        assets_performance.append({
            "symbol": asset.symbol,
            "name": asset.name,
            "data": daily_values
        })

    result = {
        "dates": date_range,
        "assets": assets_performance
    }

    # Cache for 5 minutes
    set_cache(cache_key, result, ttl=300)

    return result

@router.get("/search-stocks")
def search_stock_symbols(
    q: str = Query(..., min_length=1, description="Search query for stock symbol or name"),
    limit: int = Query(10, ge=1, le=50, description="Maximum number of results")
):
    """Search for stock symbols and company names"""
    results = search_stocks(q, limit)
    return {"results": results}

@router.get("/by-category")
def get_portfolio_by_category(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get portfolio assets grouped by category and currency"""
    # Check cache first
    cache_key = f"portfolio:category:{current_user.id}"
    cached_data = get_cache(cache_key)
    if cached_data:
        return cached_data

    # Get all user assets
    assets = db.query(Asset).filter(Asset.user_id == current_user.id).all()

    # Group by category then currency
    categories = {
        'stock-etf': {'name': 'Stock & ETF', 'currencies': {}, 'total_invested': 0},
        'cic': {'name': 'Core Investment Combo', 'currencies': {}, 'total_invested': 0},
        'foundation': {'name': 'Foundation', 'currencies': {}, 'total_invested': 0},
        'crypto': {'name': 'Crypto', 'currencies': {}, 'total_invested': 0},
        'currency-metal': {'name': 'Currency & Metals', 'currencies': {}, 'total_invested': 0},
        'other': {'name': 'Other', 'currencies': {}, 'total_invested': 0},
    }

    total_portfolio = {
        'total_invested': 0,
        'assets_count': 0
    }

    for asset in assets:
        # Calculate values
        invested_value = asset.quantity * asset.average_buy_price

        # Get category
        category = asset.asset_category if asset.asset_category in categories else 'other'
        currency = asset.currency

        # Initialize currency in category if not exists
        if currency not in categories[category]['currencies']:
            categories[category]['currencies'][currency] = {
                'assets': [],
                'total_invested': 0
            }

        # Add asset data
        categories[category]['currencies'][currency]['assets'].append({
            'id': asset.id,
            'symbol': asset.symbol,
            'name': asset.name,
            'quantity': asset.quantity,
            'average_buy_price': asset.average_buy_price,
            'invested_value': invested_value,
            'asset_type': asset.asset_type,
            'asset_category': asset.asset_category,
            'currency': asset.currency,
            'remarks': asset.remarks,
            'purchase_date': asset.purchase_date.isoformat() if asset.purchase_date else None
        })

        # Update currency totals
        categories[category]['currencies'][currency]['total_invested'] += invested_value

        # Update category totals
        categories[category]['total_invested'] += invested_value

        # Update portfolio totals
        total_portfolio['total_invested'] += invested_value
        total_portfolio['assets_count'] += 1

    result = {
        'portfolio_summary': total_portfolio,
        'categories': categories
    }

    # Cache the result for 5 minutes
    set_cache(cache_key, result, ttl=300)

    return result
