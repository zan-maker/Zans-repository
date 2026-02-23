"""
Arbitrage Scanner - Sportsbook vs Kalshi Mispricing Detection

This module compares sportsbook odds with Kalshi prediction market prices
to identify potential mispricing opportunities.
"""
import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

@dataclass
class MispricingOpportunity:
    """Represents a detected mispricing opportunity"""
    event_id: str
    event_name: str
    sport: str
    
    # Sportsbook data
    sportsbook_name: str
    sportsbook_odds: float
    sportsbook_implied_prob: float
    
    # Kalshi data
    kalshi_ticker: str
    kalshi_price: float
    kalshi_implied_prob: float
    
    # Analysis
    mispricing_pct: float  # Absolute difference
    edge_direction: str    # "sportsbook_favorite" or "kalshi_favorite"
    confidence: float      # 0-1 based on liquidity/volume
    
    # Metadata
    timestamp: str
    notes: str = ""
    
    def to_dict(self) -> Dict:
        return {
            "event_id": self.event_id,
            "event_name": self.event_name,
            "sport": self.sport,
            "sportsbook": {
                "name": self.sportsbook_name,
                "odds": self.sportsbook_odds,
                "implied_probability": round(self.sportsbook_implied_prob * 100, 2)
            },
            "kalshi": {
                "ticker": self.kalshi_ticker,
                "price": self.kalshi_price,
                "implied_probability": round(self.kalshi_implied_prob * 100, 2)
            },
            "mispricing": {
                "percentage": round(self.mispricing_pct * 100, 2),
                "edge_direction": self.edge_direction,
                "potential_profit": self._calculate_potential_profit()
            },
            "confidence": round(self.confidence, 2),
            "timestamp": self.timestamp,
            "notes": self.notes
        }
    
    def _calculate_potential_profit(self) -> float:
        """Calculate potential profit if edge is real"""
        # Simplified calculation
        if self.edge_direction == "sportsbook_favorite":
            # Sportsbook thinks higher probability than Kalshi
            # Opportunity: bet on Kalshi side (lower price)
            return (1 / self.kalshi_price - 1) * 100
        else:
            # Kalshi thinks higher probability than sportsbook
            # Opportunity: bet at sportsbook (higher odds)
            return (self.sportsbook_odds - 1) * 100


