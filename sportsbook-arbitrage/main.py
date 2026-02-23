"""
Sportsbook-Kalshi Arbitrage Bot
Main orchestrator that coordinates data fetching and mispricing detection
"""
import json
import sys
from datetime import datetime
from typing import List, Dict, Optional

# Import our modules
from odds_fetcher import OddsAPIClient, OddsNormalizer
from kalshi_connector import KalshiClient
from arbitrage_scanner import ArbitrageScanner, MispricingOpportunity

class ArbitrageBot:
    """
    Main bot that orchestrates the arbitrage detection system
    
    Workflow:
    1. Fetch sportsbook odds from RapidAPI
    2. Fetch Kalshi market prices
    3. Match events between sources
    4. Detect mispricings
    5. Generate alerts/reports
    """
    
    def __init__(
        self,
        rapidapi_key: str,
        kalshi_email: str = None,
        kalshi_password: str = None,
        threshold_pct: float = 3.0,
        min_confidence: float = 0.5
    ):
        self.odds_client = OddsAPIClient(rapidapi_key)
        self.kalshi_client = KalshiClient(kalshi_email, kalshi_password)
        self.normalizer = OddsNormalizer()
        self.scanner = ArbitrageScanner(threshold_pct, min_confidence)
        
        self.sportsbook_data: List[Dict] = []
        self.kalshi_data: List[Dict] = []
        self.opportunities: List[MispricingOpportunity] = []
        
        self.run_log: List[Dict] = []
    
    def fetch_sportsbook_odds(
        self,
        sport: str = "upcoming",
        regions: str = "us",
        markets: str = "h2h"
    ) -> List[Dict]:
        """Fetch odds from sportsbooks via RapidAPI"""
        print(f"📊 Fetching sportsbook odds: {sport}...")
        
        try:
            odds = self.odds_client.get_odds(
                sport=sport,
                regions=regions,
                markets=markets
            )
            self.sportsbook_data = odds
            print(f"✓ Retrieved {len(odds)} events from sportsbooks")
            return odds
        except Exception as e:
            print(f"✗ Failed to fetch odds: {e}")
            return []
    
    def fetch_kalshi_markets(self, league: str = None) -> List[Dict]:
        """Fetch markets from Kalshi"""
        print(f"📈 Fetching Kalshi markets...")
        
        try:
            markets = self.kalshi_client.get_sports_markets(league=league)
            self.kalshi_data = markets
            print(f"✓ Retrieved {len(markets)} markets from Kalshi")
            return markets
        except Exception as e:
            print(f"✗ Failed to fetch Kalshi markets: {e}")
            return []
    
    def scan_for_opportunities(self) -> List[MispricingOpportunity]:
        """Run the arbitrage scanner"""
        print("🔍 Scanning for mispricings...")
        
        if not self.sportsbook_data:
            print("⚠ No sportsbook data available. Run fetch_sportsbook_odds() first.")
            return []
        
        if not self.kalshi_data:
            print("⚠ No Kalshi data available. Run fetch_kalshi_markets() first.")
            return []
        
        opportunities = self.scanner.scan_batch(
            self.sportsbook_data,
            self.kalshi_data
        )
        
        self.opportunities = opportunities
        
        # Log this run
        self.run_log.append({
            "timestamp": datetime.now().isoformat(),
            "sportsbook_events": len(self.sportsbook_data),
            "kalshi_markets": len(self.kalshi_data),
            "opportunities_found": len(opportunities)
        })
        
        print(f"✓ Found {len(opportunities)} mispricing opportunities")
        return opportunities
    
    def generate_report(self, save_to_file: bool = False) -> str:
        """Generate a full report"""
        report = []
        report.append("=" * 80)
        report.append("SPORTSBOOK-KALSHI ARBITRAGE REPORT")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        report.append("=" * 80)
        report.append("")
        
        # Summary stats
        report.append("📊 SUMMARY")
        report.append("-" * 40)
        report.append(f"Sportsbook events analyzed: {len(self.sportsbook_data)}")
        report.append(f"Kalshi markets analyzed: {len(self.kalshi_data)}")
        report.append(f"Opportunities detected: {len(self.opportunities)}")
        report.append("")
        
        # Opportunities
        if self.opportunities:
            report.append(self.scanner.generate_report())
        else:
            report.append("No mispricing opportunities detected above threshold.")
            report.append("")
            report.append("Possible reasons:")
            report.append("- Markets are efficiently priced")
            report.append("- Low liquidity on Kalshi")
            report.append("- Threshold set too high")
        
        report_text = "\n".join(report)
        
        if save_to_file:
            filename = f"reports/arbitrage_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w') as f:
                f.write(report_text)
            print(f"💾 Report saved to {filename}")
        
        return report_text
    
    def run_full_scan(
        self,
        sport: str = "upcoming",
        league: str = None,
        save_report: bool = False
    ) -> List[MispricingOpportunity]:
        """
        Run a complete scan cycle
        
        Args:
            sport: Sport to scan (e.g., 'basketball_nba')
            league: League filter for Kalshi (e.g., 'NBA')
            save_report: Whether to save report to file
        
        Returns:
            List of detected opportunities
        """
        print("=" * 80)
        print("🚀 STARTING FULL ARBITRAGE SCAN")
        print("=" * 80)
        print("")
        
        # Step 1: Fetch sportsbook odds
        self.fetch_sportsbook_odds(sport=sport)
        print("")
        
        # Step 2: Fetch Kalshi markets
        self.fetch_kalshi_markets(league=league)
        print("")
        
        # Step 3: Scan for opportunities
        opportunities = self.scan_for_opportunities()
        print("")
        
        # Step 4: Generate report
        print(self.generate_report(save_to_file=save_report))
        
        return opportunities
    
    def get_run_history(self) -> List[Dict]:
        """Get history of all scan runs"""
        return self.run_log
    
    def export_opportunities_json(self, filepath: str = None):
        """Export opportunities to JSON"""
        if not filepath:
            filepath = f"data/opportunities_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        self.scanner.export_json(filepath)


