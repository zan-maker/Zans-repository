"""
Kalshi Market Search - Find NBA games by various keywords
"""
import urllib.request
import json

API_BASE = "https://api.elections.kalshi.com/trade-api/v2"

def search_markets(keyword):
    """Search markets by keyword"""
    url = f"{API_BASE}/markets?status=open&limit=200"
    
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            markets = data.get("markets", [])
            
            # Filter
            matches = []
            for m in markets:
                title = m.get("title", "").lower()
                if keyword.lower() in title:
                    matches.append({
                        "ticker": m.get("ticker"),
                        "title": m.get("title"),
                        "yes_ask": m.get("yes_ask"),
                        "no_ask": m.get("no_ask"),
                        "volume": m.get("volume", 0)
                    })
            return matches
    except Exception as e:
        return []

# Test various search terms
search_terms = [
    "basketball", "nba", "lakers", "celtics", "wizards", 
    "pistons", "knicks", "wins", "defeat", "game"
]

print("KALSHI MARKET SEARCH")
print("=" * 80)

for term in search_terms:
    results = search_markets(term)
    if results:
        print(f"\n'{term}': {len(results)} matches")
        for r in results[:3]:  # Show first 3
            yes = r['yes_ask']/100 if r['yes_ask'] else None
            print(f"  - {r['title'][:60]}...")
            if yes:
                print(f"    Yes: ${yes:.2f}, Volume: {r['volume']:,}")
