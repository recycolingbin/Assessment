"""
Stock symbol search utility
In production, this would integrate with a real API like Alpha Vantage, IEX Cloud, or Finnhub
For now, we'll use a static list of popular stocks across US, HK, and China A-share markets
"""

STOCK_DATABASE = [
    # US Stocks
    {"symbol": "AAPL", "name": "Apple Inc.", "currency": "USD", "asset_type": "stock"},
    {"symbol": "MSFT", "name": "Microsoft Corporation", "currency": "USD", "asset_type": "stock"},
    {"symbol": "GOOGL", "name": "Alphabet Inc. Class A", "currency": "USD", "asset_type": "stock"},
    {"symbol": "GOOG", "name": "Alphabet Inc. Class C", "currency": "USD", "asset_type": "stock"},
    {"symbol": "AMZN", "name": "Amazon.com Inc.", "currency": "USD", "asset_type": "stock"},
    {"symbol": "TSLA", "name": "Tesla Inc.", "currency": "USD", "asset_type": "stock"},
    {"symbol": "META", "name": "Meta Platforms Inc.", "currency": "USD", "asset_type": "stock"},
    {"symbol": "NVDA", "name": "NVIDIA Corporation", "currency": "USD", "asset_type": "stock"},
    {"symbol": "BRK.B", "name": "Berkshire Hathaway Inc. Class B", "currency": "USD", "asset_type": "stock"},
    {"symbol": "JPM", "name": "JPMorgan Chase & Co.", "currency": "USD", "asset_type": "stock"},
    {"symbol": "V", "name": "Visa Inc.", "currency": "USD", "asset_type": "stock"},
    {"symbol": "JNJ", "name": "Johnson & Johnson", "currency": "USD", "asset_type": "stock"},
    {"symbol": "WMT", "name": "Walmart Inc.", "currency": "USD", "asset_type": "stock"},
    {"symbol": "PG", "name": "Procter & Gamble Co.", "currency": "USD", "asset_type": "stock"},
    {"symbol": "MA", "name": "Mastercard Inc.", "currency": "USD", "asset_type": "stock"},
    {"symbol": "UNH", "name": "UnitedHealth Group Inc.", "currency": "USD", "asset_type": "stock"},
    {"symbol": "HD", "name": "Home Depot Inc.", "currency": "USD", "asset_type": "stock"},
    {"symbol": "DIS", "name": "Walt Disney Co.", "currency": "USD", "asset_type": "stock"},
    {"symbol": "BAC", "name": "Bank of America Corp.", "currency": "USD", "asset_type": "stock"},
    {"symbol": "ADBE", "name": "Adobe Inc.", "currency": "USD", "asset_type": "stock"},
    {"symbol": "NFLX", "name": "Netflix Inc.", "currency": "USD", "asset_type": "stock"},
    {"symbol": "CRM", "name": "Salesforce Inc.", "currency": "USD", "asset_type": "stock"},
    {"symbol": "XOM", "name": "Exxon Mobil Corporation", "currency": "USD", "asset_type": "stock"},
    {"symbol": "CSCO", "name": "Cisco Systems Inc.", "currency": "USD", "asset_type": "stock"},
    {"symbol": "PFE", "name": "Pfizer Inc.", "currency": "USD", "asset_type": "stock"},
    {"symbol": "INTC", "name": "Intel Corporation", "currency": "USD", "asset_type": "stock"},
    {"symbol": "VZ", "name": "Verizon Communications Inc.", "currency": "USD", "asset_type": "stock"},
    {"symbol": "KO", "name": "Coca-Cola Co.", "currency": "USD", "asset_type": "stock"},
    {"symbol": "NKE", "name": "Nike Inc.", "currency": "USD", "asset_type": "stock"},
    {"symbol": "T", "name": "AT&T Inc.", "currency": "USD", "asset_type": "stock"},
    {"symbol": "MRK", "name": "Merck & Co. Inc.", "currency": "USD", "asset_type": "stock"},
    {"symbol": "PEP", "name": "PepsiCo Inc.", "currency": "USD", "asset_type": "stock"},
    {"symbol": "ABBV", "name": "AbbVie Inc.", "currency": "USD", "asset_type": "stock"},
    {"symbol": "TMO", "name": "Thermo Fisher Scientific Inc.", "currency": "USD", "asset_type": "stock"},
    {"symbol": "COST", "name": "Costco Wholesale Corporation", "currency": "USD", "asset_type": "stock"},
    {"symbol": "AVGO", "name": "Broadcom Inc.", "currency": "USD", "asset_type": "stock"},
    {"symbol": "ACN", "name": "Accenture plc", "currency": "USD", "asset_type": "stock"},
    {"symbol": "LLY", "name": "Eli Lilly and Co.", "currency": "USD", "asset_type": "stock"},
    {"symbol": "ABT", "name": "Abbott Laboratories", "currency": "USD", "asset_type": "stock"},
    {"symbol": "TXN", "name": "Texas Instruments Inc.", "currency": "USD", "asset_type": "stock"},
    {"symbol": "ORCL", "name": "Oracle Corporation", "currency": "USD", "asset_type": "stock"},
    {"symbol": "DHR", "name": "Danaher Corporation", "currency": "USD", "asset_type": "stock"},
    {"symbol": "CVX", "name": "Chevron Corporation", "currency": "USD", "asset_type": "stock"},
    {"symbol": "WFC", "name": "Wells Fargo & Co.", "currency": "USD", "asset_type": "stock"},
    {"symbol": "NEE", "name": "NextEra Energy Inc.", "currency": "USD", "asset_type": "stock"},
    {"symbol": "MCD", "name": "McDonald's Corporation", "currency": "USD", "asset_type": "stock"},
    {"symbol": "LIN", "name": "Linde plc", "currency": "USD", "asset_type": "stock"},
    {"symbol": "BMY", "name": "Bristol-Myers Squibb Co.", "currency": "USD", "asset_type": "stock"},
    {"symbol": "UPS", "name": "United Parcel Service Inc.", "currency": "USD", "asset_type": "stock"},
    {"symbol": "QCOM", "name": "Qualcomm Inc.", "currency": "USD", "asset_type": "stock"},

    # US ETFs
    {"symbol": "SPY", "name": "SPDR S&P 500 ETF Trust", "currency": "USD", "asset_type": "etf"},
    {"symbol": "QQQ", "name": "Invesco QQQ Trust", "currency": "USD", "asset_type": "etf"},
    {"symbol": "VOO", "name": "Vanguard S&P 500 ETF", "currency": "USD", "asset_type": "etf"},
    {"symbol": "VTI", "name": "Vanguard Total Stock Market ETF", "currency": "USD", "asset_type": "etf"},
    {"symbol": "IVV", "name": "iShares Core S&P 500 ETF", "currency": "USD", "asset_type": "etf"},

    # Hong Kong Stocks
    {"symbol": "0700", "name": "Tencent Holdings Ltd", "currency": "HKD", "asset_type": "stock"},
    {"symbol": "9988", "name": "Alibaba Group Holding Ltd", "currency": "HKD", "asset_type": "stock"},
    {"symbol": "0005", "name": "HSBC Holdings plc", "currency": "HKD", "asset_type": "stock"},
    {"symbol": "0941", "name": "China Mobile Ltd", "currency": "HKD", "asset_type": "stock"},
    {"symbol": "1299", "name": "AIA Group Ltd", "currency": "HKD", "asset_type": "stock"},
    {"symbol": "0388", "name": "Hong Kong Exchanges and Clearing Ltd", "currency": "HKD", "asset_type": "stock"},
    {"symbol": "1398", "name": "Industrial and Commercial Bank of China Ltd", "currency": "HKD", "asset_type": "stock"},
    {"symbol": "0939", "name": "China Construction Bank Corporation", "currency": "HKD", "asset_type": "stock"},
    {"symbol": "3690", "name": "Meituan", "currency": "HKD", "asset_type": "stock"},
    {"symbol": "2318", "name": "Ping An Insurance Group Co of China Ltd", "currency": "HKD", "asset_type": "stock"},
    {"symbol": "1810", "name": "Xiaomi Corporation", "currency": "HKD", "asset_type": "stock"},
    {"symbol": "0001", "name": "CK Hutchison Holdings Ltd", "currency": "HKD", "asset_type": "stock"},
    {"symbol": "0002", "name": "CLP Holdings Ltd", "currency": "HKD", "asset_type": "stock"},
    {"symbol": "0003", "name": "Hong Kong and China Gas Co Ltd", "currency": "HKD", "asset_type": "stock"},
    {"symbol": "0011", "name": "Hang Seng Bank Ltd", "currency": "HKD", "asset_type": "stock"},
    {"symbol": "0016", "name": "Sun Hung Kai Properties Ltd", "currency": "HKD", "asset_type": "stock"},
    {"symbol": "0027", "name": "Galaxy Entertainment Group Ltd", "currency": "HKD", "asset_type": "stock"},
    {"symbol": "0066", "name": "MTR Corporation Ltd", "currency": "HKD", "asset_type": "stock"},
    {"symbol": "0175", "name": "Geely Automobile Holdings Ltd", "currency": "HKD", "asset_type": "stock"},
    {"symbol": "0883", "name": "CNOOC Ltd", "currency": "HKD", "asset_type": "stock"},
    {"symbol": "0857", "name": "PetroChina Co Ltd", "currency": "HKD", "asset_type": "stock"},
    {"symbol": "1113", "name": "CK Asset Holdings Ltd", "currency": "HKD", "asset_type": "stock"},
    {"symbol": "1997", "name": "Wharf Real Estate Investment Co Ltd", "currency": "HKD", "asset_type": "stock"},
    {"symbol": "2020", "name": "ANTA Sports Products Ltd", "currency": "HKD", "asset_type": "stock"},
    {"symbol": "2382", "name": "Sunny Optical Technology Group Co Ltd", "currency": "HKD", "asset_type": "stock"},
    {"symbol": "9618", "name": "JD.com Inc", "currency": "HKD", "asset_type": "stock"},
    {"symbol": "9999", "name": "NetEase Inc", "currency": "HKD", "asset_type": "stock"},
    {"symbol": "6098", "name": "Country Garden Services Holdings Co Ltd", "currency": "HKD", "asset_type": "stock"},
    {"symbol": "1024", "name": "Kuaishou Technology", "currency": "HKD", "asset_type": "stock"},
    {"symbol": "2269", "name": "WuXi Biologics Cayman Inc", "currency": "HKD", "asset_type": "stock"},

    # China A-Shares
    {"symbol": "600519", "name": "Kweichow Moutai Co Ltd", "currency": "CNY", "asset_type": "stock"},
    {"symbol": "600036", "name": "China Merchants Bank Co Ltd", "currency": "CNY", "asset_type": "stock"},
    {"symbol": "601318", "name": "Ping An Insurance Group Co of China Ltd", "currency": "CNY", "asset_type": "stock"},
    {"symbol": "600276", "name": "Jiangsu Hengrui Medicine Co Ltd", "currency": "CNY", "asset_type": "stock"},
    {"symbol": "000858", "name": "Wuliangye Yibin Co Ltd", "currency": "CNY", "asset_type": "stock"},
    {"symbol": "000333", "name": "Midea Group Co Ltd", "currency": "CNY", "asset_type": "stock"},
    {"symbol": "601012", "name": "Longi Green Energy Technology Co Ltd", "currency": "CNY", "asset_type": "stock"},
    {"symbol": "600887", "name": "Inner Mongolia Yili Industrial Group Co Ltd", "currency": "CNY", "asset_type": "stock"},
    {"symbol": "000568", "name": "Luzhou Laojiao Co Ltd", "currency": "CNY", "asset_type": "stock"},
    {"symbol": "002594", "name": "BYD Co Ltd", "currency": "CNY", "asset_type": "stock"},
    {"symbol": "600030", "name": "CITIC Securities Co Ltd", "currency": "CNY", "asset_type": "stock"},
    {"symbol": "601166", "name": "Industrial Bank Co Ltd", "currency": "CNY", "asset_type": "stock"},
    {"symbol": "600900", "name": "China Yangtze Power Co Ltd", "currency": "CNY", "asset_type": "stock"},
    {"symbol": "601888", "name": "China Tourism Group Duty Free Corporation Ltd", "currency": "CNY", "asset_type": "stock"},
    {"symbol": "000001", "name": "Ping An Bank Co Ltd", "currency": "CNY", "asset_type": "stock"},
    {"symbol": "600031", "name": "Sany Heavy Industry Co Ltd", "currency": "CNY", "asset_type": "stock"},
    {"symbol": "601398", "name": "Industrial and Commercial Bank of China Ltd", "currency": "CNY", "asset_type": "stock"},
    {"symbol": "601939", "name": "China Construction Bank Corporation", "currency": "CNY", "asset_type": "stock"},
    {"symbol": "601288", "name": "Agricultural Bank of China Ltd", "currency": "CNY", "asset_type": "stock"},
    {"symbol": "600000", "name": "Shanghai Pudong Development Bank Co Ltd", "currency": "CNY", "asset_type": "stock"},

    # Crypto
    {"symbol": "BTC", "name": "Bitcoin", "currency": "USD", "asset_type": "crypto"},
    {"symbol": "ETH", "name": "Ethereum", "currency": "USD", "asset_type": "crypto"},
    {"symbol": "USDT", "name": "Tether", "currency": "USD", "asset_type": "crypto"},
    {"symbol": "BNB", "name": "Binance Coin", "currency": "USD", "asset_type": "crypto"},
    {"symbol": "SOL", "name": "Solana", "currency": "USD", "asset_type": "crypto"},
    {"symbol": "XRP", "name": "Ripple", "currency": "USD", "asset_type": "crypto"},
    {"symbol": "ADA", "name": "Cardano", "currency": "USD", "asset_type": "crypto"},
    {"symbol": "DOGE", "name": "Dogecoin", "currency": "USD", "asset_type": "crypto"},

    # Precious Metals
    {"symbol": "XAU", "name": "Gold", "currency": "USD", "asset_type": "precious_metal"},
    {"symbol": "XAG", "name": "Silver", "currency": "USD", "asset_type": "precious_metal"},
    {"symbol": "XPT", "name": "Platinum", "currency": "USD", "asset_type": "precious_metal"},
    {"symbol": "XPD", "name": "Palladium", "currency": "USD", "asset_type": "precious_metal"},
]

def search_stocks(query: str, limit: int = 10):
    """
    Search for stocks by symbol or name
    Returns matching stocks sorted by relevance
    """
    if not query:
        return []

    query = query.upper().strip()
    results = []

    # Exact symbol match gets highest priority
    for stock in STOCK_DATABASE:
        if stock["symbol"] == query:
            results.insert(0, stock)
        elif stock["symbol"].startswith(query):
            results.append(stock)
        elif query in stock["name"].upper():
            results.append(stock)

    # Remove duplicates while preserving order
    seen = set()
    unique_results = []
    for stock in results:
        if stock["symbol"] not in seen:
            seen.add(stock["symbol"])
            unique_results.append(stock)

    return unique_results[:limit]
