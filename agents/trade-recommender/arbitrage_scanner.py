#!/usr/bin/env python3
"""
Example arbitrage detection script for TradeRecommender
Uses DefeatBeta API, Kalshi API, Sportsbook API, and web search
"""

import os
import sys
import requests
import json
from datetime import datetime

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import Sportsbook API client
try:
    from sportsbook_client import SportsbookAPIClient, SportsbookKalshiArbitrage
    SPORTSBOOK_AVAILABLE = True
except ImportError:
    SPORTSBOOK_AVAILABLE = False
    print("⚠️  Sportsbook client not available")

# Configuration from environment variables
BRAVE_API_KEY = os.environ.get("BRAVE_API_KEY")
KALSHI_API_KEY_ID = os.environ.get("KALSHI_API_KEY_ID", "fb109d35-efc3-42b1-bdba-0ee2a1e90ef8")
KALSHI_PRIVATE_KEY_PATH = os.environ.get("KALSHI_PRIVATE_KEY_PATH", "./keys/kalshi_private.pem")
RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY")

# Safety parameters
MIN_PROFIT_PCT = 0.5
MAX_POSITION_SIZE = 10
PAPER_TRADING = True

def search_news(query):
    """Use Brave Search to find relevant news"""
    headers = {"X-Subscription-Token": BRAVE_API_KEY}
    params = {"q": query, "count": 5}
    
    try:
        response = requests.get(
            "https://api.search.brave.com/res/v1/news/search",
            headers=headers,
            params=params,
            timeout=10
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def get_kalshi_markets():
    """Fetch available Kalshi markets"""
    headers = {"Authorization": f"Bearer {KALSHI_API_KEY_ID}"}
    
    try:
        response = requests.get(
            "https://trading-api.kalshi.com/trade-api/v2/markets",
            headers=headers,
            timeout=10
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def get_kalshi_orderbook(market_id):
    """Fetch orderbook for specific market"""
    headers = {"Authorization": f"Bearer {KALSHI_API_KEY_ID}"}
    
    try:
        response = requests.get(
            f"https://trading-api.kalshi.com/trade-api/v2/markets/{market_id}/orderbook",
            headers=headers,
            timeout=10
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def detect_arbitrage_opportunities():
    """
    Main arbitrage detection logic
    1. Fetch market data from Kalshi
    2. Search for relevant news
    3. Identify mispricings
    4. Output recommendations
    """
    opportunities = []
    
    # Step 1: Get markets
    print("Fetching Kalshi markets...")
    markets = get_kalshi_markets()
    
    if "error" in markets:
        print(f"Error fetching markets: {markets['error']}")
        return opportunities
    
    # Step 2: Analyze each market
    for market in markets.get("markets", [])[:10]:  # Check first 10
        market_id = market.get("id")
        title = market.get("title")
        
        print(f"\nAnalyzing: {title}")
        
        # Get orderbook
        orderbook = get_kalshi_orderbook(market_id)
        
        if "error" in orderbook:
            continue
        
        # Extract best bid/ask
        bids = orderbook.get("bids", [])
        asks = orderbook.get("asks", [])
        
        if not bids or not asks:
            continue
        
        best_bid = bids[0].get("price", 0) / 100  # Convert from cents
        best_ask = asks[0].get("price", 0) / 100
        
        # Check for arbitrage (buy YES + buy NO < 1)
        implied_no_ask = 1 - best_bid
        
        if (best_ask + implied_no_ask) < (1 - MIN_PROFIT_PCT/100):
            profit = (1 - best_ask - implied_no_ask) * 100
            
            # Search for news
            news = search_news(f"{title} news")
            
            opportunity = {
                "market_id": market_id,
                "title": title,
                "type": "Kalshi Arbitrage",
                "profit_pct": profit,
                "buy_yes_at": best_ask,
                "buy_no_at": implied_no_ask,
                "timestamp": datetime.now().isoformat(),
                "news_context": news,
                "confidence": 7 if profit > 1 else 5,
                "recommendation": "EXPLORE" if PAPER_TRADING else "REVIEW"
            }
            
            opportunities.append(opportunity)
            print(f"  ✓ Opportunity found: {profit:.2f}% profit")
    
    return opportunities

def format_recommendation(opp):
    """Format opportunity for Sam"""
    return f"""
ARBITRAGE OPPORTUNITY DETECTED

Market: {opp['title']}
Type: {opp['type']}
Expected Profit: {opp['profit_pct']:.2f}%

Entry Points:
- Buy YES at: {opp['buy_yes_at']:.2f}
- Buy NO at: {opp['buy_no_at']:.2f}

Confidence: {opp['confidence']}/10
Status: {opp['recommendation']}

News Context:
{json.dumps(opp['news_context'], indent=2)[:500]}

Timestamp: {opp['timestamp']}
"""

def scan_sportsbook_kalshi_arbitrage():
    """
    Scan for arbitrage between Sportsbook odds and Kalshi markets
    Returns list of opportunities
    """
    opportunities = []
    
    if not SPORTSBOOK_AVAILABLE or not RAPIDAPI_KEY:
        print("⚠️  Sportsbook API not configured. Skipping sportsbook scan.")
        return opportunities
    
    try:
        # Initialize Sportsbook client
        sb_client = SportsbookAPIClient(RAPIDAPI_KEY)
        arb_finder = SportsbookKalshiArbitrage(sb_client)
        
        print("\nFetching available sports...")
        sports = sb_client.get_sports()
        
        # Focus on major sports with Kalshi markets
        target_sports = ['basketball', 'football', 'baseball', 'hockey']
        
        for sport in sports:
            sport_id = sport.get('id', '').lower()
            if sport_id not in target_sports:
                continue
            
            print(f"\nScanning {sport.get('name', sport_id)}...")
            
            try:
                # Get leagues for this sport
                leagues = sb_client.get_leagues(sport_id)
                
                for league in leagues[:2]:  # Check first 2 leagues
                    league_id = league.get('id')
                    
                    try:
                        # Get games
                        games = sb_client.get_games(league_id)
                        
                        for game in games[:3]:  # Check first 3 games
                            game_id = game.get('id')
                            game_title = f"{game.get('home_team', '')} vs {game.get('away_team', '')}"
                            
                            print(f"  Checking: {game_title}")
                            
                            # Get odds
                            odds_data = sb_client.get_odds(game_id)
                            canonical_odds = sb_client.parse_odds_to_canonical(odds_data)
                            
                            # Find best odds
                            best_odds = sb_client.find_best_odds(canonical_odds, 'moneyline')
                            
                            # Check for value opportunities (odds differ significantly)
                            for outcome, odds in best_odds.items():
                                # Calculate no-vig probability
                                all_probs = [o.implied_probability for o in canonical_odds 
                                           if o.outcome == outcome]
                                if len(all_probs) >= 2:
                                    max_prob = max(all_probs)
                                    min_prob = min(all_probs)
                                    spread = (max_prob - min_prob) * 100
                                    
                                    if spread > 2.0:  # 2%+ spread
                                        opportunity = {
                                            "game": game_title,
                                            "type": "Sportsbook Value",
                                            "outcome": outcome,
                                            "best_book": odds.book,
                                            "best_odds": odds.odds_american,
                                            "best_implied": odds.implied_probability,
                                            "spread_pct": spread,
                                            "profit_pct": spread * 0.5,  # Estimate
                                            "timestamp": datetime.now().isoformat(),
                                            "confidence": 6 if spread > 3 else 5,
                                            "recommendation": "EXPLORE"
                                        }
                                        opportunities.append(opportunity)
                                        print(f"    ✓ Value found: {spread:.2f}% spread on {outcome}")
                                        
                    except Exception as e:
                        print(f"    Error scanning games: {e}")
                        continue
                        
            except Exception as e:
                print(f"  Error scanning leagues: {e}")
                continue
                
    except Exception as e:
        print(f"❌ Sportsbook scan error: {e}")
    
    return opportunities

if __name__ == "__main__":
    print("=" * 60)
    print("TRADE RECOMMENDER - ARBITRAGE SCANNER")
    print("=" * 60)
    print(f"Mode: {'PAPER TRADING' if PAPER_TRADING else 'LIVE'}")
    print(f"Min Profit: {MIN_PROFIT_PCT}%")
    print(f"Sources: Kalshi API + Sportsbook API (RapidAPI)")
    print()
    
    all_opportunities = []
    
    # Scan 1: Kalshi internal arbitrage
    print("\n" + "-" * 60)
    print("SCAN 1: Kalshi Internal Arbitrage")
    print("-" * 60)
    kalshi_opps = detect_arbitrage_opportunities()
    all_opportunities.extend(kalshi_opps)
    
    # Scan 2: Sportsbook value opportunities
    print("\n" + "-" * 60)
    print("SCAN 2: Sportsbook Value Opportunities")
    print("-" * 60)
    sportsbook_opps = scan_sportsbook_kalshi_arbitrage()
    all_opportunities.extend(sportsbook_opps)
    
    # Results
    print("\n" + "=" * 60)
    print(f"SCAN COMPLETE")
    print("=" * 60)
    print(f"Kalshi opportunities: {len(kalshi_opps)}")
    print(f"Sportsbook opportunities: {len(sportsbook_opps)}")
    print(f"Total: {len(all_opportunities)}")
    
    if all_opportunities:
        print(f"\n{'='*60}")
        print(f"DETAILED OPPORTUNITIES")
        print(f"{'='*60}")
        
        for opp in all_opportunities:
            print(format_recommendation(opp))
    else:
        print("\nNo arbitrage opportunities found meeting criteria.")
