#!/usr/bin/env python3
"""
Step 10: Portfolio Selection
Apply portfolio constraints and select final 5 trades.
Output in clean table format.
"""

import json
from datetime import datetime

# Portfolio parameters
NAV = 100000  # $100K portfolio
MAX_LOSS_PER_TRADE = 500  # $500 max loss
MAX_TRADES_PER_SECTOR = 2
TARGET_DELTA_RANGE = [-0.30, 0.30]
TARGET_VEGA_LIMIT = -0.05

def load_macro_context():
    """Load current macro indicators for thesis generation."""
    return {
        'vix': 15.5,
        'fed_meeting_soon': False,
        'cpi_soon': False
    }

def generate_thesis(trade, macro):
    """Generate concise thesis (max 30 words)."""
    symbol = trade['symbol']
    strategy = trade['strategy']
    iv = trade.get('iv', 30)
    pop = trade.get('pop', 65)
    
    # Base thesis on strategy type
    if strategy == 'Bull Put':
        base = f"Strong fundamentals, IV {iv:.0f}% supports put selling, {pop:.0f}% win rate."
    else:
        base = f"Technical resistance, IV {iv:.0f}% elevated, {pop:.0f}% win rate."
    
    # Add risk warning if applicable
    if trade.get('heat', 1) > 5:
        base += f" Watch for volatility."
    
    # Ensure under 30 words
    words = base.split()
    if len(words) > 30:
        base = ' '.join(words[:30])
    
    return base

def select_portfolio(trades):
    """Apply portfolio constraints and select 5 trades."""
    
    # Hard filters
    filtered = []
    for t in trades:
        # Max loss filter
        max_loss_dollars = t['max_loss'] * 100  # Per contract
        if max_loss_dollars > MAX_LOSS_PER_TRADE:
            continue
        
        # PoP filter (top option must be >= 65%)
        if t['pop'] < 65:
            continue
        
        # Credit ratio filter
        if (t['credit'] / t['max_loss']) < 0.33:
            continue
        
        filtered.append(t)
    
    print(f"After hard filters: {len(filtered)} trades")
    
    # Sort by composite score
    filtered.sort(key=lambda x: x.get('score', 0), reverse=True)
    
    # Apply portfolio constraints
    selected = []
    sector_counts = {}
    total_delta = 0
    total_vega = 0
    
    for trade in filtered:
        sector = trade.get('sector', 'Unknown')
        
        # Sector constraint
        if sector_counts.get(sector, 0) >= MAX_TRADES_PER_SECTOR:
            continue
        
        # Delta constraint (simplified - would calculate full position delta)
        trade_delta = trade.get('short_delta', 0) * 0.20  # Assume 20% position
        new_delta = total_delta + trade_delta
        if new_delta < TARGET_DELTA_RANGE[0] or new_delta > TARGET_DELTA_RANGE[1]:
            continue
        
        # Vega constraint
        trade_vega = trade.get('vega', 0) * 0.20
        new_vega = total_vega + trade_vega
        if new_vega < TARGET_VEGA_LIMIT:
            continue
        
        # Accept trade
        selected.append(trade)
        sector_counts[sector] = sector_counts.get(sector, 0) + 1
        total_delta = new_delta
        total_vega = new_vega
        
        if len(selected) >= 5:
            break
    
    return selected

def output_table(trades):
    """Output clean table format."""
    macro = load_macro_context()
    
    print("\n" + "="*80)
    print("OPTIONS RECOMMENDATIONS")
    print("="*80)
    print()
    
    # Header
    print(f"{'Ticker':<8} {'Strategy':<12} {'Legs':<25} {'Thesis':<35} {'POP':<6}")
    print("-" * 80)
    
    for trade in trades:
        symbol = trade['symbol']
        strategy = trade['strategy']
        legs = trade['legs']
        thesis = generate_thesis(trade, macro)
        pop = f"{trade['pop']:.0f}%"
        
        # Ensure thesis fits in 35 chars for display
        if len(thesis) > 35:
            thesis = thesis[:32] + "..."
        
        print(f"{symbol:<8} {strategy:<12} {legs:<25} {thesis:<35} {pop:<6}")
    
    print()
    print("="*80)
    
    # Detailed breakdown
    print("\nDETAILED TRADE CARDS:")
    print("-" * 80)
    
    for i, trade in enumerate(trades, 1):
        print(f"\n{i}. {trade['symbol']} - {trade['strategy']}")
        print(f"   Legs: {trade['legs']}")
        print(f"   Credit: ${trade['credit']:.2f} | Max Loss: ${trade['max_loss']:.2f}")
        print(f"   ROI: {trade['roi']:.1f}% | PoP: {trade['pop']:.1f}%")
        print(f"   Short Delta: {trade['short_delta']:.3f} | Theta: ${trade['theta']:.3f}")
        print(f"   IV: {trade['iv']:.1f}% | Days to Exp: {trade['days_to_exp']}")
        print(f"   Thesis: {generate_thesis(trade, macro)}")
        
        # Risk warnings
        warnings = []
        if trade.get('heat', 1) > 5:
            warnings.append("High event risk")
        if trade.get('earnings_date'):
            warnings.append(f"Earnings: {trade['earnings_date']}")
        
        if warnings:
            print(f"   ⚠️  WARNINGS: {', '.join(warnings)}")

def output_csv(trades):
    """Output CSV format for automation."""
    print("\nCSV OUTPUT:")
    print("ticker,strategy,legs,credit,max_loss,roi,pop,short_strike,long_strike")
    
    for trade in trades:
        print(f"{trade['symbol']},{trade['strategy']},\"{trade['legs']}\","
              f"{trade['credit']},{trade['max_loss']},{trade['roi']},{trade['pop']},"
              f"{trade['short_strike']},{trade['long_strike']}")

def main():
    print("="*60)
    print("STEP 10: PORTFOLIO SELECTION")
    print("="*60)
    
    # Load filtered spreads
    try:
        with open('filtered_spreads.json', 'r') as f:
            trades = json.load(f)
    except:
        print("Error: filtered_spreads.json not found. Run 02_news_filter.py first.")
        return
    
    print(f"Loaded {len(trades)} filtered trades")
    print(f"\nApplying portfolio constraints:")
    print(f"  - Max $500 loss per trade")
    print(f"  - Min 65% PoP")
    print(f"  - Max 2 per sector")
    print(f"  - Delta range: {TARGET_DELTA_RANGE}")
    print(f"  - Vega limit: {TARGET_VEGA_LIMIT}")
    
    selected = select_portfolio(trades)
    
    print(f"\nSelected {len(selected)} trades")
    
    if len(selected) < 5:
        print("\n" + "!"*60)
        print("Fewer than 5 trades meet criteria, do not execute.")
        print("!"*60)
        
        # Still output what we have
        if selected:
            output_table(selected)
    else:
        output_table(selected)
        output_csv(selected)
        
        # Save final trades
        with open('final_trades.json', 'w') as f:
            json.dump(selected, f, indent=2)
        print("\nSaved to final_trades.json")

if __name__ == '__main__':
    main()
