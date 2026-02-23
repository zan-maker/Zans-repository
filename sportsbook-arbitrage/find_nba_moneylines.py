"""
Kalshi NBA Markets - Comprehensive Search
Search all markets for NBA game lines
"""
import urllib.request
import json
from datetime import datetime

API_BASE = "https://api.elections.kalshi.com/trade-api/v2"

def fetch_all_markets():
    """Fetch all open markets"""
    markets = []
    cursor = None
    
    while True:
        url = f"{API_BASE}/markets?status=open&limit=1000"
        if cursor:
            url += f"&cursor={cursor}"
        
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=30) as response:
                data = json.loads(response.read().decode('utf-8'))
                batch = data.get("markets", [])
                markets.extend(batch)
                
                # Check for more pages
                cursor = data.get("cursor")
                if not cursor or len(batch) == 0:
                    break
                    
        except Exception as e:
            print(f"Error: {e}")
            break
    
    return markets

def is_nba_moneyline(market):
    """Check if market is an NBA moneyline game"""
    title = market.get("title", "").lower()
    ticker = market.get("ticker", "")
    
    # Must contain NBA team names
    nba_teams = [
        "lakers", "warriors", "celtics", "nets", "knicks", "76ers", "sixers",
        "raptors", "bulls", "cavaliers", "cavs", "pistons", "pacers", "bucks",
        "hawks", "heat", "magic", "wizards", "nuggets", "timberwolves", "wolves",
        "thunder", "blazers", "jazz", "suns", "kings", "clippers", "grizzlies",
        "rockets", "pelicans", "spurs", "mavericks", "mavs", "hornets"
    ]
    
    has_nba_team = any(team in title for team in nba_teams)
    
    # Should be a winner/loser question
    is_winner_market = any(phrase in title for phrase in [
        "defeat", "beat", "win against", "winner of", "victorious"
    ])
    
    # Exclude parlays, totals, props
    is_parlay = "," in title and title.count("yes") > 1
    is_total = "total" in title and "point" in title
    is_prop = any(word in title for word in ["rebounds", "assists", "points", "threes", "double double"])
    
    return has_nba_team and is_winner_market and not is_parlay and not is_total and not is_prop

if __name__ == "__main__":
    print("Searching Kalshi for NBA Moneyline Markets...")
    print("=" * 80)
    
    markets = fetch_all_markets()
    print(f"Total markets fetched: {len(markets)}")
    
    # Filter for NBA moneylines
    nba_games = [m for m in markets if is_nba_moneyline(m)]
    
    print(f"NBA game markets found: {len(nba_games)}")
    print()
    
    if nba_games:
        print("NBA MONEYLINE MARKETS:")
        print("=" * 80)
        
        for i, market in enumerate(nba_games[:10], 1):
            yes_ask = market.get("yes_ask", 0)
            no_ask = market.get("no_ask", 0)
            
            print(f"\n{i}. {market['ticker']}")
            print(f"   Title: {market['title']}")
            if yes_ask:
                print(f"   Yes: {yes_ask/100:.2f} ({yes_ask}%)")
            if no_ask:
                print(f"   No:  {no_ask/100:.2f} ({no_ask}%)")
            print(f"   Volume: {market.get('volume', 0):,}")
    else:
        print("\nNo NBA moneyline markets found.")
        print("\nSearching for any basketball-related markets...")
        
        basketball = [m for m in markets if any(word in m.get("title", "").lower() for word in ["basketball", "nba", "lakers", "celtics"])]
        print(f"Found {len(basketball)} basketball-related markets")
        
        print("\nSample titles:")
        for m in basketball[:10]:
            print(f"  - {m.get('title', '')[:70]}")
