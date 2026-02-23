"""
Live Arbitrage Demo - Real Sportsbook + Manual Kalshi
Shows the full system working with live data
"""
from odds_fetcher import OddsAPIClient, OddsNormalizer
from kalshi_manual import KalshiManualInput
from arbitrage_scanner import ArbitrageScanner
from datetime import datetime

print("=" * 80)
print("LIVE ARBITRAGE SCANNER DEMO")
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
print("=" * 80)
print()

# Step 1: Fetch live sportsbook odds
print("📊 Fetching live sportsbook odds...")
client = OddsAPIClient()
normalizer = OddsNormalizer()

sportsbook_odds = client.get_odds(sport="basketball_nba", regions="us", markets="h2h")
print(f"✓ Retrieved {len(sportsbook_odds)} NBA games from sportsbooks")
print()

# Step 2: Load Kalshi markets (manual input mode)
print("📈 Loading Kalshi markets (manual input mode)...")
kalshi = KalshiManualInput()
kalshi.load_sample_nba_markets()
kalshi_data = [kalshi.to_dict(m) for m in kalshi.get_markets()]
print(f"✓ Loaded {len(kalshi_data)} Kalshi markets")
print()

# Step 3: Run arbitrage scan
print("🔍 Scanning for mispricings...")
scanner = ArbitrageScanner(threshold_pct=2.0, min_confidence=0.3)

# Manually compare first game as demo
game = sportsbook_odds[0]  # Wizards vs Pacers
best_odds = normalizer.extract_best_odds(game)

print(f"\nExample comparison for: {game['home_team']} vs {game['away_team']}")
print("-" * 70)

# Find matching Kalshi market
kalshi_market = kalshi_data[0]  # Wizards vs Pacers market

# Compare Wizards odds
wizards_book = best_odds.get('Washington Wizards')
wizards_kalshi_prob = kalshi_market['yes_ask'] / 100  # Yes = home team

if wizards_book:
    print(f"\nWashington Wizards:")
    print(f"  Sportsbook: {wizards_book['price']:.2f} ({wizards_book['implied_prob']*100:.1f}%)")
    print(f"  Kalshi:     ${wizards_kalshi_prob:.2f} ({wizards_kalshi_prob*100:.1f}%)")
    mispricing = abs(wizards_book['implied_prob'] - wizards_kalshi_prob)
    print(f"  Mispricing: {mispricing*100:.2f}%")
    
    if mispricing > 0.02:
        print(f"  ⚠️  OPPORTUNITY DETECTED!")
        if wizards_book['implied_prob'] > wizards_kalshi_prob:
            print(f"      → Sportsbook overprices Wizards")
            print(f"      → Buy on Kalshi at ${wizards_kalshi_prob:.2f}")
        else:
            print(f"      → Kalshi overprices Wizards")
            print(f"      → Bet at sportsbook at {wizards_book['price']:.2f}")

# Compare Pacers odds
pacers_book = best_odds.get('Indiana Pacers')
pacers_kalshi_prob = kalshi_market['no_ask'] / 100  # No = away team

if pacers_book:
    print(f"\nIndiana Pacers:")
    print(f"  Sportsbook: {pacers_book['price']:.2f} ({pacers_book['implied_prob']*100:.1f}%)")
    print(f"  Kalshi:     ${pacers_kalshi_prob:.2f} ({pacers_kalshi_prob*100:.1f}%)")
    mispricing = abs(pacers_book['implied_prob'] - pacers_kalshi_prob)
    print(f"  Mispricing: {mispricing*100:.2f}%")
    
    if mispricing > 0.02:
        print(f"  ⚠️  OPPORTUNITY DETECTED!")

print()
print("=" * 80)
print("SYSTEM READY")
print("=" * 80)
print()
print("To run with live Kalshi data:")
print("1. Get Kalshi API credentials")
print("2. Update kalshi_connector.py with auth")
print("3. Or manually input current Kalshi prices in kalshi_manual.py")
print()
print("Files:")
print("  - live_odds_test.py    : View live sportsbook odds")
print("  - kalshi_manual.py     : Input Kalshi prices manually")
print("  - arbitrage_scanner.py : Detection engine")
print("  - main.py              : Full orchestrator")
