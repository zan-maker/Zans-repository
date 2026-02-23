"""
Complete Arbitrage System - Live Sportsbook + Kalshi
"""
from odds_fetcher import OddsAPIClient, OddsNormalizer
from datetime import datetime
import json

# Kalshi API Base
KALSHI_API_BASE = "https://api.elections.kalshi.com/trade-api/v2"

def fetch_kalshi_market(ticker):
    """Fetch a specific Kalshi market"""
    import urllib.request
    url = f"{KALSHI_API_BASE}/markets/{ticker}"
    
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode('utf-8'))
    except:
        return None

def find_kalshi_markets_by_query(query):
    """Search Kalshi markets by keyword"""
    import urllib.request
    url = f"{KALSHI_API_BASE}/markets?status=open&limit=100"
    
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            markets = data.get("markets", [])
            
            # Filter by query
            matching = []
            for m in markets:
                title = m.get("title", "").lower()
                if query.lower() in title:
                    matching.append({
                        "ticker": m.get("ticker"),
                        "title": m.get("title"),
                        "yes_price": m.get("yes_ask", 0) / 100 if m.get("yes_ask") else None,
                        "no_price": m.get("no_ask", 0) / 100 if m.get("no_ask") else None,
                        "volume": m.get("volume", 0)
                    })
            
            return matching
    except Exception as e:
        print(f"Error: {e}")
        return []

def run_full_scan():
    """Run complete arbitrage scan"""
    print("=" * 80)
    print("SPORTSBOOK-KALSHI ARBITRAGE SCANNER")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("=" * 80)
    print()
    
    # Step 1: Fetch live sportsbook odds
    print("📊 Fetching live sportsbook odds...")
    client = OddsAPIClient()
    normalizer = OddsNormalizer()
    
    odds = client.get_odds(sport="basketball_nba", regions="us", markets="h2h")
    print(f"✓ Retrieved {len(odds)} NBA games")
    print()
    
    # Step 2: For each game, try to find matching Kalshi market
    print("🔍 Scanning for Kalshi markets and calculating mispricings...")
    print("-" * 80)
    
    opportunities = []
    
    for game in odds[:5]:  # Check first 5 games
        home = game['home_team']
        away = game['away_team']
        commence = game['commence_time']
        
        print(f"\n{away} @ {home}")
        print(f"Game time: {commence}")
        
        # Get best odds
        best_odds = normalizer.extract_best_odds(game)
        
        # Try to find matching Kalshi market
        # Search by home team name
        home_short = home.split()[-1].lower()  # Get last word (team name)
        kalshi_markets = find_kalshi_markets_by_query(home_short)
        
        if kalshi_markets:
            print(f"  Found {len(kalshi_markets)} potential Kalshi matches")
            
            # Show the best match
            match = kalshi_markets[0]
            print(f"  Kalshi: {match['title'][:60]}...")
            print(f"  Yes: ${match['yes_price']:.2f} | No: ${match['no_price']:.2f}")
            
            # Compare odds
            for team, data in best_odds.items():
                book_prob = data['implied_prob']
                american = int((data['price'] - 1) * 100) if data['price'] >= 2 else int(-100 / (data['price'] - 1))
                print(f"  {team}: {data['price']:.2f} ({american:+d}) @ {data['bookmaker']} = {book_prob*100:.1f}%")
                
                # Calculate mispricing if we have matching Kalshi data
                if match['yes_price'] and team == home:
                    kalshi_prob = match['yes_price']
                    diff = abs(book_prob - kalshi_prob)
                    print(f"    vs Kalshi Yes: {kalshi_prob*100:.1f}% | Diff: {diff*100:.2f}%")
                    if diff > 0.03:
                        print(f"    ⚠️  OPPORTUNITY: {diff*100:.1f}% edge")
                        opportunities.append({
                            'game': f"{away} @ {home}",
                            'team': team,
                            'diff': diff,
                            'book_odds': data['price'],
                            'kalshi_price': kalshi_prob
                        })
                elif match['no_price'] and team == away:
                    kalshi_prob = match['no_price']
                    diff = abs(book_prob - kalshi_prob)
                    print(f"    vs Kalshi No: {kalshi_prob*100:.1f}% | Diff: {diff*100:.2f}%")
                    if diff > 0.03:
                        print(f"    ⚠️  OPPORTUNITY: {diff*100:.1f}% edge")
                        opportunities.append({
                            'game': f"{away} @ {home}",
                            'team': team,
                            'diff': diff,
                            'book_odds': data['price'],
                            'kalshi_price': kalshi_prob
                        })
        else:
            print(f"  No Kalshi market found (searching: '{home_short}')")
            # Show odds anyway
            for team, data in best_odds.items():
                american = int((data['price'] - 1) * 100) if data['price'] >= 2 else int(-100 / (data['price'] - 1))
                print(f"  {team}: {data['price']:.2f} ({american:+d}) @ {data['bookmaker']}")
    
    # Summary
    print()
    print("=" * 80)
    print("SCAN SUMMARY")
    print("=" * 80)
    print(f"Games analyzed: {len(odds)}")
    print(f"Opportunities found: {len(opportunities)}")
    
    if opportunities:
        print("\nOPPORTUNITIES:")
        for opp in opportunities:
            print(f"  {opp['game']} - {opp['team']}: {opp['diff']*100:.1f}% edge")
    else:
        print("\nNo arbitrage opportunities detected above 3% threshold.")
        print("\nNotes:")
        print("- Kalshi NBA game markets may use different naming conventions")
        print("- Try searching Kalshi website directly for game tickers")
        print("- Markets may have closed for immediate games")
    
    return opportunities

if __name__ == "__main__":
    opportunities = run_full_scan()
