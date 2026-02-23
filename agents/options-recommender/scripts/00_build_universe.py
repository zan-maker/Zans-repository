#!/usr/bin/env python3
"""
Step 0: Build Universe
Screen S&P 500 stocks and score using 4-category convergence model.
Outputs top 22 stocks for options analysis.
"""

import os
import json
import requests
import numpy as np
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed

# API Configuration
ALPACA_KEY = os.getenv('ALPACA_API_KEY', 'PKNDK5P66FCRH5P5ILPTVCYE7D')
ALPACA_SECRET = os.getenv('ALPACA_API_SECRET', 'z1fwAHFV9H8NY26XrZ2sSSxJggc8BwqiU2gPxVsy49V')
FINNHUB_KEY = os.getenv('FINNHUB_API_KEY', 'd6bq93hr01qp4li0f2h0d6bq93hr01qp4li0f2hg')
FRED_KEY = os.getenv('FRED_API_KEY', 'c00b92a9c6a70cb70efc3201cfb9bb5f')

ALPACA_BASE = 'https://paper-api.alpaca.markets/v2'
FINNHUB_BASE = 'https://finnhub.io/api/v1'
FRED_BASE = 'https://api.stlouisfed.org/fred'

def alpaca_headers():
    return {
        'APCA-API-KEY-ID': ALPACA_KEY,
        'APCA-API-SECRET-KEY': ALPACA_SECRET
    }

def get_sp500_symbols():
    """Fetch S&P 500 symbols from Wikipedia or cache."""
    try:
        import pandas as pd
        url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        tables = pd.read_html(url)
        symbols = tables[0]['Symbol'].tolist()
        return [s.replace('.', '-') for s in symbols]  # BRK.B -> BRK-B
    except:
        # Fallback to common symbols
        return ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'META', 'TSLA', 'NVDA', 'JPM', 
                'V', 'UNH', 'JNJ', 'WMT', 'PG', 'HD', 'MA', 'BAC', 'ABBV', 'PFE',
                'KO', 'PEP', 'COST', 'TMO', 'AVGO', 'DIS', 'ADBE', 'CRM', 'ACN',
                'VZ', 'DHR', 'ABT', 'CMCSA', 'NKE', 'TXN', 'NEE', 'PM', 'RTX']

def get_stock_quote(symbol):
    """Get current stock price from Finnhub."""
    url = f'{FINNHUB_BASE}/quote?symbol={symbol}&token={FINNHUB_KEY}'
    try:
        r = requests.get(url, timeout=5)
        data = r.json()
        return {
            'price': data.get('c'),
            'change': data.get('d'),
            'change_pct': data.get('dp'),
            'high': data.get('h'),
            'low': data.get('l'),
            'volume': data.get('v')
        }
    except Exception as e:
        return None

def get_fundamentals(symbol):
    """Get fundamental metrics from Finnhub."""
    url = f'{FINNHUB_BASE}/stock/metric?symbol={symbol}&metric=all&token={FINNHUB_KEY}'
    try:
        r = requests.get(url, timeout=5)
        data = r.json()
        m = data.get('metric', {})
        return {
            'pe': m.get('peBasicExclExtraTTM'),
            'ps': m.get('psTTM'),
            'pb': m.get('pbAnnual'),
            'roe': m.get('roeTTM'),
            'debt_equity': m.get('totalDebt/totalEquityAnnual'),
            'current_ratio': m.get('currentRatioAnnual'),
            'gross_margin': m.get('grossMarginAnnual'),
            'operating_margin': m.get('operatingMarginAnnual'),
            'profit_margin': m.get('netProfitMarginAnnual'),
            'revenue_growth': m.get('revenueGrowthTTM'),
            'eps_growth': m.get('epsGrowthTTM')
        }
    except:
        return {}

def get_financials(symbol):
    """Get financial statements for F-Score and Z-Score."""
    url = f'{FINNHUB_BASE}/stock/financials-reported?symbol={symbol}&token={FINNHUB_KEY}'
    try:
        r = requests.get(url, timeout=5)
        data = r.json()
        # Process financials for Piotroski F-Score
        return data.get('data', [])
    except:
        return []

