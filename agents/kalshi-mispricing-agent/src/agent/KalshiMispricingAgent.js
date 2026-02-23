/**
 * KalshiMispricingAgent - Main orchestrator
 * Coordinates scanning, mispricing detection, and trading
 */

const { KalshiClient } = require('../clients/KalshiClient');
const { MispricingEngine } = require('../engine/MispricingEngine');
const { RiskManager } = require('../risk/RiskManager');

class KalshiMispricingAgent {
  constructor(config = {}) {
    this.kalshi = new KalshiClient(config.kalshi);
    this.engine = new MispricingEngine(config.engine);
    this.risk = new RiskManager(config.risk);
    
    this.sportsbooks = new Map();
    this.isRunning = false;
    this.scanInterval = config.scanInterval || 30000; // 30 seconds
    this.eventMappings = new Map(); // Kalshi event -> Sportsbook event mapping
    
    // Performance tracking
    this.performance = {
      scans: 0,
      opportunitiesFound: 0,
      tradesExecuted: 0,
      totalPnL: 0
    };
  }

  /**
   * Register a sportsbook adapter
   */
  registerSportsbook(name, client) {
    this.sportsbooks.set(name, client);
    console.log(`✅ Registered sportsbook: ${name}`);
  }

  /**
   * Start the agent
   */
  async start() {
    if (this.isRunning) {
      console.log('Agent is already running');
      return;
    }

    this.isRunning = true;
    console.log('🚀 Kalshi Mispricing Agent started');

    // Initial scan
    await this.scan();

    // Schedule recurring scans
    this.scanTimer = setInterval(() => this.scan(), this.scanInterval);

    // Schedule daily reset
    this.scheduleDailyReset();
  }

  /**
   * Stop the agent
   */
  stop() {
    this.isRunning = false;
    if (this.scanTimer) {
      clearInterval(this.scanTimer);
    }
    console.log('🛑 Agent stopped');
  }

  /**
   * Main scan loop
   */
  async scan() {
    try {
      console.log(`\n🔍 Scanning at ${new Date().toISOString()}`);
      
      // Fetch Kalshi events
      const kalshiEvents = await this.fetchKalshiEvents();
      
      // Fetch sportsbook events
      const sportsbookEvents = await this.fetchSportsbookEvents();
      
      // Map events
      const canonicalEvents = this.mapEvents(kalshiEvents, sportsbookEvents);
      
      // Find arbitrage opportunities
      const arbitrage = this.engine.findArbitrageOpportunities(canonicalEvents);
      
      // Find value opportunities
      const value = this.engine.findValueOpportunities(canonicalEvents);
      
      this.performance.scans++;
      this.performance.opportunitiesFound += arbitrage.length + value.length;

      console.log(`📊 Found ${arbitrage.length} arbitrage, ${value.length} value opportunities`);

      // Report top opportunities
      if (arbitrage.length > 0) {
        console.log('\n🎯 Top Arbitrage Opportunities:');
        arbitrage.slice(0, 3).forEach((opp, i) => {
          console.log(`  ${i + 1}. ${opp.event} - ${opp.profitPercent.toFixed(2)}% profit`);
        });
      }

      if (value.length > 0) {
        console.log('\n💰 Top Value Opportunities:');
        value.slice(0, 3).forEach((opp, i) => {
          console.log(`  ${i + 1}. ${opp.event} - ${opp.ev.toFixed(2)}% EV`);
        });
      }

      return { arbitrage, value };

    } catch (error) {
      console.error('❌ Scan error:', error);
    }
  }

  /**
   * Fetch Kalshi events and market data
   */
  async fetchKalshiEvents() {
    const events = [];
    let cursor = null;
    
    do {
      const response = await this.kalshi.getEvents('active', cursor);
      
      for (const event of response.events || []) {
        try {
          const markets = await this.kalshi.getMarkets(event.id);
          
          for (const market of markets.markets || []) {
            const orderBook = await this.kalshi.getOrderBook(market.id);
            const impliedProb = KalshiClient.getImpliedProbabilityFromOrderBook(orderBook);
            
            events.push({
              id: event.id,
              marketId: market.id,
              name: event.title,
              sport: event.category,
              startTime: event.open_time,
              impliedProbability: impliedProb,
              orderBook: orderBook
            });
          }
        } catch (err) {
          console.warn(`Failed to fetch market data for event ${event.id}:`, err.message);
        }
      }
      
      cursor = response.cursor;
    } while (cursor && events.length < 100); // Limit to 100 events

    return events;
  }

  /**
   * Fetch sportsbook events
   */
  async fetchSportsbookEvents() {
    const allEvents = [];
    
    for (const [name, client] of this.sportsbooks) {
      try {
        const events = await client.getEvents();
        allEvents.push(...events.map(e => ({ ...e, bookName: name })));
      } catch (err) {
        console.warn(`Failed to fetch events from ${name}:`, err.message);
      }
    }

    return allEvents;
  }

