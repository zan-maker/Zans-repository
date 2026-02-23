/**
 * RiskManager - Enforces exposure limits and trading safety
 */

class RiskManager {
  constructor(config = {}) {
    this.limits = {
      maxPerOutcomeExposure: config.maxPerOutcomeExposure || 500,
      maxPerMarketExposure: config.maxPerMarketExposure || 1000,
      maxPerVenueDaily: config.maxPerVenueDaily || 2000,
      maxGlobalDailyLoss: config.maxGlobalDailyLoss || 5000,
      maxDrawdownPercent: config.maxDrawdownPercent || 20
    };
    
    this.exposures = {
      perOutcome: new Map(),
      perMarket: new Map(),
      perVenue: new Map(),
      dailyPnL: 0,
      peakBalance: 0,
      currentBalance: 0
    };
    
    this.killSwitch = config.killSwitch || false;
    this.tradeLog = [];
  }

  /**
   * Check if a trade passes all risk checks
   * @param {Object} trade - Trade proposal
   * @returns {Object} { allowed: boolean, reason: string }
   */
  checkTrade(trade) {
    if (this.killSwitch) {
      return { allowed: false, reason: 'Kill switch is active' };
    }

    const checks = [
      this._checkOutcomeExposure(trade),
      this._checkMarketExposure(trade),
      this._checkVenueExposure(trade),
      this._checkDailyLoss(trade),
      this._checkDrawdown(trade)
    ];

    const failed = checks.find(c => !c.passed);
    if (failed) {
      return { allowed: false, reason: failed.reason };
    }

    return { allowed: true, reason: 'All checks passed' };
  }

  /**
   * Check per-outcome exposure limit
   */
  _checkOutcomeExposure(trade) {
    const key = `${trade.venue}_${trade.marketId}_${trade.outcome}`;
    const current = this.exposures.perOutcome.get(key) || 0;
    const newExposure = current + trade.stake;
    
    if (newExposure > this.limits.maxPerOutcomeExposure) {
      return {
        passed: false,
        reason: `Per-outcome exposure limit exceeded: ${newExposure} > ${this.limits.maxPerOutcomeExposure}`
      };
    }
    
    return { passed: true };
  }

  /**
   * Check per-market exposure limit
   */
  _checkMarketExposure(trade) {
    const key = `${trade.venue}_${trade.marketId}`;
    const current = this.exposures.perMarket.get(key) || 0;
    const newExposure = current + trade.stake;
    
    if (newExposure > this.limits.maxPerMarketExposure) {
      return {
        passed: false,
        reason: `Per-market exposure limit exceeded: ${newExposure} > ${this.limits.maxPerMarketExposure}`
      };
    }
    
    return { passed: true };
  }

  /**
   * Check per-venue daily limit
   */
  _checkVenueExposure(trade) {
    const today = new Date().toISOString().split('T')[0];
    const key = `${trade.venue}_${today}`;
    const current = this.exposures.perVenue.get(key) || 0;
    const newExposure = current + trade.stake;
    
    if (newExposure > this.limits.maxPerVenueDaily) {
      return {
        passed: false,
        reason: `Per-venue daily limit exceeded: ${newExposure} > ${this.limits.maxPerVenueDaily}`
      };
    }
    
    return { passed: true };
  }

  /**
   * Check daily loss limit
   */
  _checkDailyLoss(trade) {
    const maxLoss = trade.stake; // Worst case is losing entire stake
    const projectedDailyLoss = this.exposures.dailyPnL - maxLoss;
    
    if (projectedDailyLoss < -this.limits.maxGlobalDailyLoss) {
      return {
        passed: false,
        reason: `Daily loss limit would be exceeded: ${Math.abs(projectedDailyLoss)} > ${this.limits.maxGlobalDailyLoss}`
      };
    }
    
    return { passed: true };
  }

