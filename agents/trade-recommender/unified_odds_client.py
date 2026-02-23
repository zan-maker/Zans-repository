#!/usr/bin/env python3
"""
Unified Sportsbook API Client with Failover
Supports RapidAPI Sportsbook API (primary) and The Odds API (backup)
"""

import os
import time
import json
from typing import Dict, List, Optional, Union
from dataclasses import dataclass
from datetime import datetime
import requests
from urllib.parse import urlencode


@dataclass
class OddsData:
    """Standardized odds data structure"""
    book: str
    market_type: str  # h2h/moneyline, spreads, totals
    outcome: str
    odds_american: int
    odds_decimal: float
    implied_probability: float
    timestamp: str
    source_api: str  # 'rapidapi' or 'theoddsapi'


class TheOddsAPIClient:
    """
    Client for The Odds API (backup provider)
    https://the-odds-api.com/
    """
    
    BASE_URL = "https://api.the-odds-api.com/v4"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('THE_ODDS_API_KEY')
        if not self.api_key:
            raise ValueError("The Odds API key required")
        
        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 0.5  # Max ~120 requests/minute
        
        # Cache
        self._cache = {}
        self._cache_ttl = 300  # 5 minute cache
        
        # Track usage
        self.requests_remaining = None
        self.requests_used = None
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """Make rate-limited request to API"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_request_interval:
            time.sleep(self.min_request_interval - elapsed)
        
        url = f"{self.BASE_URL}/{endpoint}"
        
        # Add API key to params
        request_params = params.copy() if params else {}
        request_params['apiKey'] = self.api_key
        
        try:
            response = requests.get(url, params=request_params, timeout=30)
            self.last_request_time = time.time()
            
            # Track rate limits from headers
            self.requests_remaining = response.headers.get('x-requests-remaining')
            self.requests_used = response.headers.get('x-requests-used')
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"❌ The Odds API request failed: {e}")
            raise
    
    def get_sports(self, all_sports: bool = False) -> List[Dict]:
        """Get list of sports"""
        cache_key = f"sports_theodds_{all_sports}"
        if self._is_cached(cache_key):
            return self._get_cache(cache_key)
        
        params = {"all": "true"} if all_sports else {}
        data = self._make_request("sports", params)
        self._set_cache(cache_key, data)
        return data
    
    def get_odds(self, sport: str, regions: str = "us", markets: str = "h2h",
                 odds_format: str = "american", date_format: str = "iso") -> List[Dict]:
        """
        Get odds for a sport
        
        Args:
            sport: Sport key (e.g., 'basketball_nba', 'americanfootball_nfl')
            regions: Comma-separated regions (us, us2, uk, au, eu)
            markets: Comma-separated markets (h2h, spreads, totals, outrights)
            odds_format: 'decimal' or 'american'
            date_format: 'iso' or 'unix'
        """
        cache_key = f"odds_theodds_{sport}_{regions}_{markets}"
        if self._is_cached(cache_key):
            return self._get_cache(cache_key)
        
        params = {
            "regions": regions,
            "markets": markets,
            "oddsFormat": odds_format,
            "dateFormat": date_format
        }
        
        data = self._make_request(f"sports/{sport}/odds", params)
        self._set_cache(cache_key, data)
        return data
    
    def get_events(self, sport: str, date_format: str = "iso") -> List[Dict]:
        """Get events for a sport"""
        cache_key = f"events_theodds_{sport}"
        if self._is_cached(cache_key):
            return self._get_cache(cache_key)
        
        params = {"dateFormat": date_format}
        data = self._make_request(f"sports/{sport}/events", params)
        self._set_cache(cache_key, data)
        return data
    
    def get_event_odds(self, sport: str, event_id: str, regions: str = "us",
                       markets: str = "h2h", odds_format: str = "american") -> Dict:
        """Get odds for specific event"""
        cache_key = f"event_odds_theodds_{event_id}"
        if self._is_cached(cache_key):
            return self._get_cache(cache_key)
        
        params = {
            "regions": regions,
            "markets": markets,
            "oddsFormat": odds_format
        }
        
        data = self._make_request(f"sports/{sport}/events/{event_id}/odds", params)
        self._set_cache(cache_key, data)
        return data
    
    def parse_odds_to_canonical(self, odds_response: List[Dict]) -> List[OddsData]:
        """Parse The Odds API response to canonical OddsData format"""
        canonical = []
        timestamp = datetime.now().isoformat()
        
        for event in odds_response:
            event_id = event.get('id')
            sport = event.get('sport_key')
            home_team = event.get('home_team')
            away_team = event.get('away_team')
            commence_time = event.get('commence_time')
            
            # Process bookmakers
            for bookmaker in event.get('bookmakers', []):
                book_name = bookmaker.get('key')
                
                for market in bookmaker.get('markets', []):
                    market_type = market.get('key')  # h2h, spreads, totals
                    
                    for outcome in market.get('outcomes', []):
                        name = outcome.get('name')
                        price = outcome.get('price')
                        point = outcome.get('point')  # For spreads/totals
                        
                        # Convert decimal to american if needed
                        if isinstance(price, float) and price < 10:
                            odds_american = self.decimal_to_american(price)
                            odds_decimal = price
                        else:
                            odds_american = int(price) if price else 0
                            odds_decimal = self.american_to_decimal(odds_american)
                        
                        # Build outcome string
                        outcome_str = name
                        if point is not None:
                            outcome_str = f"{name} {point}"
                        
                        implied_prob = self.american_to_probability(odds_american)
                        
                        canonical.append(OddsData(
                            book=book_name,
                            market_type=market_type,
                            outcome=outcome_str,
                            odds_american=odds_american,
                            odds_decimal=odds_decimal,
                            implied_probability=implied_prob,
                            timestamp=timestamp,
                            source_api='theoddsapi'
                        ))
        
        return canonical
    
    @staticmethod
    def decimal_to_american(decimal_odds: float) -> int:
        """Convert decimal odds to american"""
        if decimal_odds >= 2.0:
            return int((decimal_odds - 1) * 100)
        else:
            return int(-100 / (decimal_odds - 1))
    
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
    
    def get_usage_stats(self) -> Dict:
        """Get current API usage stats"""
        return {
            'requests_remaining': self.requests_remaining,
            'requests_used': self.requests_used,
            'requests_total': 500  # Free tier limit
        }
    
    # Cache methods
    def _is_cached(self, key: str) -> bool:
        if key not in self._cache:
            return False
        cached_time, data = self._cache[key]
        if time.time() - cached_time > self._cache_ttl:
            del self._cache[key]
            return False
        return True
    
    def _get_cache(self, key: str):
        return self._cache[key][1]
    
    def _set_cache(self, key: str, data):
        self._cache[key] = (time.time(), data)
    
    def clear_cache(self):
        self._cache.clear()


class UnifiedSportsbookClient:
    """
    Unified client with automatic failover between RapidAPI and The Odds API
    """
    
    def __init__(self):
        self.rapidapi = None
        self.theodds = None
        self.primary = 'rapidapi'
        
        # Initialize RapidAPI if key available
        rapidapi_key = os.getenv('RAPIDAPI_KEY')
        if rapidapi_key:
            try:
                from sportsbook_client import SportsbookAPIClient
                self.rapidapi = SportsbookAPIClient(rapidapi_key)
                print("✅ RapidAPI Sportsbook client initialized")
            except Exception as e:
                print(f"⚠️  Failed to initialize RapidAPI: {e}")
        
        # Initialize The Odds API if key available
        theodds_key = os.getenv('THE_ODDS_API_KEY')
        if theodds_key:
            try:
                self.theodds = TheOddsAPIClient(theodds_key)
                print("✅ The Odds API client initialized")
            except Exception as e:
                print(f"⚠️  Failed to initialize The Odds API: {e}")
        
        if not self.rapidapi and not self.theodds:
            raise ValueError("No sportsbook API keys configured")
    
    def get_sports(self) -> List[Dict]:
        """Get sports with failover"""
        try:
            if self.primary == 'rapidapi' and self.rapidapi:
                return self.rapidapi.get_sports()
            elif self.theodds:
                return self.theodds.get_sports()
        except Exception as e:
            print(f"⚠️  Primary API failed: {e}, trying backup...")
            self._switch_primary()
            return self.get_sports()
    
    def get_odds(self, sport: str, **kwargs) -> List[OddsData]:
        """Get odds with failover"""
        try:
            if self.primary == 'rapidapi' and self.rapidapi:
                # RapidAPI uses different params
                from sportsbook_client import SportsbookAPIClient
                if 'league' in kwargs:
                    games = self.rapidapi.get_games(kwargs['league'])
                    # Get odds for each game (this is inefficient, use caching)
                    all_odds = []
                    for game in games[:5]:  # Limit to 5 games
                        try:
                            odds = self.rapidapi.get_odds(game['id'])
                            all_odds.extend(self.rapidapi.parse_odds_to_canonical(odds))
                        except:
                            continue
                    return all_odds
            elif self.theodds:
                odds = self.theodds.get_odds(sport, **kwargs)
                return self.theodds.parse_odds_to_canonical(odds)
        except Exception as e:
            print(f"⚠️  Primary API failed: {e}, trying backup...")
            self._switch_primary()
            return self.get_odds(sport, **kwargs)
    
    def _switch_primary(self):
        """Switch primary API"""
        if self.primary == 'rapidapi' and self.theodds:
            self.primary = 'theodds'
            print("🔄 Switched to The Odds API as primary")
        elif self.primary == 'theodds' and self.rapidapi:
            self.primary = 'rapidapi'
            print("🔄 Switched to RapidAPI as primary")
    
    def get_usage_stats(self) -> Dict:
        """Get usage stats from both APIs"""
        stats = {}
        if self.theodds:
            stats['theodds'] = self.theodds.get_usage_stats()
        if self.rapidapi:
            stats['rapidapi'] = {'note': 'Usage tracking not available'}
        return stats


# ============ CLI INTERFACE ============

if __name__ == "__main__":
    import sys
    
    try:
        client = UnifiedSportsbookClient()
    except ValueError as e:
        print(f"❌ {e}")
        sys.exit(1)
    
    command = sys.argv[1] if len(sys.argv) > 1 else "help"
    
    if command == "sports":
        sports = client.get_sports()
        print(json.dumps(sports, indent=2))
    
    elif command == "odds":
        if len(sys.argv) < 3:
            print("Usage: python unified_odds_client.py odds <sport_key>")
            print("Example: python unified_odds_client.py odds basketball_nba")
            sys.exit(1)
        
        sport = sys.argv[2]
        odds = client.get_odds(sport, regions="us", markets="h2h")
        print(f"Found {len(odds)} odds entries")
        for o in odds[:10]:
            print(f"{o.book:15} | {o.market_type:10} | {o.outcome:25} | {o.odds_american:+4d} | {o.implied_probability:.2%} | {o.source_api}")
    
    elif command == "usage":
        stats = client.get_usage_stats()
        print(json.dumps(stats, indent=2))
    
    else:
        print("""
Unified Sportsbook API Client

Usage:
    python unified_odds_client.py <command> [args]

Commands:
    sports              List available sports
    odds <sport_key>    Get odds for a sport
    usage               Show API usage stats

Environment Variables:
    RAPIDAPI_KEY        RapidAPI key (primary)
    THE_ODDS_API_KEY    The Odds API key (backup)

Examples:
    python unified_odds_client.py sports
    python unified_odds_client.py odds basketball_nba
    python unified_odds_client.py odds americanfootball_nfl
        """)
