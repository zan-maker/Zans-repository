#!/usr/bin/env python3
"""
Steps 8-9: News Filter
Use GPT to analyze headlines for each trade and flag risk events.
Output: TRADE, WAIT, or SKIP for each candidate.
"""

import os
import json
import requests
from datetime import datetime, timedelta

FINNHUB_KEY = os.getenv('FINNHUB_API_KEY', 'd6bq93hr01qp4li0f2h0d6bq93hr01qp4li0f2hg')
FINNHUB_BASE = 'https://finnhub.io/api/v1'

def get_recent_news(symbol, days=3):
    """Get recent news headlines for a symbol."""
    end = datetime.now()
    start = end - timedelta(days=days)
    
    url = f'{FINNHUB_BASE}/company-news'
    params = {
        'symbol': symbol,
        'from': start.strftime('%Y-%m-%d'),
        'to': end.strftime('%Y-%m-%d'),
        'token': FINNHUB_KEY
    }
    
    try:
        r = requests.get(url, params=params, timeout=10)
        news = r.json()
        # Return top 3 headlines with summaries
        return [
            {
                'headline': n.get('headline', ''),
                'summary': n.get('summary', '')[:200],
                'source': n.get('source', ''),
                'datetime': datetime.fromtimestamp(n.get('datetime', 0)).strftime('%Y-%m-%d')
            }
            for n in news[:3]
        ]
    except Exception as e:
        return []

def get_earnings_date(symbol):
    """Get next earnings date."""
    url = f'{FINNHUB_BASE}/calendar/earnings?symbol={symbol}&token={FINNHUB_KEY}'
    try:
        r = requests.get(url, timeout=5)
        data = r.json()
        if data and 'earningsCalendar' in data:
            earnings = data['earningsCalendar']
            if earnings:
                return earnings[0].get('date')
    except:
        pass
    return None

def analyze_news_gpt(symbol, strategy, news_items, earnings_date):
    """
    Simulate GPT analysis of news.
    In production, this would call an LLM API.
    """
    headlines_text = "\n".join([f"- {n['headline']}" for n in news_items])
    
    # Risk keywords to check
    risk_keywords = {
        'earnings': ['earnings', 'quarterly', 'revenue', 'profit', 'eps'],
        'fda': ['fda', 'approval', 'clinical trial', 'drug'],
        'merger': ['merger', 'acquisition', 'buyout', 'takeover'],
        'lawsuit': ['lawsuit', 'sec investigation', 'settlement'],
        'bankruptcy': ['bankruptcy', 'restructuring', 'debt default'],
        'layoffs': ['layoffs', 'job cuts', 'restructuring'],
        'guidance': ['guidance', 'outlook', 'forecast']
    }
    
    # Check for risk events
    risk_score = 0
    detected_risks = []
    
    all_text = " ".join([n['headline'] + " " + n['summary'] for n in news_items]).lower()
    
    for risk_type, keywords in risk_keywords.items():
        if any(kw in all_text for kw in keywords):
            if risk_type in ['earnings', 'fda', 'merger', 'bankruptcy']:
                risk_score += 3
                detected_risks.append(risk_type)
            else:
                risk_score += 1
                detected_risks.append(risk_type)
    
    # Check earnings proximity
    if earnings_date:
        try:
            earn_date = datetime.strptime(earnings_date, '%Y-%m-%d')
            days_to_earn = (earn_date - datetime.now()).days
            if 0 <= days_to_earn <= 7:
                risk_score += 3
                detected_risks.append(f'earnings_in_{days_to_earn}d')
        except:
            pass
    
    # Determine action
    if risk_score >= 5:
        action = 'SKIP'
        heat = min(10, risk_score)
    elif risk_score >= 2:
        action = 'WAIT'
        heat = risk_score
    else:
        action = 'TRADE'
        heat = max(1, risk_score)
    
    # Generate thesis
    if detected_risks:
        thesis = f"Risk events detected: {', '.join(detected_risks[:2])}."
    else:
        thesis = "No significant risk events in recent news."
    
    return {
        'action': action,
        'heat': heat,
        'thesis': thesis,
        'headlines': [n['headline'] for n in news_items],
        'earnings_date': earnings_date,
        'detected_risks': detected_risks
    }

def main():
    print("="*60)
    print("STEPS 8-9: NEWS FILTER")
    print("="*60)
    
    # Load spreads
    try:
        with open('spreads.json', 'r') as f:
            spreads = json.load(f)
    except:
        print("Error: spreads.json not found. Run 01_build_spreads.py first.")
        return
    
    print(f"Analyzing {len(spreads)} candidates...")
    
    analyzed = []
    
    for spread in spreads:
        symbol = spread['symbol']
        strategy = spread['strategy']
        
        print(f"\n{symbol} - {strategy}")
        
        # Get data
        news = get_recent_news(symbol)
        earnings = get_earnings_date(symbol)
        
        # Analyze
        result = analyze_news_gpt(symbol, strategy, news, earnings)
        
        print(f"  Action: {result['action']} | Heat: {result['heat']}/10")
        if result['headlines']:
            print(f"  Headlines:")
            for h in result['headlines'][:2]:
                print(f"    - {h[:70]}...")
        
        # Merge with spread data
        spread.update(result)
        analyzed.append(spread)
    
    # Filter out SKIP trades
    tradeable = [s for s in analyzed if s['action'] != 'SKIP']
    skipped = [s for s in analyzed if s['action'] == 'SKIP']
    
    print(f"\n{'='*60}")
    print(f"RESULTS:")
    print(f"  Total analyzed: {len(analyzed)}")
    print(f"  SKIP: {len(skipped)}")
    print(f"  WAIT: {len([s for s in analyzed if s['action'] == 'WAIT'])}")
    print(f"  TRADE: {len(tradeable)}")
    
    # Save for portfolio selection
    with open('filtered_spreads.json', 'w') as f:
        json.dump(tradeable, f, indent=2)
    
    print(f"\nSaved {len(tradeable)} tradeable spreads to filtered_spreads.json")

if __name__ == '__main__':
    main()
