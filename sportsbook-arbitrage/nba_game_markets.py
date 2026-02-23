"""
Kalshi NBA Game Markets - Fetch from KXNBAGAME series
"""
import urllib.request
import json
from datetime import datetime

API_BASE = "https://api.elections.kalshi.com/trade-api/v2"

def fetch_series_markets(series_ticker, limit=100):
    """Fetch markets for a specific series"""
    url = f"{API_BASE}/series/{series_ticker}/markets?limit={limit}"
    
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data.get("markets", [])
    except Exception as e:
        print(f"Error fetching {series_ticker}: {e}")
        return []

def parse_game_market(market):
    """Parse market data into readable format"""
    return {
        "ticker": market.get("ticker"),
        "title": market.get("title"),
        "yes_price": market.get("yes_ask", 0) / 100 if market.get("yes_ask") else None,
        "yes_bid": market.get("yes_bid", 0) / 100 if market.get("yes_bid") else None,
        "no_price": market.get("no_ask", 0) / 100 if market.get("no_ask") else None,
        "no_bid": market.get("no_bid", 0) / 100 if market.get("no_bid") else None,
        "last_price": market.get("last_price", 0) / 100 if market.get("last_price") else None,
        "volume": market.get("volume", 0),
        "open_time": market.get("open_time"),
        "close_time": market.get("close_time"),
        "status": market.get("status"),
        "settlement_value": market.get("settlement_value")
    }

if __name__ == "__main__":
    print("Fetching NBA Game Markets from Kalshi")
    print("=" * 80)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("=" * 80)
    print()
    
    # Fetch NBA game markets
    markets = fetch_series_markets("KXNBAGAME", limit=50)
    print(f"Found {len(markets)} NBA game markets\n")
    
    if markets:
        print("NBA GAME MARKETS:")
        print("=" * 80)
        
        for i, market in enumerate(markets[:10], 1):  # Show first 10
            parsed = parse_game_market(market)
            
            print(f"\n{i}. {parsed['ticker']}")
            print(f"   {parsed['title']}")
            
            if parsed['yes_price']:
                print(f"   Yes (Home Win): ${parsed['yes_price']:.2f} ({parsed['yes_price']*100:.0f}%)")
            if parsed['no_price']:
                print(f"   No (Away Win):  ${parsed['no_price']:.2f} ({parsed['no_price']*100:.0f}%)")
            if parsed['last_price']:
                print(f"   Last Trade: ${parsed['last_price']:.2f}")
            
            print(f"   Volume: {parsed['volume']:,}")
            print(f"   Status: {parsed['status']}")
            
            # Show if market is trading
            if parsed['status'] == 'active':
                spread = (parsed['yes_price'] - (1 - parsed['no_price'])) if (parsed['yes_price'] and parsed['no_price']) else 0
                if abs(spread) > 0.01:
                    print(f"   ⚠️  Spread: {spread:.2f} (potential arbitrage)")
    else:
        print("No markets found in KXNBAGAME series")
        print("\nTrying KXMVENBASINGLEGAME...")
        markets = fetch_series_markets("KXMVENBASINGLEGAME", limit=50)
        print(f"Found {len(markets)} markets")
        for m in markets[:5]:
            print(f"  - {m.get('ticker')}: {m.get('title', '')[:60]}")
