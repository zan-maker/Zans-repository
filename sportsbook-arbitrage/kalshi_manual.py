"""
Kalshi Manual Input Mode
For when API auth isn't available - manually input Kalshi prices
"""
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class KalshiMarket:
    """Represents a Kalshi market"""
    ticker: str
    title: str
    yes_price: float  # $0.01 to $0.99
    no_price: float
    volume: int
    league: str
    home_team: str
    away_team: str
    event_date: str

class KalshiManualInput:
    """
    Manual Kalshi market input for testing
    
    When Kalshi API requires auth, use this to manually input
    market prices from the Kalshi website/app for comparison.
    """
    
    def __init__(self):
        self.markets: List[KalshiMarket] = []
    
    def add_market(
        self,
        ticker: str,
        yes_price: float,
        no_price: float,
        volume: int = 10000,
        title: str = "",
        league: str = "NBA",
        home_team: str = "",
        away_team: str = "",
        event_date: str = ""
    ) -> KalshiMarket:
        """Add a manually input market"""
        market = KalshiMarket(
            ticker=ticker,
            title=title or ticker,
            yes_price=yes_price,
            no_price=no_price,
            volume=volume,
            league=league,
            home_team=home_team,
            away_team=away_team,
            event_date=event_date
        )
        self.markets.append(market)
        return market
    
    def get_markets(self, league: str = None) -> List[KalshiMarket]:
        """Get all markets, optionally filtered by league"""
        if league:
            return [m for m in self.markets if m.league.upper() == league.upper()]
        return self.markets
    
    def to_dict(self, market: KalshiMarket) -> Dict:
        """Convert to dict format compatible with arbitrage scanner"""
        return {
            "ticker": market.ticker,
            "title": market.title,
            "yes_ask": int(market.yes_price * 100),
            "yes_bid": int(market.yes_price * 100) - 1,
            "no_ask": int(market.no_price * 100),
            "no_bid": int(market.no_price * 100) - 1,
            "volume": market.volume
        }
    
    def load_sample_nba_markets(self):
        """Load sample NBA markets for testing"""
        self.markets = []
        
        # Sample markets matching the live odds above
        # Yes price = Home team win probability
        samples = [
            {
                "ticker": "NBA-2026-02-20-WAS-vs-IND",
                "title": "Will Washington Wizards beat Indiana Pacers?",
                "yes_price": 0.39,  # Wizards implied 39%
                "no_price": 0.62,   # Pacers implied 62%
                "home_team": "Washington Wizards",
                "away_team": "Indiana Pacers",
                "volume": 25000
            },
            {
                "ticker": "NBA-2026-02-20-PHI-vs-ATL",
                "title": "Will Philadelphia 76ers beat Atlanta Hawks?",
                "yes_price": 0.63,  # 76ers implied 63%
                "no_price": 0.38,   # Hawks implied 38%
                "home_team": "Philadelphia 76ers",
                "away_team": "Atlanta Hawks",
                "volume": 32000
            },
            {
                "ticker": "NBA-2026-02-20-CLE-vs-BKN",
                "title": "Will Cleveland Cavaliers beat Brooklyn Nets?",
                "yes_price": 0.85,  # Cavs implied 85%
                "no_price": 0.16,   # Nets implied 16%
                "home_team": "Cleveland Cavaliers",
                "away_team": "Brooklyn Nets",
                "volume": 18000
            }
        ]
        
        for s in samples:
            self.add_market(**s)
        
        return self.markets
    
    def print_markets(self):
        """Display all markets"""
        print("KALSHI MARKETS (Manual Input)")
        print("=" * 70)
        print(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        print()
        
        for m in self.markets:
            print(f"{m.ticker}")
            print(f"  {m.title}")
            print(f"  Yes (Home): ${m.yes_price:.2f} ({m.yes_price*100:.0f}%)")
            print(f"  No (Away):  ${m.no_price:.2f} ({m.no_price*100:.0f}%)")
            print(f"  Volume: {m.volume:,}")
            print()


if __name__ == "__main__":
    kalshi = KalshiManualInput()
    kalshi.load_sample_nba_markets()
    kalshi.print_markets()
    
    print("\nTo use in arbitrage scanner:")
    print("  markets = kalshi.get_markets()")
    print("  kalshi_dicts = [kalshi.to_dict(m) for m in markets]")