def demo():
    """Demo with mock data"""
    print("ARBITRAGE BOT DEMO (with mock data)")
    print("=" * 80)
    print()
    
    # Create bot
    bot = ArbitrageBot(
        rapidapi_key="demo_key",
        threshold_pct=2.0
    )
    
    # Mock sportsbook data
    bot.sportsbook_data = [
        {
            "id": "evt-001",
            "sport_key": "basketball_nba",
            "home_team": "Los Angeles Lakers",
            "away_team": "Golden State Warriors",
            "bookmakers": [
                {
                    "title": "DraftKings",
                    "markets": [{
                        "key": "h2h",
                        "outcomes": [
                            {"name": "Los Angeles Lakers", "price": 1.80},
                            {"name": "Golden State Warriors", "price": 2.05}
                        ]
                    }]
                }
            ]
        },
        {
            "id": "evt-002",
            "sport_key": "basketball_nba",
            "home_team": "Boston Celtics",
            "away_team": "Miami Heat",
            "bookmakers": [
                {
                    "title": "FanDuel",
                    "markets": [{
                        "key": "h2h",
                        "outcomes": [
                            {"name": "Boston Celtics", "price": 1.35},
                            {"name": "Miami Heat", "price": 3.20}
                        ]
                    }]
                }
            ]
        }
    ]
    
    # Mock Kalshi data
    bot.kalshi_data = [
        {
            "ticker": "NBA-2025-02-17-LAL-vs-GSW",
            "title": "LAL beats GSW?",
            "yes_ask": 52,
            "yes_bid": 51,
            "no_ask": 49,
            "no_bid": 48,
            "volume": 25000
        },
        {
            "ticker": "NBA-2025-02-17-BOS-vs-MIA",
            "title": "BOS beats MIA?",
            "yes_ask": 70,
            "yes_bid": 69,
            "no_ask": 32,
            "no_bid": 31,
            "volume": 18000
        }
    ]
    
    # Run scan
    print(f"Loaded {len(bot.sportsbook_data)} sportsbook events")
    print(f"Loaded {len(bot.kalshi_data)} Kalshi markets")
    print()
    
    opportunities = bot.scan_for_opportunities()
    print()
    print(bot.generate_report())


if __name__ == "__main__":
    # Check for command line args
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo()
    else:
        print("SPORTSBOOK-KALSHI ARBITRAGE BOT")
        print("=" * 80)
        print()
        print("Usage:")
        print("  python3 main.py demo          # Run with mock data")
        print()
        print("To run live:")
        print("  1. Ensure RapidAPI key is subscribed to The Odds API")
        print("  2. from main import ArbitrageBot")
        print("  3. bot = ArbitrageBot(RAPIDAPI_KEY)")
        print("  4. bot.run_full_scan()")
        print()
        print("Running demo mode...")
        print()
        demo()
