"""
Kalshi Series Explorer - Find NBA Game Series
"""
import urllib.request
import json

API_BASE = "https://api.elections.kalshi.com/trade-api/v2"

def fetch_series():
    """Fetch all series"""
    url = f"{API_BASE}/series?limit=100"
    
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data.get("series", [])
    except Exception as e:
        print(f"Error: {e}")
        return []

def fetch_series_markets(series_ticker):
    """Fetch markets for a specific series"""
    url = f"{API_BASE}/series/{series_ticker}/markets?limit=100"
    
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data.get("markets", [])
    except Exception as e:
        return []

if __name__ == "__main__":
    print("Fetching Kalshi series...")
    print("=" * 80)
    
    series_list = fetch_series()
    print(f"Total series: {len(series_list)}")
    print()
    
    # Filter for sports series
    sports_series = [s for s in series_list if "sport" in s.get("ticker", "").lower()]
    print(f"Sports series: {len(sports_series)}")
    
    # Look for NBA specifically
    nba_series = [s for s in series_list if "nba" in s.get("ticker", "").lower()]
    print(f"NBA series: {len(nba_series)}")
    
    if nba_series:
        print("\n" + "=" * 80)
        print("NBA SERIES:")
        for s in nba_series:
            print(f"\nTicker: {s['ticker']}")
            print(f"Title: {s.get('title', '')}")
            print(f"Category: {s.get('category', '')}")
            
            # Get markets in this series
            markets = fetch_series_markets(s['ticker'])
            if markets:
                print(f"Markets in series: {len(markets)}")
                for m in markets[:3]:
                    print(f"  - {m.get('ticker')}: {m.get('title', '')[:50]}...")
    
    # Show sample of all sports series
    print("\n" + "=" * 80)
    print("ALL SPORTS SERIES (sample):")
    for s in sports_series[:10]:
        print(f"  - {s['ticker']}: {s.get('title', '')}")
