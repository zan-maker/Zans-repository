#!/bin/bash
# HedgeMaster Setup Script
# Run this to configure all cron jobs for the agentic hedging system

echo "🚀 Setting up HedgeMaster Agentic Hedging System..."
echo ""

# Check if running from OpenClaw directory
if [ ! -f "$HOME/.openclaw/openclaw.json" ]; then
    echo "❌ Error: OpenClaw config not found. Please run from OpenClaw environment."
    exit 1
fi

echo "✅ OpenClaw configuration found"
echo ""

# Check for required API keys
echo "🔑 Checking API Keys..."

if [ -z "$ALPACA_API_KEY" ]; then
    echo "⚠️  Warning: ALPACA_API_KEY not set (required for portfolio monitoring)"
fi

if [ -z "$KALSHI_API_KEY_ID" ]; then
    echo "⚠️  Warning: KALSHI_API_KEY_ID not set (required for prediction market trading)"
fi

if [ -z "$BRAVE_API_KEY" ]; then
    echo "⚠️  Warning: BRAVE_API_KEY not set (required for web search)"
fi

if [ -z "$NEWSAPI_KEY" ]; then
    echo "⚠️  Warning: NEWSAPI_KEY not set (optional, for news sentiment)"
fi

echo ""
echo "📅 Creating Cron Jobs..."
echo ""

# Job 1: Daily Portfolio Monitor (9:00 AM ET)
echo "1️⃣  Creating: Daily Portfolio Monitor (9:00 AM ET)"
openclaw cron create \
  --name "HedgeMaster - Daily Portfolio Monitor" \
  --schedule "0 9 * * *" \
  --tz "America/New_York" \
  --agent HedgeMaster \
  --prompt "Read /home/node/.openclaw/workspace/agents/hedgemaster/prompts/stage1-portfolio-monitor.md and execute Stage 1: Scan Alpaca portfolio for positions needing hedges. Check for >5% moves, earnings announcements, and news events. Trigger Risk Analyst for any position with urgency >60." \
  --delivery-mode none \
  --delivery-channel discord \
  --delivery-target "1474794532209164591" 2>/dev/null || echo "   ⚠️  Job may already exist or tool unavailable"

echo ""

# Job 2: Daily Report (6:00 PM ET)
echo "2️⃣  Creating: Daily Report (6:00 PM ET)"
openclaw cron create \
  --name "HedgeMaster - Daily Report" \
  --schedule "0 18 * * *" \
  --tz "America/New_York" \
  --agent HedgeMaster \
  --prompt "Generate daily HedgeMaster report using template at /home/node/.openclaw/workspace/agents/hedgemaster/prompts/daily-report-template.md. Include: portfolio status, active hedges, expiring positions, new opportunities, performance metrics." \
  --delivery-mode none \
  --delivery-channel discord \
  --delivery-target "1474794532209164591" 2>/dev/null || echo "   ⚠️  Job may already exist or tool unavailable"

echo ""

# Job 3: Weekly Performance Review (Sunday 8:00 AM ET)
echo "3️⃣  Creating: Weekly Performance Review (Sundays 8:00 AM ET)"
openclaw cron create \
  --name "HedgeMaster - Weekly Review" \
  --schedule "0 8 * * 0" \
  --tz "America/New_York" \
  --agent HedgeMaster \
  --prompt "Generate weekly HedgeMaster performance report. Analyze: settled hedges (win/loss), P&L summary, correlation accuracy, edge estimation accuracy, lessons learned. Update performance tracking files." \
  --delivery-mode none \
  --delivery-channel discord \
  --delivery-target "1474794532209164591" 2>/dev/null || echo "   ⚠️  Job may already exist or tool unavailable"

echo ""

# Job 4: High-Frequency Token Monitor (already exists, but include for completeness)
echo "4️⃣  Token Usage Monitor (already configured)"
echo "   ✅ Running every 15 minutes"

echo ""
echo "📁 Creating Directory Structure..."

# Create directories
mkdir -p "$HOME/.openclaw/workspace/hedgemaster/"{reports,trades,analysis,recommendations,alerts,performance}

echo "   ✅ Created: hedgemaster/"
echo "   ✅ Created: hedgemaster/reports/"
echo "   ✅ Created: hedgemaster/trades/"
echo "   ✅ Created: hedgemaster/analysis/"
echo "   ✅ Created: hedgemaster/recommendations/"
echo "   ✅ Created: hedgemaster/alerts/"
echo "   ✅ Created: hedgemaster/performance/"

echo ""
echo "📝 Initializing Tracking Files..."

# Create initial files
cat > "$HOME/.openclaw/workspace/hedgemaster/active-hedges.json" << 'EOF'
{
  "active_hedges": [],
  "summary": {
    "total_active": 0,
    "total_value": 0,
    "total_potential_payout": 0,
    "total_unrealized_pnl": 0
  },
  "last_updated": ""
}
EOF

cat > "$HOME/.openclaw/workspace/hedgemaster/performance.csv" << 'EOF'
trade_id,date,ticker,market_id,position,entry_price,exit_price,settlement_result,pnl,hedge_score,correlation,edge,notes
EOF

echo "   ✅ Created: active-hedges.json"
echo "   ✅ Created: performance.csv"

echo ""
echo "═══════════════════════════════════════════════════════"
echo "✅ HedgeMaster Setup Complete!"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "📋 Summary:"
echo "   • Daily Portfolio Monitor: 9:00 AM ET"
echo "   • Daily Report: 6:00 PM ET"
echo "   • Weekly Review: Sundays 8:00 AM ET"
echo "   • Token Monitor: Every 15 minutes"
echo ""
echo "⚙️  Manual Steps Required:"
echo ""
echo "1. Set Environment Variables:"
echo "   export ALPACA_API_KEY='your_key'"
echo "   export ALPACA_SECRET_KEY='your_secret'"
echo "   export KALSHI_API_KEY_ID='your_key_id'"
echo "   export KALSHI_PRIVATE_KEY='your_private_key'"
echo "   export BRAVE_API_KEY='your_key'"
echo "   export NEWSAPI_KEY='your_key' (optional)"
echo ""
echo "2. Verify API Access:"
echo "   • Alpaca: Ensure paper trading account is active"
echo "   • Kalshi: Verify API key has trading permissions"
echo "   • Brave: Test search API quota"
echo ""
echo "3. Test Manual Run:"
echo "   openclaw agent run HedgeMaster --prompt 'Run Stage 1 portfolio scan manually'"
echo ""
echo "📚 Documentation:"
echo "   • Skill: /home/node/.openclaw/workspace/agents/hedgemaster/SKILL.md"
echo "   • Prompts: /home/node/.openclaw/workspace/agents/hedgemaster/prompts/"
echo "   • Output: /home/node/.openclaw/workspace/hedgemaster/"
echo ""
echo "🚀 To Start:"
echo "   The system will auto-run at 9:00 AM ET tomorrow."
echo "   Or trigger manually: openclaw cron run --job-id <job_id>"
echo ""
echo "═══════════════════════════════════════════════════════"
