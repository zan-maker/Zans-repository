/**
 * MispricingEngine - Core arbitrage and mispricing detection
 */

class MispricingEngine {
  constructor(config = {}) {
    this.minArbitrageProfitPercent = config.minArbitrageProfitPercent || 2.0;
    this.minEVPercent = config.minEVPercent || 5.0;
    this.maxHoldPercent = config.maxHoldPercent || 10.0; // Ignore books with >10% vig
  }

  /**
   * Find arbitrage opportunities between Kalshi and sportsbooks
   * @param {Array} events - Canonical events with Kalshi and sportsbook data
   * @returns {Array} Arbitrage opportunities
   */
  findArbitrageOpportunities(events) {
    const opportunities = [];

    for (const event of events) {
      const arb = this._checkEventForArbitrage(event);
      if (arb) {
        opportunities.push(arb);
      }
    }

    return opportunities.sort((a, b) => b.profitPercent - a.profitPercent);
  }

  /**
   * Check a single event for arbitrage
   */
  _checkEventForArbitrage(event) {
    if (!event.kalshi || !event.sportsbook) return null;

    const kalshiProb = event.kalshi.impliedProbability;
    const bookProb = event.sportsbook.impliedProbability;
    const bookVig = event.sportsbook.vigAdjusted;

    // Check both sides for arbitrage
    const opportunities = [];

    // Case 1: Long Kalshi Yes, Short Sportsbook (or vice versa)
    if (kalshiProb.yes < bookVig.no) {
      const profit = this._calculateArbitrageProfit(
        kalshiProb.yes,
        bookVig.no,
        event.kalshi.fee,
        event.sportsbook.fee
      );
      
      if (profit.percent >= this.minArbitrageProfitPercent) {
        opportunities.push({
          type: 'arbitrage',
          event: event.name,
          sport: event.sport,
          kalshiTrade: { side: 'yes', probability: kalshiProb.yes },
          sportsbookTrade: { outcome: event.sportsbook.outcomes.no, probability: bookVig.no },
          profitPercent: profit.percent,
          expectedProfit: profit.amount,
          stakes: profit.stakes
        });
      }
    }

    // Case 2: Long Kalshi No, Short Sportsbook Yes
    if (kalshiProb.no < bookVig.yes) {
      const profit = this._calculateArbitrageProfit(
        kalshiProb.no,
        bookVig.yes,
        event.kalshi.fee,
        event.sportsbook.fee
      );
      
      if (profit.percent >= this.minArbitrageProfitPercent) {
        opportunities.push({
          type: 'arbitrage',
          event: event.name,
          sport: event.sport,
          kalshiTrade: { side: 'no', probability: kalshiProb.no },
          sportsbookTrade: { outcome: event.sportsbook.outcomes.yes, probability: bookVig.yes },
          profitPercent: profit.percent,
          expectedProfit: profit.amount,
          stakes: profit.stakes
        });
      }
    }

    return opportunities.length > 0 ? opportunities[0] : null;
  }

  /**
   * Calculate arbitrage profit and optimal stakes
   */
  _calculateArbitrageProfit(probA, probB, feeA = 0, feeB = 0) {
    // Convert probabilities to decimal odds
    const oddsA = 1 / probA;
    const oddsB = 1 / probB;

    // Calculate implied stake ratio
    const stakeRatio = oddsB / (oddsA + oddsB);

    // Assume $100 total stake for calculation
    const totalStake = 100;
    const stakeA = totalStake * stakeRatio;
    const stakeB = totalStake - stakeA;

    // Calculate payouts
    const payoutA = stakeA * oddsA * (1 - feeA);
    const payoutB = stakeB * oddsB * (1 - feeB);

    // Profit is the minimum payout minus total stake
    const minPayout = Math.min(payoutA, payoutB);
    const profit = minPayout - totalStake;
    const profitPercent = (profit / totalStake) * 100;

    return {
      percent: profitPercent,
      amount: profit,
      stakes: {
        total: totalStake,
        a: stakeA,
        b: stakeB
      }
    };
  }

