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
    """Get historical performance data based on actual buy/sell transactions"""
    # Check cache first
    cache_key = f"performance:{current_user.id}:{days}"
    cached_data = get_cache(cache_key)
    if cached_data:
        return cached_data

    # Get all user transactions
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)

    transactions = db.query(Transaction).filter(
        Transaction.user_id == current_user.id,
        Transaction.transaction_date >= start_date
    ).order_by(Transaction.transaction_date).all()

    if not transactions:
        return []

    # Generate date range
    date_range = []
    current = start_date
    while current <= end_date:
        date_range.append(current.date())
        current += timedelta(days=1)

    # Track portfolio state over time
    # Get initial state (all transactions before start_date)
    initial_transactions = db.query(Transaction).filter(
        Transaction.user_id == current_user.id,
        Transaction.transaction_date < start_date
    ).order_by(Transaction.transaction_date).all()

    # Calculate initial holdings
    holdings = {}  # asset_id -> {quantity, total_invested}

    for txn in initial_transactions:
        if txn.asset_id not in holdings:
            holdings[txn.asset_id] = {'quantity': 0, 'total_invested': 0}

        if txn.transaction_type == TransactionType.BUY:
            holdings[txn.asset_id]['quantity'] += txn.quantity
            holdings[txn.asset_id]['total_invested'] += txn.total_amount
        elif txn.transaction_type == TransactionType.SELL:
            if holdings[txn.asset_id]['quantity'] > 0:
                # Reduce invested proportionally
                ratio = txn.quantity / holdings[txn.asset_id]['quantity']
                holdings[txn.asset_id]['total_invested'] -= holdings[txn.asset_id]['total_invested'] * ratio
                holdings[txn.asset_id]['quantity'] -= txn.quantity

    # Build daily performance data
    performance_data = []
    transaction_index = 0

    for date in date_range:
        # Process all transactions for this date
        while transaction_index < len(transactions) and transactions[transaction_index].transaction_date.date() <= date:
            txn = transactions[transaction_index]

            if txn.asset_id not in holdings:
                holdings[txn.asset_id] = {'quantity': 0, 'total_invested': 0}

            if txn.transaction_type == TransactionType.BUY:
                holdings[txn.asset_id]['quantity'] += txn.quantity
                holdings[txn.asset_id]['total_invested'] += txn.total_amount
            elif txn.transaction_type == TransactionType.SELL:
                if holdings[txn.asset_id]['quantity'] > 0:
                    # Reduce invested proportionally
                    ratio = min(txn.quantity / holdings[txn.asset_id]['quantity'], 1.0)
                    holdings[txn.asset_id]['total_invested'] -= holdings[txn.asset_id]['total_invested'] * ratio
                    holdings[txn.asset_id]['quantity'] -= txn.quantity

            transaction_index += 1

        # Calculate total portfolio value for this date
        # Since we don't have real-time price data, use the invested value as current value
        # In production, you would fetch actual market prices here
        total_value = sum(h['total_invested'] for h in holdings.values() if h['quantity'] > 0)

        performance_data.append({
            'date': date.isoformat(),
            'total_value': round(total_value, 2)
        })

    # Cache for 5 minutes
    set_cache(cache_key, performance_data, ttl=300)

    return performance_data

