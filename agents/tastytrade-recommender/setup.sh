#!/bin/bash
# TastyTrade Recommender Setup Script
# Sets up automated options recommendations for $100 account

echo "🎯 Setting up TastyTrade Options Recommender..."
echo "Account Size: $100 (Small Account Strategy)"
echo ""

# Check OpenClaw environment
if [ ! -f "$HOME/.openclaw/openclaw.json" ]; then
    echo "❌ Error: OpenClaw config not found"
    exit 1
fi

echo "✅ OpenClaw environment verified"
echo ""

# Create directories
mkdir -p "$HOME/.openclaw/workspace/tastytrade/"{recommendations,trades,performance}
echo "✅ Created tastytrade/ directory structure"

# Initialize tracking files
cat > "$HOME/.openclaw/workspace/tastytrade/performance.csv" << 'EOF'
date,underlying,strategy,credit,result,pnl,balance,notes
EOF

cat > "$HOME/.openclaw/workspace/tastytrade/active-trades.json" << 'EOF'
{
  "active_trades": [],
  "account_balance": 100,
  "available_buying_power": 100,
  "last_updated": ""
}
EOF

echo "✅ Initialized tracking files"
echo ""

# Set environment variable
echo "🔑 Configuring API Key..."
export TASTYTRADE_API_KEY="80e479d6235f546b188f9c86ec53bf80019c4bff"

# Add to bashrc for persistence
echo "" >> ~/.bashrc
echo "# TastyTrade API" >> ~/.bashrc
echo 'export TASTYTRADE_API_KEY="80e479d6235f546b188f9c86ec53bf80019c4bff"' >> ~/.bashrc

echo "✅ API key configured"
echo ""

# Note about cron jobs
echo "📅 Cron Job Schedule:"
echo ""
echo "The following cron jobs will be created:"
echo "  1. TastyTrade Morning Scan - 9:30 AM ET daily"
echo "  2. TastyTrade Midday Check - 12:00 PM ET daily"
echo "  3. TastyTrade Pre-Close - 3:30 PM ET daily"
echo ""
echo "To create these jobs, run:"
echo "  openclaw cron create --name 'TastyTrade-Morning' --schedule '30 9 * * *' ..."
echo ""

echo "═══════════════════════════════════════════════════════"
echo "✅ TastyTrade Recommender Setup Complete!"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "📋 Configuration Summary:"
echo "   • API Key: Configured"
echo "   • Account: $100 small account"
echo "   • Strategy: High-probability credit spreads"
echo "   • Max Trade: $20 (20% of account)"
echo "   • Max Positions: 3 ($60 buying power)"
echo ""
echo "⚙️  Manual Steps:"
echo ""
echo "1. Verify API access:"
echo "   curl -H 'Authorization: 80e479d6235f546b188f9c86ec53bf80019c4bff'"
echo "        https://api.tastytrade.com/accounts"
echo ""
echo "2. Test manual scan:"
echo "   openclaw agent run TastyTrade-Recommender"
echo "        --prompt 'Scan SPY for bull put spread opportunities'"
echo ""
echo "3. Set up cron jobs (see SKILL.md for commands)"
echo ""
echo "📚 Documentation:"
echo "   • Skill: agents/tastytrade-recommender/SKILL.md"
echo "   • Prompts: agents/tastytrade-recommender/prompts/"
echo "   • Output: tastytrade/"
echo ""
echo "🚀 Ready to trade!"
echo "═══════════════════════════════════════════════════════"