  /**
   * Find value opportunities (directional mispricings)
   * @param {Array} events - Canonical events
   * @param {Object} fairProbabilities - User's fair probability estimates
   * @returns {Array} Value opportunities
   */
  findValueOpportunities(events, fairProbabilities = {}) {
    const opportunities = [];

    for (const event of events) {
      const fairProb = fairProbabilities[event.id] || this._estimateFairProbability(event);
      if (!fairProb) continue;

      const value = this._checkEventForValue(event, fairProb);
      if (value && value.ev >= this.minEVPercent) {
        opportunities.push(value);
      }
    }

    return opportunities.sort((a, b) => b.ev - a.ev);
  }

  /**
   * Check event for value against fair probability
   */
  _checkEventForValue(event, fairProb) {
    const opportunities = [];

    // Check Kalshi Yes
    if (event.kalshi) {
      const kalshiYesEV = this._calculateEV(fairProb.yes, event.kalshi.price.yes, event.kalshi.fee);
      if (kalshiYesEV >= this.minEVPercent) {
        opportunities.push({
          venue: 'kalshi',
          side: 'yes',
          event: event.name,
          fairProbability: fairProb.yes,
          marketPrice: event.kalshi.price.yes,
          ev: kalshiYesEV
        });
      }

      // Check Kalshi No
      const kalshiNoEV = this._calculateEV(fairProb.no, event.kalshi.price.no, event.kalshi.fee);
      if (kalshiNoEV >= this.minEVPercent) {
        opportunities.push({
          venue: 'kalshi',
          side: 'no',
          event: event.name,
          fairProbability: fairProb.no,
          marketPrice: event.kalshi.price.no,
          ev: kalshiNoEV
        });
      }
    }

    // Check Sportsbook
    if (event.sportsbook) {
      for (const outcome of event.sportsbook.outcomes) {
        const ev = this._calculateEV(
          fairProb[outcome.id],
          outcome.probability,
          event.sportsbook.fee
        );
        
        if (ev >= this.minEVPercent) {
          opportunities.push({
            venue: event.sportsbook.name,
            outcome: outcome.name,
            event: event.name,
            fairProbability: fairProb[outcome.id],
            marketPrice: outcome.probability,
            ev: ev
          });
        }
      }
    }

    return opportunities.length > 0 ? opportunities[0] : null;
  }

  /**
   * Calculate expected value
   */
  _calculateEV(fairProb, marketProb, fee = 0) {
    const fairOdds = 1 / fairProb;
    const marketOdds = 1 / marketProb;
    const winAmount = (fairOdds - 1) * (1 - fee);
    const loseAmount = -1;
    
    const winProb = fairProb;
    const loseProb = 1 - fairProb;
    
    const ev = (winProb * winAmount) + (loseProb * loseAmount);
    return ev * 100; // Return as percentage
  }

  /**
   * Estimate fair probability from market consensus
   * Simple average of vig-adjusted probabilities
   */
  _estimateFairProbability(event) {
    const probs = [];

    if (event.kalshi?.impliedProbability) {
      probs.push(event.kalshi.impliedProbability);
    }

    if (event.sportsbook?.vigAdjusted) {
      probs.push(event.sportsbook.vigAdjusted);
    }

    if (probs.length === 0) return null;

    // Average the probabilities
    const avgYes = probs.reduce((sum, p) => sum + p.yes, 0) / probs.length;
    const avgNo = probs.reduce((sum, p) => sum + p.no, 0) / probs.length;

    // Normalize
    const total = avgYes + avgNo;
    return {
      yes: avgYes / total,
      no: avgNo / total
    };
  }

  /**
   * Convert Kalshi price to fee-adjusted probability
   * Kalshi charges fees on winning trades
   */
  static kalshiPriceToProbability(price, feePercent = 0) {
    const impliedProb = price / 10000;
    return impliedProb * (1 - feePercent);
  }

  /**
   * Calculate Kelly criterion stake
   * @param {number} fairProb - Fair probability
   * @param {number} marketProb - Market implied probability
   * @param {number} bankroll - Total bankroll
   * @returns {number} Recommended stake as percentage of bankroll
   */
  static kellyCriterion(fairProb, marketProb, bankroll) {
    const b = (1 / marketProb) - 1; // Decimal odds minus 1
    const p = fairProb;
    const q = 1 - p;
    
    const kelly = (b * p - q) / b;
    
    // Return half-Kelly for safety
    return Math.max(0, kelly * 0.5 * bankroll);
  }
}

module.exports = { MispricingEngine };