def get_options_chain(symbol):
    """Get available options contracts from Alpaca."""
    url = f'{ALPACA_BASE}/options/contracts'
    params = {
        'underlying_symbol': symbol,
        'status': 'active',
        'expiration_date_gte': (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d'),
        'expiration_date_lte': (datetime.now() + timedelta(days=45)).strftime('%Y-%m-%d'),
        'limit': 100
    }
    try:
        r = requests.get(url, headers=alpaca_headers(), params=params, timeout=10)
        data = r.json()
        contracts = data.get('option_contracts', [])
        
        # Count strikes and get IV data
        strikes = set(c['strike_price'] for c in contracts)
        
        return {
            'count': len(contracts),
            'strikes': len(strikes),
            'has_options': len(contracts) >= 20
        }
    except Exception as e:
        return {'count': 0, 'strikes': 0, 'has_options': False}

def calculate_piortroski_fscore(financials):
    """Calculate 9-point Piotroski F-Score."""
    if not financials or len(financials) < 2:
        return 5  # Neutral if no data
    
    score = 0
    try:
        curr = financials[0]
        prev = financials[1]
        
        # Profitability (4 points)
        if curr.get('netIncome', 0) > 0: score += 1
        if curr.get('operatingCashFlow', 0) > 0: score += 1
        
        curr_roa = curr.get('netIncome', 0) / max(curr.get('assets', 1), 1)
        prev_roa = prev.get('netIncome', 0) / max(prev.get('assets', 1), 1)
        if curr_roa > prev_roa: score += 1
        
        if curr.get('operatingCashFlow', 0) > curr.get('netIncome', 0): score += 1
        
        # Leverage/Liquidity (3 points)
        curr_lev = curr.get('longTermDebt', 0) / max(curr.get('assets', 1), 1)
        prev_lev = prev.get('longTermDebt', 0) / max(prev.get('assets', 1), 1)
        if curr_lev < prev_lev: score += 1
        
        curr_cr = curr.get('currentAssets', 0) / max(curr.get('currentLiabilities', 1), 1)
        prev_cr = prev.get('currentAssets', 0) / max(prev.get('currentLiabilities', 1), 1)
        if curr_cr > prev_cr: score += 1
        
        if curr.get('commonStock', 0) <= prev.get('commonStock', 0): score += 1
        
        # Efficiency (2 points)
        if curr.get('grossMargin', 0) > prev.get('grossMargin', 0): score += 1
        
        curr_at = curr.get('revenue', 0) / max(curr.get('assets', 1), 1)
        prev_at = prev.get('revenue', 0) / max(prev.get('assets', 1), 1)
        if curr_at > prev_at: score += 1
        
    except:
        pass
    
    return score

def calculate_altman_zscore(financials, market_cap):
    """Calculate Altman Z-Score for bankruptcy prediction."""
    if not financials:
        return 3.0  # Assume safe if no data
    
    try:
        f = financials[0]
        assets = f.get('assets', 0)
        if assets == 0:
            return 3.0
        
        working_capital = f.get('currentAssets', 0) - f.get('currentLiabilities', 0)
        retained_earnings = f.get('retainedEarnings', 0)
        ebit = f.get('ebit', 0)
        total_liabilities = f.get('totalLiabilities', 0)
        revenue = f.get('revenue', 0)
        
        A = working_capital / assets
        B = retained_earnings / assets
        C = ebit / assets
        D = market_cap / max(total_liabilities, 1)
        E = revenue / assets
        
        Z = 1.2*A + 1.4*B + 3.3*C + 0.6*D + 1.0*E
        return Z
    except:
        return 3.0

def score_quality(fundamentals, financials, market_cap):
    """Calculate Quality score (0-100)."""
    f_score = calculate_piortroski_fscore(financials)
    z_score = calculate_altman_zscore(financials, market_cap)
    
    # F-Score component (0-50 points)
    f_component = (f_score / 9) * 50
    
    # Z-Score component (0-50 points)
    if z_score > 3: z_component = 50
    elif z_score > 1.8: z_component = 25 + (z_score - 1.8) / 1.2 * 25
    else: z_component = max(0, z_score / 1.8 * 25)
    
    return f_component + z_component

def score_vol_edge(symbol):
    """Calculate Vol-Edge score (0-100) based on IV vs HV."""
    # Get historical volatility from Alpaca
    end = datetime.now()
    start = end - timedelta(days=252)  # 1 year
    
    url = f'{ALPACA_BASE}/stocks/{symbol}/bars'
    params = {
        'timeframe': '1Day',
        'start': start.strftime('%Y-%m-%d'),
        'end': end.strftime('%Y-%m-%d'),
        'limit': 300
    }
    
    try:
        r = requests.get(url, headers=alpaca_headers(), params=params, timeout=10)
        bars = r.json().get('bars', [])
        
        if len(bars) < 20:
            return 50  # Neutral
        
        closes = [b['c'] for b in bars]
        log_returns = np.diff(np.log(closes))
        hv = np.std(log_returns) * np.sqrt(252) * 100  # Annualized HV
        
        # Get current IV from options snapshot (simplified)
        # In practice, fetch from Alpaca options endpoint
        iv = hv * 1.3  # Placeholder - would fetch actual IV
        
        ratio = iv / max(hv, 1)
        
        # Score based on IV/HV ratio
        if ratio > 2.0: return 90 + min((ratio - 2.0) * 10, 10)
        elif ratio > 1.5: return 70 + (ratio - 1.5) * 40
        elif ratio > 1.0: return 40 + (ratio - 1.0) * 60
        else: return max(0, ratio * 40)
        
    except:
        return 50

def get_macro_regime():
    """Get current macro regime classification from FRED."""
    series = ['VIXCLS', 'DGS10', 'UNRATE', 'CPIAUCSL', 'GDP', 'UMCSENT']
    data = {}
    
    for s in series:
        url = f'{FRED_BASE}/series/observations'
        params = {
            'series_id': s,
            'api_key': FRED_KEY,
            'sort_order': 'desc',
            'limit': 1,
            'file_type': 'json'
        }
        try:
            r = requests.get(url, params=params, timeout=5)
            obs = r.json().get('observations', [])
            if obs:
                data[s] = float(obs[0]['value'])
        except:
            data[s] = None
    
    # Simple regime classification
    vix = data.get('VIXCLS', 20)
    unrate = data.get('UNRATE', 4)
    
    if vix < 20 and unrate < 5:
        return 'Goldilocks'
    elif vix > 25:
        return 'Contraction'
    else:
        return 'Recovery'

def score_regime(symbol, sector):
    """Calculate Regime score (0-100) based on macro fit."""
    regime = get_macro_regime()
    
    # Sector preferences by regime
    regime_scores = {
        'Goldilocks': {
            'Technology': 90, 'Consumer Cyclical': 85, 'Communication': 80,
            'Financial': 75, 'Industrials': 75, 'Healthcare': 70,
            'Consumer Defensive': 60, 'Utilities': 50, 'Energy': 60
        },
        'Contraction': {
            'Utilities': 90, 'Consumer Defensive': 85, 'Healthcare': 80,
            'Technology': 50, 'Financial': 40, 'Consumer Cyclical': 40,
            'Communication': 50, 'Industrials': 45, 'Energy': 55
        },
        'Recovery': {
            'Financial': 90, 'Consumer Cyclical': 85, 'Industrials': 80,
            'Technology': 75, 'Energy': 70, 'Materials': 75,
            'Communication': 70, 'Healthcare': 65, 'Utilities': 50
        }
    }
    
    return regime_scores.get(regime, {}).get(sector, 60)

def score_info_edge(symbol):
    """Calculate Info-Edge score (0-100) from analyst, insider, news signals."""
    score = 50  # Neutral base
    
    # Analyst recommendations
    url = f'{FINNHUB_BASE}/stock/recommendation?symbol={symbol}&token={FINNHUB_KEY}'
    try:
        r = requests.get(url, timeout=5)
        recs = r.json()
        if recs:
            latest = recs[0]
            total = latest.get('buy', 0) + latest.get('hold', 0) + latest.get('sell', 0)
            if total > 0:
                buy_ratio = latest.get('buy', 0) / total
                if buy_ratio > 0.7: score += 10
                elif buy_ratio < 0.3: score -= 10
    except:
        pass
    
    # Insider transactions (last 3 months)
    url = f'{FINNHUB_BASE}/stock/insider-transactions?symbol={symbol}&token={FINNHUB_KEY}'
    try:
        r = requests.get(url, timeout=5)
        txs = r.json().get('data', [])
        buys = sum(1 for t in txs if t.get('transactionType') == 'P')
        sells = sum(1 for t in txs if t.get('transactionType') == 'S')
        if buys > sells * 2: score += 15
        elif sells > buys * 2: score -= 15
    except:
        pass
    
    return min(100, max(0, score))

def analyze_stock(symbol):
    """Full analysis pipeline for a single stock."""
    print(f"Analyzing {symbol}...")
    
    # Get base data
    quote = get_stock_quote(symbol)
    if not quote or not quote['price']:
        return None
    
    price = quote['price']
    
    # Price filter ($30-$400)
    if price < 30 or price > 400:
        return None
    
    # Check options availability
    options = get_options_chain(symbol)
    if not options['has_options']:
        return None
    
    # Get fundamental data
    fundamentals = get_fundamentals(symbol)
    financials = get_financials(symbol)
    
    # Calculate market cap for Z-Score
    # Would get actual shares outstanding from profile
    market_cap = price * 1e9  # Placeholder
    
    # Score all 4 categories
    vol_score = score_vol_edge(symbol)
    quality_score = score_quality(fundamentals, financials, market_cap)
    
    # Get sector for regime scoring
    sector = 'Technology'  # Would fetch from profile
    regime_score = score_regime(symbol, sector)
    
    info_score = score_info_edge(symbol)
    
    # Check convergence gate (at least 3 of 4 > 50)
    scores = [vol_score, quality_score, regime_score, info_score]
    above_50 = sum(1 for s in scores if s > 50)
    
    if above_50 < 3:
        return None
    
    # Calculate weighted composite
    composite = (vol_score * 0.25 + quality_score * 0.25 + 
                 regime_score * 0.25 + info_score * 0.25)
    
    return {
        'symbol': symbol,
        'price': price,
        'volume': quote.get('volume'),
        'options_count': options['count'],
        'vol_score': vol_score,
        'quality_score': quality_score,
        'regime_score': regime_score,
        'info_score': info_score,
        'composite': composite,
        'above_50_count': above_50,
        'fundamentals': fundamentals
    }

def main():
    print("="*60)
    print("STEP 0: BUILD UNIVERSE")
    print("="*60)
    
    symbols = get_sp500_symbols()
    print(f"Loaded {len(symbols)} S&P 500 symbols")
    
    results = []
    
    # Analyze in parallel (rate limited)
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(analyze_stock, s): s for s in symbols[:100]}  # Limit for testing
        for future in as_completed(futures):
            result = future.result()
            if result:
                results.append(result)
    
    # Sort by composite score
    results.sort(key=lambda x: x['composite'], reverse=True)
    
    # Take top 22
    top_22 = results[:22]
    
    print(f"\nSelected top {len(top_22)} stocks:")
    for r in top_22[:10]:
        print(f"  {r['symbol']:5} | Composite: {r['composite']:.1f} | "
              f"Vol: {r['vol_score']:.0f} | Q: {r['quality_score']:.0f} | "
              f"R: {r['regime_score']:.0f} | I: {r['info_score']:.0f}")
    
    # Save to file for next step
    with open('universe.json', 'w') as f:
        json.dump(top_22, f, indent=2)
    
    print(f"\nSaved to universe.json")
    return top_22

if __name__ == '__main__':
    main()
