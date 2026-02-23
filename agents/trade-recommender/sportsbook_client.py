#!/usr/bin/env python3
"""
Sportsbook API Client (RapidAPI)
Fetches odds from multiple sportsbooks for arbitrage detection with Kalshi.

API: https://rapidapi.com/sportsbook-api-sportsbook-api-default/api/sportsbook-api2
"""

import os
import time
import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import requests
from urllib.parse import urlencode


@dataclass
class OddsData:
    """Standardized odds data structure"""
    book: str
    market_type: str  # moneyline, spread, total
    outcome: str
    odds_american: int
    odds_decimal: float
    implied_probability: float
    timestamp: str


@dataclass
class GameEvent:
    """Canonical game event structure"""
    id: str
    sport: str
    league: str
    home_team: str
    away_team: str
    start_time: str
    odds: List[OddsData]


class SportsbookAPIClient:
    """
    Client for RapidAPI Sportsbook API
    Provides unified interface to fetch odds from multiple sportsbooks
    """
    
    BASE_URL = "https://sportsbook-api2.p.rapidapi.com"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Sportsbook API client
        
        Args:
            api_key: RapidAPI key (defaults to RAPIDAPI_KEY env var)
        """
        self.api_key = api_key or os.getenv('RAPIDAPI_KEY')
        if not self.api_key:
            raise ValueError("RapidAPI key required. Set RAPIDAPI_KEY environment variable.")
        
        self.headers = {
            'X-RapidAPI-Key': self.api_key,
            'X-RapidAPI-Host': 'sportsbook-api2.p.rapidapi.com'
        }
        
        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 0.6  # Max ~100 requests/minute on free tier
        
        # Cache
        self._cache = {}
        self._cache_ttl = 300  # 5 minute cache
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """
        Make rate-limited request to API
        
        Args:
            endpoint: API endpoint path
            params: Query parameters
            
        Returns:
            JSON response as dict
        """
        # Rate limiting
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_request_interval:
            time.sleep(self.min_request_interval - elapsed)
        
        url = f"{self.BASE_URL}/{endpoint}"
        if params:
            url += "?" + urlencode(params)
        
        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            self.last_request_time = time.time()
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"❌ API request failed: {e}")
            raise
    
    def get_sports(self) -> List[Dict]:
        """
        Get list of available sports
        
        Returns:
            List of sport objects with id and name
        """
        cache_key = "sports"
        if self._is_cached(cache_key):
            return self._get_cache(cache_key)
        
        data = self._make_request("sports")
        self._set_cache(cache_key, data)
        return data
    
    def get_leagues(self, sport: str) -> List[Dict]:
        """
        Get leagues for a specific sport
        
        Args:
            sport: Sport ID (e.g., 'basketball', 'football')
            
        Returns:
            List of league objects
        """
        cache_key = f"leagues_{sport}"
        if self._is_cached(cache_key):
            return self._get_cache(cache_key)
        
        data = self._make_request("leagues", {"sport": sport})
        self._set_cache(cache_key, data)
        return data
    
    def get_games(self, league: str, date: Optional[str] = None) -> List[Dict]:
        """
        Get games/events for a league
        
        Args:
            league: League ID (e.g., 'NBA', 'NFL')
            date: Optional date filter (YYYY-MM-DD)
            
        Returns:
            List of game objects
        """
        params = {"league": league}
        if date:
            params["date"] = date
        
        cache_key = f"games_{league}_{date or 'today'}"
        if self._is_cached(cache_key):
            return self._get_cache(cache_key)
        
        data = self._make_request("games", params)
        self._set_cache(cache_key, data)
        return data
    
    def get_odds(self, game_id: str) -> Dict:
        """
        Get odds for a specific game
        
        Args:
            game_id: Game/event ID
            
        Returns:
            Odds data across multiple sportsbooks
        """
        cache_key = f"odds_{game_id}"
        if self._is_cached(cache_key):
            return self._get_cache(cache_key)
        
        data = self._make_request("odds", {"gameId": game_id})
        self._set_cache(cache_key, data)
        return data
    
    def get_markets(self, game_id: str) -> List[Dict]:
        """
        Get available betting markets for a game
        
        Args:
            game_id: Game/event ID
            
        Returns:
            List of available markets
        """
        cache_key = f"markets_{game_id}"
        if self._is_cached(cache_key):
            return self._get_cache(cache_key)
        
        data = self._make_request("markets", {"gameId": game_id})
        self._set_cache(cache_key, data)
        return data
    
    def get_books(self) -> List[Dict]:
        """
        Get list of supported sportsbooks
        
        Returns:
            List of bookmaker objects
        """
        cache_key = "books"
        if self._is_cached(cache_key):
            return self._get_cache(cache_key)
        
        data = self._make_request("books")
        self._set_cache(cache_key, data)
        return data
    
    def get_live_odds(self, game_id: str) -> Dict:
        """
        Get live/in-play odds for a game
        
        Args:
            game_id: Game/event ID
            
        Returns:
            Live odds data
        """
        cache_key = f"live_{game_id}"
        if self._is_cached(cache_key):
            return self._get_cache(cache_key)
        
        data = self._make_request("live", {"gameId": game_id})
        self._set_cache(cache_key, data)
        return data
    
    # ============ UTILITY METHODS ============
    
    @staticmethod
    def american_to_decimal(american_odds: int) -> float:
        """Convert American odds to decimal"""
        if american_odds > 0:
            return (american_odds / 100) + 1
        else:
            return (100 / abs(american_odds)) + 1
    
    @staticmethod
    def american_to_probability(american_odds: int) -> float:
        """Convert American odds to implied probability"""
        if american_odds > 0:
            return 100 / (american_odds + 100)
        else:
            return abs(american_odds) / (abs(american_odds) + 100)
    
    @staticmethod
    def remove_vig(probabilities: List[float]) -> List[float]:
        """Remove vig (sportsbook margin) from implied probabilities"""
        total = sum(probabilities)
        return [p / total for p in probabilities]
    
    @staticmethod
    def calculate_hold(probabilities: List[float]) -> float:
        """Calculate sportsbook hold percentage"""
        total = sum(probabilities)
        return (total - 1) * 100
    
    def parse_odds_to_canonical(self, odds_data: Dict) -> List[OddsData]:
        """
        Parse API odds response to canonical OddsData format
        
        Args:
            odds_data: Raw odds response from API
            
        Returns:
            List of OddsData objects
        """
        canonical = []
        timestamp = datetime.now().isoformat()
        
        for book_name, book_data in odds_data.items():
            if not isinstance(book_data, dict):
                continue
            
            # Parse moneyline
            if 'moneyline' in book_data:
                for outcome, odds in book_data['moneyline'].items():
                    canonical.append(OddsData(
                        book=book_name,
                        market_type='moneyline',
                        outcome=outcome,
                        odds_american=odds,
                        odds_decimal=self.american_to_decimal(odds),
                        implied_probability=self.american_to_probability(odds),
                        timestamp=timestamp
                    ))
            
            # Parse spread
            if 'spread' in book_data:
                for outcome, data in book_data['spread'].items():
                    if isinstance(data, dict):
                        canonical.append(OddsData(
                            book=book_name,
                            market_type='spread',
                            outcome=f"{outcome} {data.get('line', '')}",
                            odds_american=data.get('odds', 0),
                            odds_decimal=self.american_to_decimal(data.get('odds', 0)),
                            implied_probability=self.american_to_probability(data.get('odds', 0)),
                            timestamp=timestamp
                        ))
            
            # Parse totals
            if 'totals' in book_data:
                for outcome, data in book_data['totals'].items():
                    if isinstance(data, dict):
                        canonical.append(OddsData(
                            book=book_name,
                            market_type='total',
                            outcome=f"{outcome} {data.get('line', '')}",
                            odds_american=data.get('odds', 0),
                            odds_decimal=self.american_to_decimal(data.get('odds', 0)),
                            implied_probability=self.american_to_probability(data.get('odds', 0)),
                            timestamp=timestamp
                        ))
        
        return canonical
    
    def find_best_odds(self, odds_list: List[OddsData], market_type: str = None) -> Dict[str, OddsData]:
        """
        Find best odds for each outcome
        
        Args:
            odds_list: List of OddsData
            market_type: Optional filter by market type
            
        Returns:
            Dict mapping outcome -> best OddsData
        """
        best = {}
        
        for odds in odds_list:
            if market_type and odds.market_type != market_type:
                continue
            
            outcome = odds.outcome
            if outcome not in best or odds.odds_decimal > best[outcome].odds_decimal:
                best[outcome] = odds
        
        return best
    
    # ============ CACHE METHODS ============
    
    def _is_cached(self, key: str) -> bool:
        """Check if key is in cache and not expired"""
        if key not in self._cache:
            return False
        
        cached_time, data = self._cache[key]
        if time.time() - cached_time > self._cache_ttl:
            del self._cache[key]
            return False
        
        return True
    
    def _get_cache(self, key: str):
        """Get cached data"""
        return self._cache[key][1]
    
    def _set_cache(self, key: str, data):
        """Set cache entry"""
        self._cache[key] = (time.time(), data)
    
    def clear_cache(self):
        """Clear all cached data"""
        self._cache.clear()


class SportsbookKalshiArbitrage:
    """
    Specialized class for detecting arbitrage between Sportsbook odds and Kalshi markets
    """
    
    def __init__(self, sportsbook_client: SportsbookAPIClient, kalshi_client=None):
        self.sb = sportsbook_client
        self.kalshi = kalshi_client
    
    def find_arbitrage(self, game_id: str, kalshi_market: Dict) -> Optional[Dict]:
        """
        Find arbitrage between sportsbook odds and Kalshi market
        
        Args:
            game_id: Sportsbook game ID
            kalshi_market: Kalshi market data with yes/no prices
            
        Returns:
            Arbitrage opportunity if found, None otherwise
        """
        # Get sportsbook odds
        odds_data = self.sb.get_odds(game_id)
        canonical_odds = self.sb.parse_odds_to_canonical(odds_data)
        
        # Get best moneyline odds
        best_odds = self.sb.find_best_odds(canonical_odds, 'moneyline')
        
        opportunities = []
        
        # Compare with Kalshi yes/no prices
        if kalshi_market and 'yes_price' in kalshi_market and 'no_price' in kalshi_market:
            kalshi_yes_prob = kalshi_market['yes_price'] / 10000  # Kalshi prices in cents
            kalshi_no_prob = kalshi_market['no_price'] / 10000
            
            # Check each sportsbook outcome
            for outcome, odds in best_odds.items():
                sb_prob = odds.implied_probability
                
                # Case 1: Kalshi YES < Sportsbook NO implied (bet YES on Kalshi, bet outcome on book)
                if 'yes' in outcome.lower() or outcome == kalshi_market.get('yes_outcome', ''):
                    if kalshi_yes_prob < (1 - sb_prob):  # Arbitrage condition
                        profit = self._calc_arbitrage_profit(kalshi_yes_prob, 1 - sb_prob)
                        if profit > 0:
                            opportunities.append({
                                'type': 'arbitrage',
                                'direction': 'kalshi_yes_book_outcome',
                                'game': game_id,
                                'profit_pct': profit,
                                'kalshi_price': kalshi_yes_prob,
                                'sportsbook_odds': odds.odds_american,
                                'sportsbook_implied': sb_prob
                            })
                
                # Case 2: Kalshi NO < Sportsbook YES implied
                elif 'no' in outcome.lower() or outcome == kalshi_market.get('no_outcome', ''):
                    if kalshi_no_prob < sb_prob:  # Arbitrage condition
                        profit = self._calc_arbitrage_profit(kalshi_no_prob, sb_prob)
                        if profit > 0:
                            opportunities.append({
                                'type': 'arbitrage',
                                'direction': 'kalshi_no_book_yes',
                                'game': game_id,
                                'profit_pct': profit,
                                'kalshi_price': kalshi_no_prob,
                                'sportsbook_odds': odds.odds_american,
                                'sportsbook_implied': sb_prob
                            })
        
        # Return best opportunity
        if opportunities:
            return max(opportunities, key=lambda x: x['profit_pct'])
        
        return None
    
    def _calc_arbitrage_profit(self, prob_a: float, prob_b: float) -> float:
        """Calculate arbitrage profit percentage"""
        # Stake $100 total, split based on odds
        odds_a = 1 / prob_a
        odds_b = 1 / prob_b
        
        stake_a = 100 * odds_b / (odds_a + odds_b)
        stake_b = 100 - stake_a
        
        payout_a = stake_a * odds_a
        payout_b = stake_b * odds_b
        
        min_payout = min(payout_a, payout_b)
        profit = min_payout - 100
        
        return (profit / 100) * 100  # Return as percentage


# ============ CLI INTERFACE ============

if __name__ == "__main__":
    import sys
    
    # Initialize client
    try:
        client = SportsbookAPIClient()
    except ValueError as e:
        print(f"❌ {e}")
        sys.exit(1)
    
    command = sys.argv[1] if len(sys.argv) > 1 else "help"
    
    if command == "sports":
        sports = client.get_sports()
        print(json.dumps(sports, indent=2))
    
    elif command == "leagues":
        if len(sys.argv) < 3:
            print("Usage: python sportsbook_client.py leagues <sport>")
            sys.exit(1)
        leagues = client.get_leagues(sys.argv[2])
        print(json.dumps(leagues, indent=2))
    
    elif command == "games":
        if len(sys.argv) < 3:
            print("Usage: python sportsbook_client.py games <league> [date]")
            sys.exit(1)
        date = sys.argv[3] if len(sys.argv) > 3 else None
        games = client.get_games(sys.argv[2], date)
        print(json.dumps(games, indent=2))
    
    elif command == "odds":
        if len(sys.argv) < 3:
            print("Usage: python sportsbook_client.py odds <game_id>")
            sys.exit(1)
        odds = client.get_odds(sys.argv[2])
        canonical = client.parse_odds_to_canonical(odds)
        for o in canonical[:10]:  # Show first 10
            print(f"{o.book:15} | {o.market_type:10} | {o.outcome:20} | {o.odds_american:+4d} | {o.implied_probability:.2%}")
    
    elif command == "books":
        books = client.get_books()
        print(json.dumps(books, indent=2))
    
    elif command == "best":
        if len(sys.argv) < 3:
            print("Usage: python sportsbook_client.py best <game_id>")
            sys.exit(1)
        odds = client.get_odds(sys.argv[2])
        canonical = client.parse_odds_to_canonical(odds)
        best = client.find_best_odds(canonical)
        for outcome, odds in best.items():
            print(f"{outcome:25} | {odds.book:15} | {odds.odds_american:+4d} | {odds.implied_probability:.2%}")
    
    else:
        print("""
Sportsbook API Client (RapidAPI)

Usage:
    python sportsbook_client.py <command> [args]

Commands:
    sports              List available sports
    leagues <sport>     List leagues for sport
    games <league>      List games for league
    odds <game_id>      Get odds for game
    books               List supported sportsbooks
    best <game_id>      Find best odds for each outcome

Environment:
    RAPIDAPI_KEY        Required. Get from RapidAPI dashboard.

Examples:
    python sportsbook_client.py sports
    python sportsbook_client.py leagues basketball
    python sportsbook_client.py games NBA
    python sportsbook_client.py odds abc123
        """)
