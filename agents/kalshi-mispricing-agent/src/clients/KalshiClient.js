/**
 * KalshiClient - Authenticated REST API client for Kalshi
 * Handles RSA-signed requests, rate limiting, and API interactions
 */

const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

class KalshiClient {
  constructor(config = {}) {
    this.baseUrl = config.baseUrl || 'https://trading-api.kalshi.com/v1';
    this.apiKeyId = config.apiKeyId || process.env.KALSHI_API_KEY_ID;
    this.privateKeyPath = config.privateKeyPath || process.env.KALSHI_PRIVATE_KEY_PATH;
    this.privateKey = null;
    this.lastRequestTime = 0;
    this.minRequestInterval = 100; // 100ms between requests
    
    if (this.privateKeyPath && fs.existsSync(this.privateKeyPath)) {
      this.privateKey = fs.readFileSync(this.privateKeyPath, 'utf8');
    }
  }

  /**
   * Generate RSA signature for Kalshi authentication
   */
  _signRequest(timestamp, method, path, body = '') {
    if (!this.privateKey) {
      throw new Error('Private key not loaded');
    }
    
    const message = `${timestamp}${method.toUpperCase()}${path}${body}`;
    const signer = crypto.createSign('RSA-SHA256');
    signer.update(message);
    return signer.sign(this.privateKey, 'base64');
  }

  /**
   * Make authenticated request to Kalshi API
   */
  async _request(method, path, data = null) {
    // Rate limiting
    const now = Date.now();
    const timeSinceLastRequest = now - this.lastRequestTime;
    if (timeSinceLastRequest < this.minRequestInterval) {
      await new Promise(resolve => setTimeout(resolve, this.minRequestInterval - timeSinceLastRequest));
    }
    this.lastRequestTime = Date.now();

    const timestamp = Math.floor(Date.now() / 1000).toString();
    const body = data ? JSON.stringify(data) : '';
    const signature = this._signRequest(timestamp, method, path, body);

    const url = `${this.baseUrl}${path}`;
    const headers = {
      'KALSHI-ACCESS-KEY': this.apiKeyId,
      'KALSHI-ACCESS-TIMESTAMP': timestamp,
      'KALSHI-ACCESS-SIGNATURE': signature,
      'Content-Type': 'application/json'
    };

    try {
      const response = await fetch(url, {
        method,
        headers,
        body: data ? body : undefined
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Kalshi API error: ${response.status} ${errorText}`);
      }

      return await response.json();
    } catch (error) {
      console.error(`Kalshi API request failed: ${method} ${path}`, error);
      throw error;
    }
  }

  // ==================== MARKET DATA ====================

  /**
   * Get all active events
   */
  async getEvents(status = 'active', cursor = null) {
    let path = `/events?status=${status}`;
    if (cursor) path += `&cursor=${cursor}`;
    return this._request('GET', path);
  }

  /**
   * Get specific event details
   */
  async getEvent(eventId) {
    return this._request('GET', `/events/${eventId}`);
  }

  /**
   * Get markets for an event
   */
  async getMarkets(eventId) {
    return this._request('GET', `/events/${eventId}/markets`);
  }

  /**
   * Get specific market details
   */
  async getMarket(marketId) {
    return this._request('GET', `/markets/${marketId}`);
  }

  /**
   * Get market order book
   */
  async getOrderBook(marketId) {
    return this._request('GET', `/markets/${marketId}/orderbook`);
  }

  /**
   * Get series information
   */
  async getSeries(seriesId) {
    return this._request('GET', `/series/${seriesId}`);
  }

  // ==================== TRADING ====================

  /**
   * Place an order
   */
  async placeOrder(marketId, side, count, price) {
    const data = {
      market_id: marketId,
      side: side, // 'yes' or 'no'
      count: count,
      price: price // In cents (e.g., 4500 = 45.00¢)
    };
    return this._request('POST', '/orders', data);
  }

  /**
   * Cancel an order
   */
  async cancelOrder(orderId) {
    return this._request('DELETE', `/orders/${orderId}`);
  }

  /**
   * Get order status
   */
  async getOrder(orderId) {
    return this._request('GET', `/orders/${orderId}`);
  }

  /**
   * Get all open orders
   */
  async getOpenOrders() {
    return this._request('GET', '/orders?status=open');
  }

  // ==================== PORTFOLIO ====================

  /**
   * Get current positions
   */
  async getPositions() {
    return this._request('GET', '/portfolio/positions');
  }

  /**
   * Get balance
   */
  async getBalance() {
    return this._request('GET', '/portfolio/balance');
  }

  /**
   * Get settlement history
   */
  async getSettlements() {
    return this._request('GET', '/portfolio/settlements');
  }

  // ==================== UTILITY ====================

  /**
   * Convert probability to Kalshi price (cents)
   * Example: 0.65 probability → 6500 (65.00¢)
   */
  static probabilityToPrice(probability) {
    return Math.round(probability * 10000);
  }

  /**
   * Convert Kalshi price to probability
   * Example: 6500 → 0.65
   */
  static priceToProbability(price) {
    return price / 10000;
  }

  /**
   * Calculate implied probability from Kalshi order book
   * Uses best bid/ask midpoint
   */
  static getImpliedProbabilityFromOrderBook(orderBook) {
    if (!orderBook || !orderBook.yes || !orderBook.no) return null;
    
    const bestYesBid = orderBook.yes.bids?.[0]?.price || 0;
    const bestYesAsk = orderBook.yes.asks?.[0]?.price || 10000;
    
    const bestNoBid = orderBook.no.bids?.[0]?.price || 0;
    const bestNoAsk = orderBook.no.asks?.[0]?.price || 10000;
    
    // Midpoint for yes
    const yesMid = (bestYesBid + bestYesAsk) / 2;
    const yesProb = yesMid / 10000;
    
    // Midpoint for no
    const noMid = (bestNoBid + bestNoAsk) / 2;
    const noProb = noMid / 10000;
    
    // Normalize (yes + no should = 1)
    const total = yesProb + noProb;
    return {
      yes: yesProb / total,
      no: noProb / total
    };
  }
}

module.exports = { KalshiClient };
