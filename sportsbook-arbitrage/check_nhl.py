#!/usr/bin/env python3
"""
Check specific NHL 4 Nations markets (from memory)
"""
import urllib.request
import json

API_BASE = "https://api.elections.kalshi.com/trade-api/v2"

# Known series/tickers from memory
# NHL 4 Nations Face-Off - Canada vs USA - Feb 20
# From memory: "NHL 4 Nations Face-Off" - Canada at 55¢, Feb 20 resolution

markets_to_check = [
    "KXHOCKEY4NAT",  # Potential ticker pattern
    "KX4NATIONS",
    "KXHOCKEY",
    "KXHOCKEY-26",
    "KXOLYMPIC",
]

print("=" * 80)
print("CHECKING SPECIFIC NHL MARKETS")
print("=" * 80)
print()

def get_market(ticker):
    """Get specific market"""
    url = f"{API_BASE}/markets/{ticker}"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}

# Try to find the NHL market
for ticker in markets_to_check:
    result = get_market(ticker)
    if result and "error" not in result:
        print(f"\n✓ FOUND: {ticker}")
        print(json.dumps(result, indent=2))
        break
else:
    print("No markets found with tested tickers.")
    print()
    print("Attempting series search...")
    
    # Try to find hockey series
    url = f"{API_BASE}/series?category=sports&limit=100"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))
            series_list = data.get("series", [])
            
            hockey_series = [s for s in series_list if 'hockey' in s.get("title", "").lower() or 'nhl' in s.get("ticker", "").lower()]
            
            if hockey_series:
                print(f"\nFound {len(hockey_series)} hockey series:")
                for s in hockey_series[:5]:
                    print(f"  - {s.get('ticker')}: {s.get('title')}")
            else:
                print("No hockey series found in sports category.")
                
    except Exception as e:
        print(f"Error: {e}")

print()
print("=" * 80)
print("From MEMORY.md:")
print("  NHL 4 Nations Face-Off - Canada at 55¢")
print("  Resolution: Feb 20, 2026")
print("  Status: Requires manual DraftKings check for Canada vs USA odds")
print("=" * 80)
