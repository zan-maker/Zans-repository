#!/usr/bin/env python3
"""
Steps 1-7: Build Credit Spreads
Generate bull put and bear call spreads with full Greeks and PoP calculations.
"""

import os
import json
import requests
import numpy as np
from datetime import datetime, timedelta
from scipy.stats import norm

# API Configuration
ALPACA_KEY = os.getenv('ALPACA_API_KEY', 'PKNDK5P66FCRH5P5ILPTVCYE7D')
ALPACA_SECRET = os.getenv('ALPACA_API_SECRET', 'z1fwAHFV9H8NY26XrZ2sSSxJggc8BwqiU2gPxVsy49V')
FINNHUB_KEY = os.getenv('FINNHUB_API_KEY', 'd6bq93hr01qp4li0f2h0d6bq93hr01qp4li0f2hg')

ALPACA_BASE = 'https://paper-api.alpaca.markets/v2'
FINNHUB_BASE = 'https://finnhub.io/api/v1'

def alpaca_headers():
    return {
        'APCA-API-KEY-ID': ALPACA_KEY,
        'APCA-API-SECRET-KEY': ALPACA_SECRET
    }

def get_stock_price(symbol):
    """Get current stock price."""
    url = f'{FINNHUB_BASE}/quote?symbol={symbol}&token={FINNHUB_KEY}'
    try:
        r = requests.get(url, timeout=5)
        return r.json().get('c')
    except:
        return None

