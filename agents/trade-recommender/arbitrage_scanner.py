#!/usr/bin/env python3
"""
Example arbitrage detection script for TradeRecommender
Uses DefeatBeta API, Kalshi API, and web search
"""

import os
import requests
import json
from datetime import datetime

# Configuration from environment variables
BRAVE_API_KEY = os.environ.get("BRAVE_API_KEY")
KALSHI_API_KEY_ID = os.environ.get("KALSHI_API_KEY_ID")
KALSHI_PRIVATE_KEY = os.environ.get("KALSHI_PRIVATE_KEY")

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

if __name__ == "__main__":
    print("=" * 60)
    print("TRADE RECOMMENDER - ARBITRAGE SCANNER")
    print("=" * 60)
    print(f"Mode: {'PAPER TRADING' if PAPER_TRADING else 'LIVE'}")
    print(f"Min Profit: {MIN_PROFIT_PCT}%")
    print()
    
    opps = detect_arbitrage_opportunities()
    
    if opps:
        print(f"\n{'='*60}")
        print(f"FOUND {len(opps)} OPPORTUNITIES")
        print(f"{'='*60}")
        
        for opp in opps:
            print(format_recommendation(opp))
    else:
        print("\nNo arbitrage opportunities found meeting criteria.")
