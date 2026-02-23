#!/usr/bin/env python3
"""
Full market scan - all categories, no volume filter
"""
import urllib.request
import json
from datetime import datetime, timedelta

API_BASE = "https://api.elections.kalshi.com/trade-api/v2"

current_date = datetime(2026, 2, 17)
cutoff_date = current_date + timedelta(days=7)

print("=" * 80)
print("ALL MARKETS RESOLVING BY FEB 24, 2026")
print("=" * 80)
print()

def get_markets(limit=500):
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
        for fmt in ["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ"]:
            try:
                return datetime.strptime(date_str[:len(fmt)-2] if 'T' in fmt else date_str, fmt)
            except:
                continue
    except:
        pass
    return None

def format_volume(v):
    if v >= 1000000:
        return f"${v/1000000:.1f}M"
    elif v >= 1000:
        return f"${v/1000:.0f}K"
    else:
        return f"${v}"

# Fetch markets
print("Fetching all markets...")
data = get_markets(500)
markets = data.get("markets", [])
print(f"Total open markets: {len(markets)}")
print()

# Filter for near-term resolution
near_term = []

for m in markets:
    ticker = m.get("ticker", "")
    title = m.get("title", "")
    volume = m.get("volume", 0)
    yes_ask = m.get("yes_ask", 0)
    yes_bid = m.get("yes_bid", 0)
    close_date = parse_date(m.get("close_date") or m.get("settlement_date"))
    category = m.get("category", "unknown")
    
    if not close_date or close_date > cutoff_date:
        continue
    
    near_term.append({
        "ticker": ticker,
        "title": title[:70],
        "volume": volume,
        "yes_ask": yes_ask / 100 if yes_ask else None,
        "yes_bid": yes_bid / 100 if yes_bid else None,
        "close_date": close_date,
        "category": category
    })

print(f"MARKETS RESOLVING BY {cutoff_date.strftime('%Y-%m-%d')}:")
print("=" * 100)
print(f"{'Ticker':<25} {'Category':<12} {'Volume':<10} {'Yes Ask':<8} {'Closes':<12} Title")
print("-" * 100)

if near_term:
    # Sort by volume
    for m in sorted(near_term, key=lambda x: x['volume'], reverse=True):
        yes_str = f"{m['yes_ask']:.0%}" if m['yes_ask'] else "N/A"
        print(f"{m['ticker']:<25} {m['category']:<12} {format_volume(m['volume']):<10} {yes_str:<8} {m['close_date'].strftime('%m/%d'):<12} {m['title'][:40]}...")
else:
    print("No markets found resolving in next 7 days.")

print()
print("=" * 100)

# Check for high volume markets
high_volume = [m for m in near_term if m['volume'] >= 50000]
print(f"\nHIGH VOLUME (≥$50K): {len(high_volume)}")
for m in high_volume:
    print(f"  - {m['ticker']}: {format_volume(m['volume'])} - {m['title'][:50]}...")

# Check for CPI/Fed markets
financial = [m for m in near_term if any(k in m['title'].lower() for k in ['cpi', 'fed', 'inflation', 'rate'])]
print(f"\nFINANCIAL MARKETS: {len(financial)}")
for m in financial:
    print(f"  - {m['ticker']}: {format_volume(m['volume'])} - {m['title'][:50]}...")

print()
print("=" * 100)
print("SCAN COMPLETE")