class ArbitrageScanner:
    """
    Scans for mispricing opportunities between sportsbooks and Kalshi
    """
    
    def __init__(self, threshold_pct: float = 3.0, min_confidence: float = 0.5):
        """
        Initialize scanner
        
        Args:
            threshold_pct: Minimum mispricing % to flag (default 3%)
            min_confidence: Minimum confidence level (0-1)
        """
        self.threshold = threshold_pct / 100  # Convert to decimal
        self.min_confidence = min_confidence
        self.opportunities: List[MispricingOpportunity] = []
    
    def calculate_implied_probability(self, decimal_odds: float) -> float:
        """Convert decimal odds to implied probability"""
        return 1.0 / decimal_odds
    
    def remove_vig(self, prob1: float, prob2: float) -> Tuple[float, float]:
        """Remove vigorish to get true probabilities"""
        total = prob1 + prob2
        return (prob1 / total, prob2 / total)
    
    def compare_event(
        self,
        event_id: str,
        event_name: str,
        sport: str,
        team_name: str,
        sportsbook_odds: float,
        sportsbook_name: str,
        kalshi_price: float,
        kalshi_ticker: str,
        kalshi_volume: int = 0,
        notes: str = ""
    ) -> Optional[MispricingOpportunity]:
        """
        Compare a single event between sportsbook and Kalshi
        
        Returns:
            MispricingOpportunity if threshold met, None otherwise
        """
        # Convert to implied probabilities
        book_prob = self.calculate_implied_probability(sportsbook_odds)
        kalshi_prob = kalshi_price  # Kalshi price is already implied probability
        
        # Calculate mispricing
        mispricing = abs(book_prob - kalshi_prob)
        
        # Determine edge direction
        if book_prob > kalshi_prob:
            edge = "sportsbook_favorite"
        else:
            edge = "kalshi_favorite"
        
        # Calculate confidence based on volume
        # Higher volume = higher confidence
        confidence = min(kalshi_volume / 10000, 1.0) if kalshi_volume > 0 else 0.5
        
        # Check thresholds
        if mispricing < self.threshold or confidence < self.min_confidence:
            return None
        
        opportunity = MispricingOpportunity(
            event_id=event_id,
            event_name=event_name,
            sport=sport,
            sportsbook_name=sportsbook_name,
            sportsbook_odds=sportsbook_odds,
            sportsbook_implied_prob=book_prob,
            kalshi_ticker=kalshi_ticker,
            kalshi_price=kalshi_price,
            kalshi_implied_prob=kalshi_prob,
            mispricing_pct=mispricing,
            edge_direction=edge,
            confidence=confidence,
            timestamp=datetime.now().isoformat(),
            notes=notes
        )
        
        return opportunity
    
    def scan_batch(
        self,
        events: List[Dict],
        kalshi_markets: List[Dict]
    ) -> List[MispricingOpportunity]:
        """
        Scan a batch of events against Kalshi markets
        
        Args:
            events: List of sportsbook events with odds
            kalshi_markets: List of Kalshi markets
        
        Returns:
            List of detected opportunities
        """
        opportunities = []
        
        # Create lookup for Kalshi markets
        kalshi_lookup = {}
        for market in kalshi_markets:
            ticker = market.get("ticker", "").lower()
            kalshi_lookup[ticker] = market
        
        # Compare each event
        for event in events:
            event_id = event.get("id", "")
            home_team = event.get("home_team", "")
            away_team = event.get("away_team", "")
            sport = event.get("sport_key", "")
            
            # Try to find matching Kalshi market
            # This requires fuzzy matching on team names
            match_key = self._generate_match_key(home_team, away_team, sport)
            
            if match_key in kalshi_lookup:
                kalshi_market = kalshi_lookup[match_key]
                
                # Get best odds from bookmakers
                best_odds = self._extract_best_odds(event)
                
                for team, odds_data in best_odds.items():
                    kalshi_price = self._get_kalshi_price_for_team(kalshi_market, team)
                    
                    if kalshi_price:
                        opp = self.compare_event(
                            event_id=event_id,
                            event_name=f"{home_team} vs {away_team}",
                            sport=sport,
                            team_name=team,
                            sportsbook_odds=odds_data["odds"],
                            sportsbook_name=odds_data["bookmaker"],
                            kalshi_price=kalshi_price,
                            kalshi_ticker=kalshi_market.get("ticker"),
                            kalshi_volume=kalshi_market.get("volume", 0)
                        )
                        
                        if opp:
                            opportunities.append(opp)
        
        self.opportunities = opportunities
        return opportunities
    
    def _generate_match_key(self, home: str, away: str, sport: str) -> str:
        """Generate a matching key for event lookup"""
        # Simplified - in production would need fuzzy matching
        home_clean = home.lower().replace(" ", "")
        away_clean = away.lower().replace(" ", "")
        return f"{sport.lower()}_{home_clean}_{away_clean}"
    
    def _extract_best_odds(self, event: Dict) -> Dict[str, Dict]:
        """Extract best odds for each team from event data"""
        best = {}
        
        for bookmaker in event.get("bookmakers", []):
            for market in bookmaker.get("markets", []):
                if market.get("key") != "h2h":
                    continue
                
                for outcome in market.get("outcomes", []):
                    team = outcome["name"]
                    odds = outcome["price"]
                    
                    if team not in best or odds > best[team]["odds"]:
                        best[team] = {
                            "odds": odds,
                            "bookmaker": bookmaker["title"]
                        }
        
        return best
    
    def _get_kalshi_price_for_team(self, market: Dict, team: str) -> Optional[float]:
        """Get Kalshi price for a specific team"""
        # Kalshi "Yes" is typically home team win
        # This needs better logic based on market structure
        title = market.get("title", "").lower()
        if team.lower() in title:
            yes_price = market.get("yes_ask", 0)
            return yes_price / 100 if yes_price else None
        return None
    
    def generate_report(self) -> str:
        """Generate human-readable report of opportunities"""
        if not self.opportunities:
            return "No mispricing opportunities detected."
        
        lines = [
            "=" * 70,
            "ARBITRAGE SCANNER REPORT",
            f"Generated: {datetime.now().isoformat()}",
            f"Threshold: {self.threshold * 100}% | Min Confidence: {self.min_confidence}",
            "=" * 70,
            ""
        ]
        
        # Sort by mispricing magnitude
        sorted_opps = sorted(
            self.opportunities,
            key=lambda x: x.mispricing_pct,
            reverse=True
        )
        
        for i, opp in enumerate(sorted_opps, 1):
            lines.append(f"OPPORTUNITY #{i}")
            lines.append("-" * 50)
            lines.append(f"Event: {opp.event_name}")
            lines.append(f"Sport: {opp.sport}")
            lines.append(f"")
            lines.append(f"Sportsbook ({opp.sportsbook_name}):")
            lines.append(f"  Odds: {opp.sportsbook_odds}")
            lines.append(f"  Implied Prob: {opp.sportsbook_implied_prob * 100:.2f}%")
            lines.append(f"")
            lines.append(f"Kalshi ({opp.kalshi_ticker}):")
            lines.append(f"  Price: ${opp.kalshi_price:.2f}")
            lines.append(f"  Implied Prob: {opp.kalshi_implied_prob * 100:.2f}%")
            lines.append(f"")
            lines.append(f"MISPRICING: {opp.mispricing_pct * 100:.2f}%")
            lines.append(f"Edge Direction: {opp.edge_direction}")
            lines.append(f"Confidence: {opp.confidence * 100:.1f}%")
            lines.append(f"Potential Profit: {opp._calculate_potential_profit():.2f}%")
            lines.append("")
        
        lines.append("=" * 70)
        lines.append(f"Total opportunities: {len(self.opportunities)}")
        lines.append("=" * 70)
        
        return "\n".join(lines)
    
    def export_json(self, filepath: str):
        """Export opportunities to JSON file"""
        data = [opp.to_dict() for opp in self.opportunities]
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Exported {len(data)} opportunities to {filepath}")


