"""
Sportsbook Odds Fetcher - The Odds API (Direct)
Uses urllib (built-in) instead of requests
"""
import urllib.request
import urllib.error
import json
from datetime import datetime
from typing import Dict, List, Optional

# Configuration - Direct API Access
API_KEY = "a2584115f9fd3d4520f34449495a9d4f"
BASE_URL = "https://api.the-odds-api.com/v4"

class OddsAPIClient:
    """Client for The Odds API (Direct)"""
    
    def __init__(self, api_key: str = API_KEY):
        self.api_key = api_key
    
    def _make_request(self, url: str, params: Dict = None) -> Dict:
        """Make HTTP request with error handling"""
        # Add API key to params
        if params is None:
            params = {}
        params["apiKey"] = self.api_key
        
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        full_url = f"{url}?{query_string}"
        
        req = urllib.request.Request(full_url)
        
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                return json.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            raise Exception(f"HTTP Error {e.code}: {error_body}")
        except Exception as e:
            raise Exception(f"Request failed: {e}")
    
    def get_sports(self) -> List[Dict]:
        """Get list of available sports"""
        url = f"{BASE_URL}/sports/"
        return self._make_request(url)
    
    def get_odds(
        self, 
        sport: str = "upcoming",
        regions: str = "us",
        markets: str = "h2h",
        odds_format: str = "decimal",
        date_format: str = "iso"
    ) -> List[Dict]:
        """
        Get odds for a sport
        
        Args:
            sport: Sport key (e.g., 'basketball_nba', 'americanfootball_nfl') 
                   or 'upcoming' for all upcoming events
            regions: 'us', 'uk', 'eu', 'au' or comma-separated combo
            markets: 'h2h' (moneyline), 'spreads', 'totals', 'outrights'
            odds_format: 'decimal' or 'american'
            date_format: 'iso' or 'unix'
        """
        url = f"{BASE_URL}/sports/{sport}/odds"
        params = {
            "regions": regions,
            "markets": markets,
            "oddsFormat": odds_format,
            "dateFormat": date_format
        }
        
        return self._make_request(url, params)
    
    def get_event_odds(
        self,
        sport: str,
        event_id: str,
        regions: str = "us",
        markets: str = "h2h",
        odds_format: str = "decimal"
    ) -> Dict:
        """Get odds for a specific event"""
        url = f"{BASE_URL}/sports/{sport}/events/{event_id}/odds"
        params = {
            "regions": regions,
            "markets": markets,
            "oddsFormat": odds_format
        }
        
        return self._make_request(url, params)
    
    def get_scores(self, sport: str = "upcoming", days_from: int = 1) -> List[Dict]:
        """Get scores (and odds) for events"""
        url = f"{BASE_URL}/sports/{sport}/scores"
        params = {"daysFrom": days_from}
        
        return self._make_request(url, params)


class OddsNormalizer:
    """Normalize odds from different bookmakers"""
    
    @staticmethod
    def decimal_to_implied_prob(decimal_odds: float) -> float:
        """Convert decimal odds to implied probability"""
        return 1 / decimal_odds
    
    @staticmethod
    def american_to_decimal(american_odds: int) -> float:
        """Convert American odds to decimal"""
        if american_odds > 0:
            return (american_odds / 100) + 1
        else:
            return (100 / abs(american_odds)) + 1
    
    @staticmethod
    def remove_vig(prob1: float, prob2: float) -> tuple:
        """Remove vigorish to get true implied probability"""
        total_prob = prob1 + prob2
        return (prob1 / total_prob, prob2 / total_prob)
    
    def extract_best_odds(self, event: Dict, market: str = "h2h") -> Dict:
        """
        Extract best available odds from all bookmakers for an event
        
        Returns:
            Dict with best odds for each outcome and bookmaker info
        """
        outcomes = {}
        
        for bookmaker in event.get("bookmakers", []):
            for market_data in bookmaker.get("markets", []):
                if market_data.get("key") != market:
                    continue
                
                for outcome in market_data.get("outcomes", []):
                    name = outcome["name"]
                    price = outcome["price"]
                    
                    if name not in outcomes or price > outcomes[name]["price"]:
                        outcomes[name] = {
                            "price": price,
                            "bookmaker": bookmaker["title"],
                            "implied_prob": self.decimal_to_implied_prob(price)
                        }
        
        return outcomes


if __name__ == "__main__":
    # Test the client
    client = OddsAPIClient()
    normalizer = OddsNormalizer()
    
    print("Testing The Odds API connection...")
    print("=" * 50)
    
    # Get available sports
    try:
        sports = client.get_sports()
        print(f"✓ Connected! Available sports: {len(sports)}")
        
        # Show active sports
        active_sports = [s for s in sports if s.get("active")]
        print(f"\nActive sports ({len(active_sports)}):")
        for sport in active_sports[:10]:  # Show first 10
            print(f"  - {sport['key']}: {sport['title']}")
        
        # Get upcoming odds (limited to save API calls)
        print("\n" + "=" * 50)
        print("Fetching upcoming NBA odds...")
        
        try:
            odds = client.get_odds(
                sport="basketball_nba",
                regions="us",
                markets="h2h"
            )
            print(f"✓ Retrieved {len(odds)} upcoming NBA games")
            
            # Show first game details
            if odds:
                game = odds[0]
                print(f"\nExample game: {game['home_team']} vs {game['away_team']}")
                print(f"Commences: {game['commence_time']}")
                
                best_odds = normalizer.extract_best_odds(game)
                print(f"\nBest odds (moneyline):")
                for team, data in best_odds.items():
                    print(f"  {team}: {data['price']} ({data['bookmaker']}) - Implied: {data['implied_prob']:.2%}")
                
        except Exception as e:
            print(f"✗ Error fetching odds: {e}")
            
    except Exception as e:
        print(f"✗ Connection failed: {e}")
