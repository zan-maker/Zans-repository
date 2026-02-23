/**
 * SportsbookClient Interface
 * Standardized API for interacting with sportsbooks
 */

class SportsbookClient {
  constructor(config = {}) {
    this.name = config.name || 'GenericSportsbook';
    this.baseUrl = config.baseUrl;
    this.apiKey = config.apiKey;
    this.minRequestInterval = config.minRequestInterval || 1000;
    this.lastRequestTime = 0;
  }

  /**
   * Rate-limited request wrapper
   */
  async _throttledRequest(requestFn) {
    const now = Date.now();
    const timeSinceLastRequest = now - this.lastRequestTime;
    if (timeSinceLastRequest < this.minRequestInterval) {
      await new Promise(resolve => 
        setTimeout(resolve, this.minRequestInterval - timeSinceLastRequest)
      );
    }
    this.lastRequestTime = Date.now();
    return requestFn();
  }

  /**
   * Get odds for a specific event
   * @param {string} eventId - Sportsbook's event identifier
   * @returns {Promise<Object>} Odds data with markets and outcomes
   */
  async getOdds(eventId) {
    throw new Error('getOdds must be implemented by subclass');
  }

  /**
   * Place a bet
   * @param {string} eventId - Event identifier
   * @param {string} marketId - Market identifier
   * @param {string} outcome - Outcome selection
   * @param {number} stake - Bet amount in dollars
   * @param {number} priceLimit - Minimum acceptable odds
   * @returns {Promise<Object>} Bet confirmation
   */
  async placeBet(eventId, marketId, outcome, stake, priceLimit) {
    throw new Error('placeBet must be implemented by subclass');
  }

  /**
   * Get open bets
   * @returns {Promise<Array>} List of open bets
   */
  async getOpenBets() {
    throw new Error('getOpenBets must be implemented by subclass');
  }

  /**
   * Get account balance
   * @returns {Promise<number>} Balance in dollars
   */
  async getBalance() {
    throw new Error('getBalance must be implemented by subclass');
  }

  /**
   * Convert American odds to implied probability
   * @param {number} odds - American odds (+150, -200, etc.)
   * @returns {number} Implied probability (0-1)
   */
  static americanOddsToProbability(odds) {
    if (odds > 0) {
      return 100 / (odds + 100);
    } else {
      return Math.abs(odds) / (Math.abs(odds) + 100);
    }
  }

  /**
   * Convert decimal odds to implied probability
   * @param {number} odds - Decimal odds (2.5, 1.8, etc.)
   * @returns {number} Implied probability (0-1)
   */
  static decimalOddsToProbability(odds) {
    return 1 / odds;
  }

  /**
   * Convert fractional odds to implied probability
   * @param {string} odds - Fractional odds ("3/2", "5/1", etc.)
   * @returns {number} Implied probability (0-1)
   */
  static fractionalOddsToProbability(odds) {
    const [numerator, denominator] = odds.split('/').map(Number);
    return denominator / (numerator + denominator);
  }

  /**
   * Remove vig from implied probabilities
   * @param {Array<number>} probabilities - Raw implied probabilities
   * @returns {Array<number>} Vig-adjusted probabilities
   */
  static removeVig(probabilities) {
    const total = probabilities.reduce((sum, p) => sum + p, 0);
    return probabilities.map(p => p / total);
  }

  /**
   * Calculate hold percentage from odds
   * @param {Array<number>} probabilities - Implied probabilities
   * @returns {number} Hold percentage
   */
  static calculateHold(probabilities) {
    const total = probabilities.reduce((sum, p) => sum + p, 0);
    return (total - 1) * 100;
  }
}

module.exports = { SportsbookClient };
