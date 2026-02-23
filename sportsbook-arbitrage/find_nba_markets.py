"""
Kalshi Market Explorer - Find NBA Game Markets
"""
import urllib.request
import json

API_BASE = "https://api.elections.kalshi.com/trade-api/v2"

def fetch_markets():
    """Fetch all open sports markets"""
    url = f"{API_BASE}/markets?status=open&limit=1000"
    
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data.get("markets", [])
    except Exception as e:
        print(f"Error: {e}")
        return []

def search_nba_games(markets):
    """Search for NBA game markets (not parlays)"""
    nba_games = []
    
    for market in markets:
        title = market.get("title", "").lower()
        ticker = market.get("ticker", "")
        
        # Look for single game markets (not multi-game parlays)
        # These typically have team names and simple yes/no structure
        nba_teams = [
            "lakers", "warriors", "celtics", "nets", "knicks", "76ers", "raptors",
            "bulls", "cavaliers", "pistons", "pacers", "bucks", "hawks", "heat",
            "magic", "wizards", "nuggets", "timberwolves", "thunder", "blazers",
            "jazz", "suns", "kings", "clippers", "grizzlies", "rockets", "pelicans",
            "spurs", "mavericks", "hornets"
        ]
        
        # Check if it's NBA related
        is_nba = any(team in title for team in nba_teams)
        
        # Exclude multi-game parlays (they have commas in title)
        is_single_game = "," not in title or title.count("wins") == 1
        
        if is_nba and is_single_game:
            nba_games.append({
                "ticker": ticker,
                "title": market.get("title"),
                "yes_ask": market.get("yes_ask"),
                "yes_bid": market.get("yes_bid"),
                "no_ask": market.get("no_ask"),
                "no_bid": market.get("no_bid"),
                "volume": market.get("volume", 0),
                "last_price": market.get("last_price"),
                "status": market.get("status")
            })
    
    return nba_games

if __name__ == "__main__":
    print("Fetching Kalshi markets...")
    print("=" * 80)
    
    markets = fetch_markets()
    print(f"Total markets: {len(markets)}")
    
    # Search for NBA games
    nba_games = search_nba_games(markets)
    print(f"NBA game markets found: {len(nba_games)}")
    print()
    
    if nba_games:
        print("NBA GAME MARKETS:")
        print("=" * 80)
        for game in nba_games[:10]:  # Show first 10
            print(f"\nTicker: {game['ticker']}")
            print(f"Title: {game['title']}")
            if game.get('yes_ask'):
                print(f"Yes: {game['yes_ask']/100:.2f} ({game['yes_ask']}%)")
            if game.get('no_ask'):
                print(f"No:  {game['no_ask']/100:.2f} ({game['no_ask']}%)")
            print(f"Volume: {game['volume']:,}")
            print(f"Status: {game['status']}")
    else:
        print("\nNo NBA game markets found in current listings.")
        print("\nSample of available markets:")
        for m in markets[:5]:
            print(f"  - {m.get('ticker')}: {m.get('title', '')[:60]}...")