if __name__ == "__main__":
    # Demo with mock data
    print("Testing Arbitrage Scanner...")
    print("=" * 60)
    
    scanner = ArbitrageScanner(threshold_pct=2.0)
    
    # Mock comparison
    opp = scanner.compare_event(
        event_id="test-001",
        event_name="Lakers vs Warriors",
        sport="NBA",
        team_name="Lakers",
        sportsbook_odds=1.80,  # -125 American
        sportsbook_name="DraftKings",
        kalshi_price=0.52,  # $0.52 = 52% implied
        kalshi_ticker="NBA-2025-02-17-LAL-vs-GSW",
        kalshi_volume=25000,
        notes="Test data"
    )
    
    if opp:
        scanner.opportunities = [opp]
        print("✓ Opportunity detected!")
        print(f"\n{scanner.generate_report()}")
    else:
        print("No opportunity (below threshold)")
    
    # Show calculation
    print("\n" + "=" * 60)
    print("CALCULATION EXAMPLE:")
    print("=" * 60)
    print("Sportsbook odds: 1.80 (decimal)")
    print("Implied probability: 1/1.80 = 55.56%")
    print("")
    print("Kalshi price: $0.52")
    print("Implied probability: 52%")
    print("")
    print("Mispricing: |55.56% - 52%| = 3.56%")
    print("Edge: Sportsbook prices Lakers higher probability than Kalshi")
    print("→ Opportunity: Buy Lakers on Kalshi at $0.52")
