# Stock and asset data for auto-fill functionality
# This can be extended to use a real API in the future

STOCK_DATABASE = {
    # US Stocks
    'AAPL': {'name': 'Apple Inc.', 'type': 'stock', 'currency': 'USD', 'market': 'NASDAQ'},
    'MSFT': {'name': 'Microsoft Corporation', 'type': 'stock', 'currency': 'USD', 'market': 'NASDAQ'},
    'GOOGL': {'name': 'Alphabet Inc.', 'type': 'stock', 'currency': 'USD', 'market': 'NASDAQ'},
    'GOOG': {'name': 'Alphabet Inc. Class C', 'type': 'stock', 'currency': 'USD', 'market': 'NASDAQ'},
    'AMZN': {'name': 'Amazon.com Inc.', 'type': 'stock', 'currency': 'USD', 'market': 'NASDAQ'},
    'NVDA': {'name': 'NVIDIA Corporation', 'type': 'stock', 'currency': 'USD', 'market': 'NASDAQ'},
    'META': {'name': 'Meta Platforms Inc.', 'type': 'stock', 'currency': 'USD', 'market': 'NASDAQ'},
    'TSLA': {'name': 'Tesla Inc.', 'type': 'stock', 'currency': 'USD', 'market': 'NASDAQ'},
    'JPM': {'name': 'JPMorgan Chase & Co.', 'type': 'stock', 'currency': 'USD', 'market': 'NYSE'},
    'V': {'name': 'Visa Inc.', 'type': 'stock', 'currency': 'USD', 'market': 'NYSE'},
    'WMT': {'name': 'Walmart Inc.', 'type': 'stock', 'currency': 'USD', 'market': 'NYSE'},
    'JNJ': {'name': 'Johnson & Johnson', 'type': 'stock', 'currency': 'USD', 'market': 'NYSE'},
    'DIS': {'name': 'The Walt Disney Company', 'type': 'stock', 'currency': 'USD', 'market': 'NYSE'},
    'MCD': {'name': 'McDonald\'s Corporation', 'type': 'stock', 'currency': 'USD', 'market': 'NYSE'},
    'BA': {'name': 'The Boeing Company', 'type': 'stock', 'currency': 'USD', 'market': 'NYSE'},
    'PG': {'name': 'Procter & Gamble Co.', 'type': 'stock', 'currency': 'USD', 'market': 'NYSE'},
    'MA': {'name': 'Mastercard Inc.', 'type': 'stock', 'currency': 'USD', 'market': 'NYSE'},
    'UNH': {'name': 'UnitedHealth Group Inc.', 'type': 'stock', 'currency': 'USD', 'market': 'NYSE'},
    'HD': {'name': 'Home Depot Inc.', 'type': 'stock', 'currency': 'USD', 'market': 'NYSE'},
    'BAC': {'name': 'Bank of America Corp.', 'type': 'stock', 'currency': 'USD', 'market': 'NYSE'},
    'NFLX': {'name': 'Netflix Inc.', 'type': 'stock', 'currency': 'USD', 'market': 'NASDAQ'},
    'ADBE': {'name': 'Adobe Inc.', 'type': 'stock', 'currency': 'USD', 'market': 'NASDAQ'},
    'CRM': {'name': 'Salesforce Inc.', 'type': 'stock', 'currency': 'USD', 'market': 'NYSE'},
    'INTC': {'name': 'Intel Corporation', 'type': 'stock', 'currency': 'USD', 'market': 'NASDAQ'},
    'CSCO': {'name': 'Cisco Systems Inc.', 'type': 'stock', 'currency': 'USD', 'market': 'NASDAQ'},

    # ETFs
    'SPY': {'name': 'SPDR S&P 500 ETF', 'type': 'etf', 'currency': 'USD', 'market': 'NYSE'},
    'QQQ': {'name': 'Invesco QQQ Trust', 'type': 'etf', 'currency': 'USD', 'market': 'NASDAQ'},
    'IVV': {'name': 'iShares Core S&P 500 ETF', 'type': 'etf', 'currency': 'USD', 'market': 'NYSE'},
    'VOO': {'name': 'Vanguard S&P 500 ETF', 'type': 'etf', 'currency': 'USD', 'market': 'NYSE'},
    'VTI': {'name': 'Vanguard Total Stock Market ETF', 'type': 'etf', 'currency': 'USD', 'market': 'NASDAQ'},
    'AGG': {'name': 'iShares Core U.S. Aggregate Bond ETF', 'type': 'etf', 'currency': 'USD', 'market': 'NYSE'},
    'BND': {'name': 'Vanguard Total Bond Market ETF', 'type': 'etf', 'currency': 'USD', 'market': 'NASDAQ'},
    'VGIT': {'name': 'Vanguard Intermediate-Term Treasury ETF', 'type': 'etf', 'currency': 'USD', 'market': 'NASDAQ'},

    # Hong Kong Stocks
    '0001': {'name': 'CK Hutchison Holdings Ltd', 'type': 'stock', 'currency': 'HKD', 'market': 'HKEX'},
    '0002': {'name': 'CLP Holdings Ltd', 'type': 'stock', 'currency': 'HKD', 'market': 'HKEX'},
    '0003': {'name': 'Hong Kong and China Gas Co Ltd', 'type': 'stock', 'currency': 'HKD', 'market': 'HKEX'},
    '0005': {'name': 'HSBC Holdings plc', 'type': 'stock', 'currency': 'HKD', 'market': 'HKEX'},
    '0011': {'name': 'Hang Seng Bank Ltd', 'type': 'stock', 'currency': 'HKD', 'market': 'HKEX'},
    '0016': {'name': 'Sun Hung Kai Properties Ltd', 'type': 'stock', 'currency': 'HKD', 'market': 'HKEX'},
    '0027': {'name': 'Galaxy Entertainment Group Ltd', 'type': 'stock', 'currency': 'HKD', 'market': 'HKEX'},
    '0066': {'name': 'MTR Corporation Ltd', 'type': 'stock', 'currency': 'HKD', 'market': 'HKEX'},
    '0175': {'name': 'Geely Automobile Holdings Ltd', 'type': 'stock', 'currency': 'HKD', 'market': 'HKEX'},
    '0388': {'name': 'Hong Kong Exchanges and Clearing Ltd', 'type': 'stock', 'currency': 'HKD', 'market': 'HKEX'},
    '0700': {'name': 'Tencent Holdings Ltd', 'type': 'stock', 'currency': 'HKD', 'market': 'HKEX'},
    '0857': {'name': 'PetroChina Co Ltd', 'type': 'stock', 'currency': 'HKD', 'market': 'HKEX'},
    '0883': {'name': 'CNOOC Ltd', 'type': 'stock', 'currency': 'HKD', 'market': 'HKEX'},
    '0939': {'name': 'China Construction Bank Corporation', 'type': 'stock', 'currency': 'HKD', 'market': 'HKEX'},
    '0941': {'name': 'China Mobile Ltd', 'type': 'stock', 'currency': 'HKD', 'market': 'HKEX'},
    '1024': {'name': 'Kuaishou Technology', 'type': 'stock', 'currency': 'HKD', 'market': 'HKEX'},
    '1113': {'name': 'CK Asset Holdings Ltd', 'type': 'stock', 'currency': 'HKD', 'market': 'HKEX'},
    '1299': {'name': 'AIA Group Ltd', 'type': 'stock', 'currency': 'HKD', 'market': 'HKEX'},
    '1398': {'name': 'Industrial and Commercial Bank of China Ltd', 'type': 'stock', 'currency': 'HKD', 'market': 'HKEX'},
    '1810': {'name': 'Xiaomi Corporation', 'type': 'stock', 'currency': 'HKD', 'market': 'HKEX'},
    '1997': {'name': 'Wharf Real Estate Investment Co Ltd', 'type': 'stock', 'currency': 'HKD', 'market': 'HKEX'},
    '2020': {'name': 'ANTA Sports Products Ltd', 'type': 'stock', 'currency': 'HKD', 'market': 'HKEX'},
    '2269': {'name': 'WuXi Biologics Cayman Inc', 'type': 'stock', 'currency': 'HKD', 'market': 'HKEX'},
    '2318': {'name': 'Ping An Insurance Group Co of China Ltd', 'type': 'stock', 'currency': 'HKD', 'market': 'HKEX'},
    '2382': {'name': 'Sunny Optical Technology Group Co Ltd', 'type': 'stock', 'currency': 'HKD', 'market': 'HKEX'},
    '3690': {'name': 'Meituan', 'type': 'stock', 'currency': 'HKD', 'market': 'HKEX'},
    '6098': {'name': 'Country Garden Services Holdings Co Ltd', 'type': 'stock', 'currency': 'HKD', 'market': 'HKEX'},
    '9618': {'name': 'JD.com Inc', 'type': 'stock', 'currency': 'HKD', 'market': 'HKEX'},
    '9988': {'name': 'Alibaba Group Holding Ltd', 'type': 'stock', 'currency': 'HKD', 'market': 'HKEX'},
    '9999': {'name': 'NetEase Inc', 'type': 'stock', 'currency': 'HKD', 'market': 'HKEX'},

    # China A-Shares
    '000001': {'name': 'Ping An Bank Co Ltd', 'type': 'stock', 'currency': 'CNY', 'market': 'SZSE'},
    '000333': {'name': 'Midea Group Co Ltd', 'type': 'stock', 'currency': 'CNY', 'market': 'SZSE'},
    '000568': {'name': 'Luzhou Laojiao Co Ltd', 'type': 'stock', 'currency': 'CNY', 'market': 'SZSE'},
    '000858': {'name': 'Wuliangye Yibin Co Ltd', 'type': 'stock', 'currency': 'CNY', 'market': 'SZSE'},
    '002594': {'name': 'BYD Co Ltd', 'type': 'stock', 'currency': 'CNY', 'market': 'SZSE'},
    '600000': {'name': 'Shanghai Pudong Development Bank Co Ltd', 'type': 'stock', 'currency': 'CNY', 'market': 'SSE'},
    '600030': {'name': 'CITIC Securities Co Ltd', 'type': 'stock', 'currency': 'CNY', 'market': 'SSE'},
    '600031': {'name': 'Sany Heavy Industry Co Ltd', 'type': 'stock', 'currency': 'CNY', 'market': 'SSE'},
    '600036': {'name': 'China Merchants Bank Co Ltd', 'type': 'stock', 'currency': 'CNY', 'market': 'SSE'},
    '600276': {'name': 'Jiangsu Hengrui Medicine Co Ltd', 'type': 'stock', 'currency': 'CNY', 'market': 'SSE'},
    '600519': {'name': 'Kweichow Moutai Co Ltd', 'type': 'stock', 'currency': 'CNY', 'market': 'SSE'},
    '600887': {'name': 'Inner Mongolia Yili Industrial Group Co Ltd', 'type': 'stock', 'currency': 'CNY', 'market': 'SSE'},
    '600900': {'name': 'China Yangtze Power Co Ltd', 'type': 'stock', 'currency': 'CNY', 'market': 'SSE'},
    '601012': {'name': 'Longi Green Energy Technology Co Ltd', 'type': 'stock', 'currency': 'CNY', 'market': 'SSE'},
    '601166': {'name': 'Industrial Bank Co Ltd', 'type': 'stock', 'currency': 'CNY', 'market': 'SSE'},
    '601288': {'name': 'Agricultural Bank of China Ltd', 'type': 'stock', 'currency': 'CNY', 'market': 'SSE'},
    '601318': {'name': 'Ping An Insurance Group Co of China Ltd', 'type': 'stock', 'currency': 'CNY', 'market': 'SSE'},
    '601398': {'name': 'Industrial and Commercial Bank of China Ltd', 'type': 'stock', 'currency': 'CNY', 'market': 'SSE'},
    '601668': {'name': 'China State Construction Engineering Corp', 'type': 'stock', 'currency': 'CNY', 'market': 'SSE'},
    '601888': {'name': 'China Tourism Group Duty Free Corporation Ltd', 'type': 'stock', 'currency': 'CNY', 'market': 'SSE'},
    '601939': {'name': 'China Construction Bank Corporation', 'type': 'stock', 'currency': 'CNY', 'market': 'SSE'},
    '601988': {'name': 'Bank of China Ltd', 'type': 'stock', 'currency': 'CNY', 'market': 'SSE'},

    # Cryptocurrencies
    'BTC': {'name': 'Bitcoin', 'type': 'crypto', 'currency': 'USD', 'market': 'Crypto'},
    'ETH': {'name': 'Ethereum', 'type': 'crypto', 'currency': 'USD', 'market': 'Crypto'},
    'USDT': {'name': 'Tether', 'type': 'crypto', 'currency': 'USD', 'market': 'Crypto'},
    'USDC': {'name': 'USD Coin', 'type': 'crypto', 'currency': 'USD', 'market': 'Crypto'},
    'BNB': {'name': 'Binance Coin', 'type': 'crypto', 'currency': 'USD', 'market': 'Crypto'},
    'XRP': {'name': 'Ripple', 'type': 'crypto', 'currency': 'USD', 'market': 'Crypto'},
    'ADA': {'name': 'Cardano', 'type': 'crypto', 'currency': 'USD', 'market': 'Crypto'},
    'SOL': {'name': 'Solana', 'type': 'crypto', 'currency': 'USD', 'market': 'Crypto'},
    'DOGE': {'name': 'Dogecoin', 'type': 'crypto', 'currency': 'USD', 'market': 'Crypto'},
    'LTC': {'name': 'Litecoin', 'type': 'crypto', 'currency': 'USD', 'market': 'Crypto'},
    'BCH': {'name': 'Bitcoin Cash', 'type': 'crypto', 'currency': 'USD', 'market': 'Crypto'},

    # Precious Metals
    'XAU': {'name': 'Gold', 'type': 'precious_metal', 'currency': 'USD', 'market': 'Commodity'},
    'XAG': {'name': 'Silver', 'type': 'precious_metal', 'currency': 'USD', 'market': 'Commodity'},
    'XPT': {'name': 'Platinum', 'type': 'precious_metal', 'currency': 'USD', 'market': 'Commodity'},
    'XPD': {'name': 'Palladium', 'type': 'precious_metal', 'currency': 'USD', 'market': 'Commodity'},

    # Bonds
    'US10Y': {'name': 'US 10-Year Treasury Bond', 'type': 'bond', 'currency': 'USD', 'market': 'Treasury'},
    'US2Y': {'name': 'US 2-Year Treasury Bond', 'type': 'bond', 'currency': 'USD', 'market': 'Treasury'},
    'US30Y': {'name': 'US 30-Year Treasury Bond', 'type': 'bond', 'currency': 'USD', 'market': 'Treasury'},
}

def get_stock_auto_data(symbol: str):
    """Get auto-fill data for a stock symbol"""
    symbol_upper = symbol.upper()
    return STOCK_DATABASE.get(symbol_upper)

def determine_asset_category(asset_type: str, currency: str) -> str:
    """Determine asset category based on type and currency"""
    asset_type_lower = asset_type.lower()

    if asset_type_lower == 'crypto':
        return 'crypto'
    elif asset_type_lower in ['bond', 'mutual_fund']:
        return 'cic'
    elif asset_type_lower in ['etf', 'stock']:
        return 'stock-etf'
    elif asset_type_lower in ['precious_metal', 'currency', 'money_market']:
        return 'currency-metal'
    else:
        return 'other'

def auto_fill_asset(symbol: str):
    """Auto-fill asset details from symbol"""
    data = get_stock_auto_data(symbol)
    if data:
        return {
            'symbol': symbol.upper(),
            'name': data.get('name', symbol.upper()),
            'asset_type': data.get('type', 'stock'),
            'currency': data.get('currency', 'USD'),
            'asset_category': determine_asset_category(data.get('type', 'stock'), data.get('currency', 'USD')),
            'market': data.get('market', 'Unknown')
        }
    return None
