#!/usr/bin/env node
/**
 * Kalshi Sportsbook Mispricing Agent
 * Main entry point
 */

require('dotenv').config();

const { KalshiMispricingAgent } = require('./src/agent/KalshiMispricingAgent');

// Configuration
const config = {
  kalshi: {
    apiKeyId: process.env.KALSHI_API_KEY_ID,
    privateKeyPath: process.env.KALSHI_PRIVATE_KEY_PATH
  },
  engine: {
    minArbitrageProfitPercent: parseFloat(process.env.MIN_ARBITRAGE_PROFIT) || 2.0,
    minEVPercent: parseFloat(process.env.MIN_EV_PERCENT) || 5.0,
    maxHoldPercent: parseFloat(process.env.MAX_HOLD_PERCENT) || 10.0
  },
  risk: {
    maxPerOutcomeExposure: parseFloat(process.env.MAX_PER_OUTCOME) || 500,
    maxPerMarketExposure: parseFloat(process.env.MAX_PER_MARKET) || 1000,
    maxPerVenueDaily: parseFloat(process.env.MAX_PER_VENUE_DAILY) || 2000,
    maxGlobalDailyLoss: parseFloat(process.env.MAX_DAILY_LOSS) || 5000,
    maxDrawdownPercent: parseFloat(process.env.MAX_DRAWDOWN) || 20,
    killSwitch: process.env.KILL_SWITCH === 'true'
  },
  scanInterval: parseInt(process.env.SCAN_INTERVAL) || 30000
};

// Create agent
const agent = new KalshiMispricingAgent(config);

// CLI commands
const command = process.argv[2];

async function main() {
  switch (command) {
    case 'start':
      await agent.start();
      break;
      
    case 'stop':
      agent.stop();
      process.exit(0);
      break;
      
    case 'scan':
      const result = await agent.scan();
      console.log(JSON.stringify(result, null, 2));
      process.exit(0);
      break;
      
    case 'status':
      const status = await agent.getReport('status');
      console.log(JSON.stringify(status, null, 2));
      process.exit(0);
      break;
      
    case 'kill':
      agent.risk.activateKillSwitch('Manual activation');
      process.exit(0);
      break;
      
    case 'unkill':
      agent.risk.deactivateKillSwitch();
      process.exit(0);
      break;
      
    default:
      console.log(`
Kalshi Sportsbook Mispricing Agent

Usage:
  npm start [command]

Commands:
  start    Start the agent (continuous scanning)
  stop     Stop the agent
  scan     Run a single scan and output results
  status   Get current status and exposures
  kill     Activate kill switch (emergency stop)
  unkill   Deactivate kill switch

Environment Variables:
  KALSHI_API_KEY_ID         Kalshi API key ID
  KALSHI_PRIVATE_KEY_PATH   Path to private key file
  MIN_ARBITRAGE_PROFIT      Minimum arbitrage profit % (default: 2.0)
  MIN_EV_PERCENT            Minimum expected value % (default: 5.0)
  SCAN_INTERVAL             Scan interval in ms (default: 30000)
  MAX_PER_OUTCOME           Max exposure per outcome (default: 500)
  MAX_PER_MARKET            Max exposure per market (default: 1000)
  MAX_DAILY_LOSS            Max daily loss limit (default: 5000)
      `);
      process.exit(0);
  }
}

main().catch(console.error);
