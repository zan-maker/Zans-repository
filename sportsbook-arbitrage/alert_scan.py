#!/usr/bin/env python3
"""
Quick check for high-edge Kalshi opportunities resolving within 7 days
"""
import urllib.request
import json
from datetime import datetime, timedelta

API_BASE = "https://api.elections.kalshi.com/trade-api/v2"

# Current date: Feb 17, 2026
# 7-day window: resolves by Feb 24, 2026
current_date = datetime(2026, 2, 17)
cutoff_date = current_date + timedelta(days=7)

print("=" * 80)
print("HIGH-EDGE KALSHI SCAN")
print(f"Current: {current_date.strftime('%Y-%m-%d')}")
print(f"Cutoff:  {cutoff_date.strftime('%Y-%m-%d')} (7 days)")
print("=" * 80)
print()
print("ALERT CRITERIA:")
print("  - Edge ≥ 4%")
print("  - Confidence ≥ 7/10")
print("  - Volume ≥ $50K")
print("  - Resolves within 7 days")
print()

def get_markets(limit=200):
    """Get open markets"""
    url = f"{API_BASE}/markets?status=open&limit={limit}"
    
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=15) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"Error: {e}")
        return {"markets": []}

def parse_date(date_str):
    """Parse date string"""
    if not date_str:
        return None
    try:
        # Try various formats
        for fmt in ["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ"]:
            try:
                return datetime.strptime(date_str[:len(fmt)-2] if 'T' in fmt else date_str, fmt)
            except:
                continue
    except:
        pass
    return None

# Fetch markets
print("Fetching markets...")
data = get_markets(200)
markets = data.get("markets", [])
print(f"Found {len(markets)} open markets")
print()

# Filter for high-volume, near-term markets
candidates = []

for m in markets:
    ticker = m.get("ticker", "")
    title = m.get("title", "")
    volume = m.get("volume", 0)
    yes_price = m.get("yes_ask", 0) / 100 if m.get("yes_ask") else None
    close_date = parse_date(m.get("close_date") or m.get("settlement_date"))
    
    # Check volume threshold
    if volume < 50000:
        continue
    
    # Check resolution date
    if not close_date or close_date > cutoff_date:
        continue
    
    candidates.append({
        "ticker": ticker,
        "title": title,
        "volume": volume,
        "yes_price": yes_price,
        "close_date": close_date,
        "category": m.get("category", "")
    })

print(f"CANDIDATES (Volume ≥$50K, Resolves by {cutoff_date.strftime('%Y-%m-%d')}):")
print("=" * 80)

if not candidates:
    print("\nNo markets meet criteria.")
    print("\nPossible reasons:")
    print("  - API only returning parlay/futures markets (not single games)")
    print("  - No high-volume markets resolving in next 7 days")
    print("  - Check kalshi.com directly for game markets")
else:
    for c in sorted(candidates, key=lambda x: x['volume'], reverse=True):
        print(f"\n{c['ticker']}")
        print(f"  Title: {c['title'][:70]}...")
        print(f"  Volume: ${c['volume']:,}")
        print(f"  Yes Price: {c['yes_price']:.0%}" if c['yes_price'] else "  Yes Price: N/A")
        print(f"  Closes: {c['close_date'].strftime('%Y-%m-%d')}")
        print(f"  Category: {c['category']}")

print()
print("=" * 80)
print("SCAN COMPLETE")
print()
print("Note: Kalshi API appears to only return:")
print("  - Multi-game parlays (college basketball)")
print("  - Futures markets (championships, awards)")
print("  - NOT single NBA game moneylines")
print()
print("For single game markets, check kalshi.com directly or use")
print("authenticated API with specific ticker lookup.")