def get_options_chain(symbol):
    """Get full options chain with Greeks."""
    url = f'{ALPACA_BASE}/options/contracts'
    params = {
        'underlying_symbol': symbol,
        'status': 'active',
        'expiration_date_gte': (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d'),
        'expiration_date_lte': (datetime.now() + timedelta(days=45)).strftime('%Y-%m-%d'),
        'limit': 200
    }
    
    try:
        r = requests.get(url, headers=alpaca_headers(), params=params, timeout=15)
        contracts = r.json().get('option_contracts', [])
        
        # Fetch Greeks and quotes for each contract
        enriched = []
        for contract in contracts:
            symbol_opt = contract['symbol']
            
            # Get snapshot with Greeks
            snap_url = f'{ALPACA_BASE}/options/snapshots/{symbol_opt}'
            try:
                snap_r = requests.get(snap_url, headers=alpaca_headers(), timeout=5)
                snap = snap_r.json()
            except:
                snap = {}
            
            # Get latest quote
            quote_url = f'{ALPACA_BASE}/options/quotes/latest'
            try:
                quote_r = requests.get(quote_url, headers=alpaca_headers(), 
                                      params={'symbol': symbol_opt}, timeout=5)
                quote = quote_r.json().get('quote', {})
            except:
                quote = {}
            
            mid = (quote.get('bid_price', 0) + quote.get('ask_price', 0)) / 2
            spread_pct = (quote.get('ask_price', 0) - quote.get('bid_price', 0)) / max(mid, 0.01)
            
            # Skip illiquid options
            if mid < 0.30 or spread_pct > 0.10:
                continue
            
            enriched.append({
                'symbol': symbol_opt,
                'strike': float(contract['strike_price']),
                'expiration': contract['expiration_date'],
                'type': contract['type'],
                'bid': quote.get('bid_price', 0),
                'ask': quote.get('ask_price', 0),
                'mid': mid,
                'iv': snap.get('implied_volatility', 0.30),
                'delta': snap.get('greeks', {}).get('delta', 0),
                'gamma': snap.get('greeks', {}).get('gamma', 0),
                'theta': snap.get('greeks', {}).get('theta', 0),
                'vega': snap.get('greeks', {}).get('vega', 0),
                'volume': snap.get('volume', 0),
                'open_interest': snap.get('open_interest', 0)
            })
        
        return enriched
    except Exception as e:
        print(f"Error fetching options for {symbol}: {e}")
        return []

def calculate_pop(stock_price, strike, days_to_exp, iv, risk_free_rate=0.045, option_type='put'):
    """Calculate Probability of Profit using Black-Scholes."""
    T = days_to_exp / 365.0
    sigma = iv
    
    if sigma <= 0 or T <= 0:
        return 0.5
    
    d1 = (np.log(stock_price / strike) + (risk_free_rate + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type == 'put':
        # For short put: PoP = Probability stock stays above strike
        return 1 - norm.cdf(-d2)
    else:
        # For short call: PoP = Probability stock stays below strike
        return 1 - norm.cdf(d2)

def build_bull_put_spreads(calls, puts, stock_price, symbol):
    """Build bull put spreads (bullish strategy)."""
    spreads = []
    
    # Filter OTM puts (strike < stock price)
    otm_puts = [p for p in puts if p['strike'] < stock_price * 0.95]
    otm_puts.sort(key=lambda x: x['strike'], reverse=True)
    
    for i, short_put in enumerate(otm_puts):
        # Target 15-35 delta for short leg
        if abs(short_put['delta']) < 0.15 or abs(short_put['delta']) > 0.35:
            continue
        
        # Find long put $5-10 below short
        long_puts = [p for p in puts if p['strike'] < short_put['strike'] - 2]
        if not long_puts:
            continue
        
        long_put = max(long_puts, key=lambda x: x['strike'])
        
        # Calculate spread metrics
        credit = short_put['mid'] - long_put['mid']
        width = short_put['strike'] - long_put['strike']
        max_loss = width - credit
        
        if max_loss <= 0 or credit <= 0:
            continue
        
        roi = (credit / max_loss) * 100
        
        # Skip if ROI outside 5-50%
        if roi < 5 or roi > 50:
            continue
        
        # Calculate PoP
        days_to_exp = 30  # Approximate
        pop = calculate_pop(stock_price, short_put['strike'], days_to_exp, 
                           short_put['iv'], option_type='put')
        
        # Skip if PoP < 60%
        if pop < 0.60:
            continue
        
        # Skip if max loss > $500
        if max_loss * 100 > 500:  # Per contract
            continue
        
        spreads.append({
            'symbol': symbol,
            'strategy': 'Bull Put',
            'legs': f"Sell ${short_put['strike']:.0f}P / Buy ${long_put['strike']:.0f}P",
            'short_strike': short_put['strike'],
            'long_strike': long_put['strike'],
            'credit': round(credit, 2),
            'max_loss': round(max_loss, 2),
            'roi': round(roi, 1),
            'pop': round(pop * 100, 1),
            'short_delta': round(short_put['delta'], 3),
            'theta': round(short_put['theta'], 3),
            'iv': round(short_put['iv'] * 100, 1),
            'days_to_exp': days_to_exp,
            'score': (roi * pop * 100) / 100  # (ROI * PoP) / 100
        })
    
    return spreads

def build_bear_call_spreads(calls, puts, stock_price, symbol):
    """Build bear call spreads (bearish strategy)."""
    spreads = []
    
    # Filter OTM calls (strike > stock price)
    otm_calls = [c for c in calls if c['strike'] > stock_price * 1.05]
    otm_calls.sort(key=lambda x: x['strike'])
    
    for i, short_call in enumerate(otm_calls):
        # Target 15-35 delta for short leg
        if abs(short_call['delta']) < 0.15 or abs(short_call['delta']) > 0.35:
            continue
        
        # Find long call $5-10 above short
        long_calls = [c for c in calls if c['strike'] > short_call['strike'] + 2]
        if not long_calls:
            continue
        
        long_call = min(long_calls, key=lambda x: x['strike'])
        
        # Calculate spread metrics
        credit = short_call['mid'] - long_call['mid']
        width = long_call['strike'] - short_call['strike']
        max_loss = width - credit
        
        if max_loss <= 0 or credit <= 0:
            continue
        
        roi = (credit / max_loss) * 100
        
        # Skip if ROI outside 5-50%
        if roi < 5 or roi > 50:
            continue
        
        # Calculate PoP
        days_to_exp = 30  # Approximate
        pop = calculate_pop(stock_price, short_call['strike'], days_to_exp,
                           short_call['iv'], option_type='call')
        
        # Skip if PoP < 60%
        if pop < 0.60:
            continue
        
        # Skip if max loss > $500
        if max_loss * 100 > 500:
            continue
        
        spreads.append({
            'symbol': symbol,
            'strategy': 'Bear Call',
            'legs': f"Sell ${short_call['strike']:.0f}C / Buy ${long_call['strike']:.0f}C",
            'short_strike': short_call['strike'],
            'long_strike': long_call['strike'],
            'credit': round(credit, 2),
            'max_loss': round(max_loss, 2),
            'roi': round(roi, 1),
            'pop': round(pop * 100, 1),
            'short_delta': round(short_call['delta'], 3),
            'theta': round(short_call['theta'], 3),
            'iv': round(short_call['iv'] * 100, 1),
            'days_to_exp': days_to_exp,
            'score': (roi * pop * 100) / 100
        })
    
    return spreads

def get_sector(symbol):
    """Get GICS sector for symbol."""
    url = f'{FINNHUB_BASE}/stock/profile2?symbol={symbol}&token={FINNHUB_KEY}'
    try:
        r = requests.get(url, timeout=5)
        return r.json().get('finnhubIndustry', 'Unknown')
    except:
        return 'Unknown'

def analyze_symbol(symbol_data):
    """Build spreads for a single symbol."""
    symbol = symbol_data['symbol']
    print(f"Building spreads for {symbol}...")
    
    stock_price = get_stock_price(symbol)
    if not stock_price:
        return []
    
    chain = get_options_chain(symbol)
    if len(chain) < 10:
        return []
    
    calls = [c for c in chain if c['type'] == 'call']
    puts = [c for c in chain if c['type'] == 'put']
    
    if len(calls) < 5 or len(puts) < 5:
        return []
    
    bull_puts = build_bull_put_spreads(calls, puts, stock_price, symbol)
    bear_calls = build_bear_call_spreads(calls, puts, stock_price, symbol)
    
    all_spreads = bull_puts + bear_calls
    
    # Add sector tag
    sector = get_sector(symbol)
    for s in all_spreads:
        s['sector'] = sector
        s['stock_price'] = stock_price
    
    # Return top 3 by score
    all_spreads.sort(key=lambda x: x['score'], reverse=True)
    return all_spreads[:3]

def main():
    print("="*60)
    print("STEPS 1-7: BUILD CREDIT SPREADS")
    print("="*60)
    
    # Load universe
    try:
        with open('universe.json', 'r') as f:
            universe = json.load(f)
    except:
        print("Error: universe.json not found. Run 00_build_universe.py first.")
        return
    
    print(f"Loaded {len(universe)} stocks from universe")
    
    all_spreads = []
    
    for stock_data in universe:
        spreads = analyze_symbol(stock_data)
        all_spreads.extend(spreads)
        print(f"  {stock_data['symbol']}: {len(spreads)} spreads")
    
    # Rank all spreads
    all_spreads.sort(key=lambda x: x['score'], reverse=True)
    
    # Take top 9 with sector diversification
    selected = []
    sector_counts = {}
    
    for spread in all_spreads:
        sector = spread.get('sector', 'Unknown')
        if sector_counts.get(sector, 0) < 2:  # Max 2 per sector
            selected.append(spread)
            sector_counts[sector] = sector_counts.get(sector, 0) + 1
        
        if len(selected) >= 9:
            break
    
    print(f"\nSelected top {len(selected)} diversified spreads:")
    for s in selected[:5]:
        print(f"  {s['symbol']:5} {s['strategy']:10} | "
              f"ROI: {s['roi']:5.1f}% | PoP: {s['pop']:5.1f}% | "
              f"Credit: ${s['credit']:.2f}")
    
    # Save for news filter step
    with open('spreads.json', 'w') as f:
        json.dump(selected, f, indent=2)
    
    print(f"\nSaved to spreads.json")

if __name__ == '__main__':
    main()
