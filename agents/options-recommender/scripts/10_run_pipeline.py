#!/usr/bin/env python3
"""
10_run_pipeline.py - End-to-end Options Recommender Pipeline

Runs the complete workflow:
  Step 0: Build Universe (S&P 500 screening)
  Steps 1-7: Build Credit Spreads
  Steps 8-9: News Filter (GPT risk analysis)
  Step 10: Portfolio Selection

Expected runtime: ~1000 seconds
"""

import os
import sys
import time
import json
from datetime import datetime

# Ensure scripts directory is in path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

def run_step(step_name, module_name):
    """Run a pipeline step and report timing."""
    print("\n" + "="*70)
    print(f"RUNNING: {step_name}")
    print("="*70)
    
    start = time.time()
    
    try:
        # Import and run module
        module = __import__(module_name)
        if hasattr(module, 'main'):
            module.main()
        
        elapsed = time.time() - start
        print(f"\n✓ {step_name} completed in {elapsed:.1f}s")
        return True, elapsed
        
    except Exception as e:
        elapsed = time.time() - start
        print(f"\n✗ {step_name} failed after {elapsed:.1f}s: {e}")
        return False, elapsed

def main():
    print("="*70)
    print("OPTIONS RECOMMENDER - FULL PIPELINE")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    # Check API keys
    required_env = {
        'ALPACA_API_KEY': os.getenv('ALPACA_API_KEY', 'PKNDK5P66FCRH5P5ILPTVCYE7D'),
        'ALPACA_API_SECRET': os.getenv('ALPACA_API_SECRET', 'z1fwAHFV9H8NY26XrZ2sSSxJggc8BwqiU2gPxVsy49V'),
        'FINNHUB_API_KEY': os.getenv('FINNHUB_API_KEY', 'd6bq93hr01qp4li0f2h0d6bq93hr01qp4li0f2hg'),
        'FRED_API_KEY': os.getenv('FRED_API_KEY', 'c00b92a9c6a70cb70efc3201cfb9bb5f')
    }
    
    print("\nAPI Configuration:")
    for key, value in required_env.items():
        masked = value[:8] + "..." if value else "NOT SET"
        print(f"  {key}: {masked}")
    
    total_start = time.time()
    results = []
    
    # Step 0: Build Universe
    success, elapsed = run_step("Step 0: Build Universe", "00_build_universe")
    results.append(("Build Universe", success, elapsed))
    if not success:
        print("\nPipeline halted at Step 0")
        return
    
    # Steps 1-7: Build Credit Spreads
    success, elapsed = run_step("Steps 1-7: Build Credit Spreads", "01_build_spreads")
    results.append(("Build Spreads", success, elapsed))
    if not success:
        print("\nPipeline halted at Step 1-7")
        return
    
    # Steps 8-9: News Filter
    success, elapsed = run_step("Steps 8-9: News Filter", "02_news_filter")
    results.append(("News Filter", success, elapsed))
    if not success:
        print("\nPipeline halted at Step 8-9")
        return
    
    # Step 10: Portfolio Selection
    success, elapsed = run_step("Step 10: Portfolio Selection", "03_portfolio_select")
    results.append(("Portfolio Select", success, elapsed))
    
    # Summary
    total_elapsed = time.time() - total_start
    
    print("\n" + "="*70)
    print("PIPELINE SUMMARY")
    print("="*70)
    
    for name, success, elapsed in results:
        status = "✓" if success else "✗"
        print(f"{status} {name:20} {elapsed:8.1f}s")
    
    print("-" * 70)
    print(f"  {'TOTAL':20} {total_elapsed:8.1f}s")
    print("="*70)
    
    # Check output
    try:
        with open('final_trades.json', 'r') as f:
            trades = json.load(f)
        print(f"\n✓ Generated {len(trades)} trade recommendations")
        
        if len(trades) >= 5:
            print("✓ Ready for execution")
        else:
            print("⚠ Fewer than 5 trades - review recommended")
            
    except FileNotFoundError:
        print("\n✗ No final trades generated")
    
    print(f"\nFinished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == '__main__':
    main()