  /**
   * Check drawdown limit
   */
  _checkDrawdown(trade) {
    const maxLoss = trade.stake;
    const projectedBalance = this.exposures.currentBalance - maxLoss;
    
    if (this.exposures.peakBalance > 0) {
      const drawdown = ((this.exposures.peakBalance - projectedBalance) / this.exposures.peakBalance) * 100;
      
      if (drawdown > this.limits.maxDrawdownPercent) {
        return {
          passed: false,
          reason: `Drawdown limit would be exceeded: ${drawdown.toFixed(2)}% > ${this.limits.maxDrawdownPercent}%`
        };
      }
    }
    
    return { passed: true };
  }

  /**
   * Record a trade that passed risk checks
   */
  recordTrade(trade, result) {
    // Update exposures
    const outcomeKey = `${trade.venue}_${trade.marketId}_${trade.outcome}`;
    const marketKey = `${trade.venue}_${trade.marketId}`;
    const venueKey = `${trade.venue}_${new Date().toISOString().split('T')[0]}`;
    
    this.exposures.perOutcome.set(outcomeKey, 
      (this.exposures.perOutcome.get(outcomeKey) || 0) + trade.stake);
    
    this.exposures.perMarket.set(marketKey,
      (this.exposures.perMarket.get(marketKey) || 0) + trade.stake);
    
    this.exposures.perVenue.set(venueKey,
      (this.exposures.perVenue.get(venueKey) || 0) + trade.stake);
    
    // Log trade
    this.tradeLog.push({
      timestamp: new Date().toISOString(),
      trade,
      result,
      exposures: this.getExposureSummary()
    });
  }

  /**
   * Update balance and track peak
   */
  updateBalance(balance) {
    this.exposures.currentBalance = balance;
    
    if (balance > this.exposures.peakBalance) {
      this.exposures.peakBalance = balance;
    }
  }

  /**
   * Record P&L from settled trades
   */
  recordPnL(pnl) {
    this.exposures.dailyPnL += pnl;
  }

  /**
   * Activate kill switch (emergency stop)
   */
  activateKillSwitch(reason) {
    this.killSwitch = true;
    console.error(`🚨 KILL SWITCH ACTIVATED: ${reason}`);
    this.tradeLog.push({
      timestamp: new Date().toISOString(),
      type: 'KILL_SWITCH',
      reason
    });
  }

  /**
   * Deactivate kill switch
   */
  deactivateKillSwitch() {
    this.killSwitch = false;
    console.log('✅ Kill switch deactivated');
  }

  /**
   * Get current exposure summary
   */
  getExposureSummary() {
    return {
      perOutcome: Object.fromEntries(this.exposures.perOutcome),
      perMarket: Object.fromEntries(this.exposures.perMarket),
      perVenue: Object.fromEntries(this.exposures.perVenue),
      dailyPnL: this.exposures.dailyPnL,
      peakBalance: this.exposures.peakBalance,
      currentBalance: this.exposures.currentBalance,
      drawdown: this.exposures.peakBalance > 0 
        ? ((this.exposures.peakBalance - this.exposures.currentBalance) / this.exposures.peakBalance * 100).toFixed(2) + '%'
        : '0%'
    };
  }

  /**
   * Reset daily counters (call at midnight)
   */
  resetDailyCounters() {
    // Keep per-outcome and per-market (these are position limits)
    // Reset venue daily and P&L
    const yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);
    const yesterdayKey = yesterday.toISOString().split('T')[0];
    
    // Remove yesterday's venue entries
    for (const key of this.exposures.perVenue.keys()) {
      if (key.endsWith(yesterdayKey)) {
        this.exposures.perVenue.delete(key);
      }
    }
    
    this.exposures.dailyPnL = 0;
    console.log('📊 Daily counters reset');
  }

  /**
   * Get trade log
   */
  getTradeLog(limit = 100) {
    return this.tradeLog.slice(-limit);
  }
}

module.exports = { RiskManager };
