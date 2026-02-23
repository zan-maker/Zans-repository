"""
Live Odds Test - Fetch and display current sportsbook odds
"""
from odds_fetcher import OddsAPIClient, OddsNormalizer
from datetime import datetime

client = OddsAPIClient()
normalizer = OddsNormalizer()

print("LIVE SPORTSBOOK ODDS")
print("=" * 80)
print(f"Fetched: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
print("=" * 80)
print()

# Get NBA odds
odds = client.get_odds(sport="basketball_nba", regions="us", markets="h2h")

print(f"Found {len(odds)} upcoming NBA games\n")

for i, game in enumerate(odds[:5], 1):  # Show first 5 games
    home = game['home_team']
    away = game['away_team']
    commence = game['commence_time']
    
    print(f"GAME {i}: {away} @ {home}")
    print(f"Time: {commence}")
    print(f"Bookmakers: {len(game.get('bookmakers', []))}")
    
    best_odds = normalizer.extract_best_odds(game)
    
    print("Best Odds (Moneyline):")
    for team, data in best_odds.items():
        american = int((data['price'] - 1) * 100) if data['price'] >= 2 else int(-100 / (data['price'] - 1))
        print(f"  {team:25} {data['price']:.2f} ({american:+d}) @ {data['bookmaker']}")
    
    # Calculate vig-free probabilities
    probs = [data['implied_prob'] for data in best_odds.values()]
    if len(probs) == 2:
        true_probs = normalizer.remove_vig(probs[0], probs[1])
        print(f"True Probabilities (vig removed): {true_probs[0]*100:.1f}% / {true_probs[1]*100:.1f}%")
    
    print()

print("=" * 80)
print("Ready for Kalshi comparison once Kalshi auth is configured")
