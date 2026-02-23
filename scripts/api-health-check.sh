#!/bin/bash
# API Usage Monitor Script
# Run daily to check API limits and send alerts

echo "=== API Usage Check - $(date) ==="

# Check Hunter.io (if endpoint available)
# Hunter doesn't have a simple usage endpoint, but we can track manually
echo "Hunter.io: Manual tracking required (50 req/mo limit)"

# Check AlphaVantage (no direct usage API, need to track manually)
echo "AlphaVantage: Manual tracking required (25 calls/day limit)"

# Check Brave Search (no usage API on free tier)
echo "Brave Search: Manual tracking required (2,000 req/mo limit)"

# Check Zyte (has usage endpoint if API key set)
if [ -n "$ZYTE_API_KEY" ]; then
    echo "Zyte: Check https://app.zyte.com/billing for usage"
fi

# Check Abstract API
if [ -n "$ABSTRACT_API_KEY" ]; then
    echo "Abstract API: Check https://app.abstractapi.com for usage"
fi

echo ""
echo "=== RECOMMENDATIONS ==="
echo "1. Check API-TRACKER.md for manual usage logging"
echo "2. Review Hunter.io before email verification campaigns"
echo "3. Monitor AlphaVantage for trade recommendations"
echo "4. Set calendar reminder to review weekly"