@router.get("/performance-history/{category}")
def get_category_performance_history(
    category: str,
    days: int = 30,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get historical performance data for a specific category based on actual buy/sell transactions"""
    # Check cache first
    cache_key = f"performance:{current_user.id}:{category}:{days}"
    cached_data = get_cache(cache_key)
    if cached_data:
        return cached_data

    # Get all user transactions for assets in this category
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)

    # Get assets in this category
    category_assets = db.query(Asset).filter(
        Asset.user_id == current_user.id,
        Asset.asset_category == category
    ).all()

    if not category_assets:
        return []

    asset_ids = [asset.id for asset in category_assets]

    transactions = db.query(Transaction).filter(
        Transaction.user_id == current_user.id,
        Transaction.asset_id.in_(asset_ids),
        Transaction.transaction_date >= start_date
    ).order_by(Transaction.transaction_date).all()

    # Generate date range
    date_range = []
    current = start_date
    while current <= end_date:
        date_range.append(current.date())
        current += timedelta(days=1)

    # Track portfolio state over time
    # Get initial state (all transactions before start_date)
    initial_transactions = db.query(Transaction).filter(
        Transaction.user_id == current_user.id,
        Transaction.asset_id.in_(asset_ids),
        Transaction.transaction_date < start_date
    ).order_by(Transaction.transaction_date).all()

    # Calculate initial holdings
    holdings = {}  # asset_id -> {quantity, total_invested}

    for txn in initial_transactions:
        if txn.asset_id not in holdings:
            holdings[txn.asset_id] = {'quantity': 0, 'total_invested': 0}

        if txn.transaction_type == TransactionType.BUY:
            holdings[txn.asset_id]['quantity'] += txn.quantity
            holdings[txn.asset_id]['total_invested'] += txn.total_amount
        elif txn.transaction_type == TransactionType.SELL:
            if holdings[txn.asset_id]['quantity'] > 0:
                # Reduce invested proportionally
                ratio = txn.quantity / holdings[txn.asset_id]['quantity']
                holdings[txn.asset_id]['total_invested'] -= holdings[txn.asset_id]['total_invested'] * ratio
                holdings[txn.asset_id]['quantity'] -= txn.quantity

    # Build daily performance data
    performance_data = []
    transaction_index = 0

    for date in date_range:
        # Process all transactions for this date
        while transaction_index < len(transactions) and transactions[transaction_index].transaction_date.date() <= date:
            txn = transactions[transaction_index]

            if txn.asset_id not in holdings:
                holdings[txn.asset_id] = {'quantity': 0, 'total_invested': 0}

            if txn.transaction_type == TransactionType.BUY:
                holdings[txn.asset_id]['quantity'] += txn.quantity
                holdings[txn.asset_id]['total_invested'] += txn.total_amount
            elif txn.transaction_type == TransactionType.SELL:
                if holdings[txn.asset_id]['quantity'] > 0:
                    # Reduce invested proportionally
                    ratio = min(txn.quantity / holdings[txn.asset_id]['quantity'], 1.0)
                    holdings[txn.asset_id]['total_invested'] -= holdings[txn.asset_id]['total_invested'] * ratio
                    holdings[txn.asset_id]['quantity'] -= txn.quantity

            transaction_index += 1

        # Calculate total category value for this date
        total_value = sum(h['total_invested'] for h in holdings.values() if h['quantity'] > 0)

        performance_data.append({
            'date': date.isoformat(),
            'total_value': round(total_value, 2)
        })

    # Cache for 5 minutes
    set_cache(cache_key, performance_data, ttl=300)

    return performance_data

@router.get("/search-stocks")
def search_stock_symbols(
    q: str = Query(..., min_length=1, description="Search query for stock symbol or name"),
    limit: int = Query(10, ge=1, le=50, description="Maximum number of results")
):
    """Search for stock symbols and company names"""
    results = search_stocks(q, limit)
    return {"results": results}

@router.get("/gains-summary")
def get_gains_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get realized and unrealized gains/losses summary"""
    # Check cache first
    cache_key = f"gains:{current_user.id}"
    cached_data = get_cache(cache_key)
    if cached_data:
        return cached_data

    # Calculate realized gains (from sell transactions)
    # We need to recalculate dynamically because:
    # 1. Old transactions may have realized_gain_loss = 0 (before column existed)
    # 2. The average_buy_price may have changed after the transaction was created
    sell_transactions = db.query(Transaction).filter(
        Transaction.user_id == current_user.id,
        Transaction.transaction_type == TransactionType.SELL
    ).all()

    total_realized_gain_loss = 0
    for txn in sell_transactions:
        # Use stored value if it exists and is non-zero, otherwise recalculate
        if txn.realized_gain_loss is not None and txn.realized_gain_loss != 0:
            total_realized_gain_loss += txn.realized_gain_loss
        else:
            # Recalculate for old transactions that have 0 or None
            asset = db.query(Asset).filter(Asset.id == txn.asset_id).first()
            if asset:
                calculated_gain = (txn.price_per_unit - asset.average_buy_price) * txn.quantity
                total_realized_gain_loss += calculated_gain
                # Update the transaction record for future queries
                txn.realized_gain_loss = calculated_gain

    # Commit any updates made during recalculation
    db.commit()

    # Calculate unrealized gains (from current holdings)
    assets = db.query(Asset).filter(Asset.user_id == current_user.id).all()

    total_unrealized_gain_loss = 0
    for asset in assets:
        if asset.quantity > 0:
            # Current value = quantity * average_buy_price (since we don't have real-time prices)
            # In production, you'd fetch current market price
            current_value = asset.quantity * asset.average_buy_price
            invested_value = asset.quantity * asset.average_buy_price
            # For now, unrealized is 0 since we use average_buy_price as current price
            # In production: unrealized = (current_market_price - average_buy_price) * quantity
            total_unrealized_gain_loss += 0

    result = {
        "total_realized_gain_loss": round(total_realized_gain_loss, 2),
        "total_unrealized_gain_loss": round(total_unrealized_gain_loss, 2),
        "total_gain_loss": round(total_realized_gain_loss + total_unrealized_gain_loss, 2),
        "realized_transactions_count": len(sell_transactions)
    }

    # Cache for 5 minutes
    set_cache(cache_key, result, ttl=300)

    return result

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