  /**
   * Map Kalshi events to sportsbook events
   */
  mapEvents(kalshiEvents, sportsbookEvents) {
    const canonical = [];

    for (const kEvent of kalshiEvents) {
      // Find matching sportsbook event
      const match = this.findMatchingEvent(kEvent, sportsbookEvents);
      
      if (match) {
        canonical.push({
          id: `${kEvent.id}_${match.bookName}`,
          name: kEvent.name,
          sport: kEvent.sport,
          startTime: kEvent.startTime,
          kalshi: {
            eventId: kEvent.id,
            marketId: kEvent.marketId,
            impliedProbability: kEvent.impliedProbability,
            price: {
              yes: kEvent.impliedProbability.yes * 10000,
              no: kEvent.impliedProbability.no * 10000
            },
            fee: 0 // Kalshi fees are on settlement
          },
          sportsbook: {
            name: match.bookName,
            eventId: match.id,
            impliedProbability: match.impliedProbability,
            vigAdjusted: match.vigAdjusted,
            outcomes: match.outcomes,
            fee: 0 // Sportsbook fees are built into odds
          }
        });
      }
    }

    return canonical;
  }

  /**
   * Find matching sportsbook event for a Kalshi event
   */
  findMatchingEvent(kalshiEvent, sportsbookEvents) {
    // Simple string matching - in production use ML/Fuzzy matching
    const kName = kalshiEvent.name.toLowerCase();
    
    return sportsbookEvents.find(sEvent => {
      const sName = sEvent.name.toLowerCase();
      
      // Check for common team/player names
      const commonTerms = kName.split(' ').filter(w => w.length > 3);
      const matches = commonTerms.filter(term => sName.includes(term));
      
      // Need at least 2 matching terms and same sport
      return matches.length >= 2 && sEvent.sport === kalshiEvent.sport;
    });
  }

  /**
   * Execute an arbitrage trade
   */
  async executeArbitrage(opportunity) {
    console.log(`\n🎯 Executing arbitrage: ${opportunity.event}`);

    // Calculate stakes
    const totalStake = 100; // Start small
    const kalshiStake = totalStake * 0.5;
    const bookStake = totalStake * 0.5;

    // Risk check
    const kalshiTrade = {
      venue: 'kalshi',
      marketId: opportunity.kalshiTrade.marketId,
      outcome: opportunity.kalshiTrade.side,
      stake: kalshiStake
    };

    const bookTrade = {
      venue: opportunity.sportsbookTrade.venue || 'sportsbook',
      marketId: opportunity.sportsbookTrade.marketId,
      outcome: opportunity.sportsbookTrade.outcome,
      stake: bookStake
    };

    const kCheck = this.risk.checkTrade(kalshiTrade);
    const bCheck = this.risk.checkTrade(bookTrade);

    if (!kCheck.allowed) {
      console.log(`❌ Kalshi trade rejected: ${kCheck.reason}`);
      return;
    }

    if (!bCheck.allowed) {
      console.log(`❌ Sportsbook trade rejected: ${bCheck.reason}`);
      return;
    }

    try {
      // Place Kalshi order
      const kalshiPrice = Math.round(opportunity.kalshiTrade.probability * 10000);
      const kalshiResult = await this.kalshi.placeOrder(
        opportunity.kalshiTrade.marketId,
        opportunity.kalshiTrade.side,
        kalshiStake,
        kalshiPrice
      );

      // Place sportsbook bet
      const bookClient = this.sportsbooks.get(opportunity.sportsbookTrade.venue);
      const bookResult = await bookClient.placeBet(
        opportunity.sportsbookTrade.marketId,
        opportunity.sportsbookTrade.outcome,
        bookStake,
        opportunity.sportsbookTrade.probability
      );

      // Record trades
      this.risk.recordTrade(kalshiTrade, kalshiResult);
      this.risk.recordTrade(bookTrade, bookResult);

      this.performance.tradesExecuted += 2;

      console.log('✅ Arbitrage executed successfully');

      return { kalshi: kalshiResult, sportsbook: bookResult };

    } catch (error) {
      console.error('❌ Trade execution failed:', error);
      // TODO: Handle partial fills - cancel other leg
    }
  }

  /**
   * Get natural language report
   */
  async getReport(query) {
    const summary = {
      status: this.isRunning ? 'Running' : 'Stopped',
      scans: this.performance.scans,
      opportunities: this.performance.opportunitiesFound,
      trades: this.performance.tradesExecuted,
      exposures: this.risk.getExposureSummary()
    };

    if (query.includes('arbitrage') || query.includes('opportunities')) {
      const { arbitrage } = await this.scan();
      return {
        ...summary,
        arbitrageOpportunities: arbitrage
      };
    }

    if (query.includes('exposure') || query.includes('risk')) {
      return {
        ...summary,
        exposures: this.risk.getExposureSummary()
      };
    }

    return summary;
  }

  /**
   * Schedule daily reset
   */
  scheduleDailyReset() {
    const now = new Date();
    const tomorrow = new Date(now);
    tomorrow.setDate(tomorrow.getDate() + 1);
    tomorrow.setHours(0, 5, 0, 0); // 5 minutes past midnight

    const msUntilMidnight = tomorrow - now;

    setTimeout(() => {
      this.risk.resetDailyCounters();
      // Schedule next reset
      setInterval(() => this.risk.resetDailyCounters(), 24 * 60 * 60 * 1000);
    }, msUntilMidnight);
  }
}

module.exports = { KalshiMispricingAgent };
