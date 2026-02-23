"""
Kalshi API Connector with RSA Authentication
Production-grade connector for Kalshi trading API
"""
import urllib.request
import json
import base64
import hashlib
from datetime import datetime, timezone
from typing import Dict, List, Optional
from dataclasses import dataclass

# Kalshi API Configuration
KALSHI_API_BASE = "https://api.elections.kalshi.com/trade-api/v2"

# API Credentials
API_KEY_ID = "a23a4240-8abd-47b4-900e-072226c47489"
PRIVATE_KEY_PEM = """-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEA0teO+CI/M0dEHMrcJaRX5f75K+IxiE4+mWUKWcXoiXEHH09Z
SgWrjHPLy/lyPqpMQ251ydwFdWSK5KEmH54QIP+mV+VTUMuy3Ip8QONcaM2U1dqw
jtsOtgp+LWxZXX+sqSl32SWPZz1+e5BVuH/MVBdfyERUZo6KOaX0QdCJilMjOISP
j7w9sEL8oA5oydbtI2dUi2+E1bh+jgun4Mn5H6IAx7+VzSGdprpX9rxAcnrXoL8P
GIEeyKgF+JLiXhSvzfbRdf3qnvuhS/zUh01CaKfGXX9if/Gfgdf3fSnmqO2sLtiL
OJFXxScNEeF7xRS5AZIfI1Ea+CPf1GGdOBb0tQIDAQABAoIBAErXJzGe/m4WSvAp
dfGKn4TNd+cC2HA4zfGnMwBgxsUasNuFT/19e8JUTC/wMIRb8Mwyxm7LwchE0ySK
qzyn37PG62Xhyiww0iGEqsxhqCivaLhscyWSTmuB1/4JqsMMkd5OEPOsaHXOFzqH
JlZiTsY+scolrwvkZt5FsSk3e8r0SM2JbxP2G+sxUfMGI+2HzMwXviGsGPBVC1Sx
yq5WMoSIu+d7dSSR7jZYaIHsVklLDu6dUSQaPM+edSzFG8JeZVOLC+AFDuqatSQF
fgRWPcPynDF7FKaTuudtx8otv0cp7NRBXzWzqqUKS3wQCs32x+mV0lVaUo/dncuI
DeSUYzUCgYEA3/x5uM5sM57WqxA+6XBJ5dvLO7pTu1NnretF8xQu6T3z83cUnbtV
ilaF4MXPOIckN/f8tm5ZoDjGFYnu6QzZZWeMhOi1pPMjIkgDo0H1FSOtqP5Jm75S
K4uNU1C1ps+gebQyrn8G/ehVS0tkSVNIQMWR573TmpxxPuJCBqH0fSMCgYEA8Pok
6bvUjtt0NRP8XR49NV5AU73szUHDTK67ogYjm9R7jA195fd2XO5YYA5I/ns94gJx
pCxxzzSQPkmHpzqPd9mHviQAhdqTSoEqcAgwZOJ1rw+RF1MkvEKzMY+qaLW7geLk
axGGCI2FWKIrBvRLumxKvY01qhBFMRJHziy6wEcCgYBBSde1Lb5OYatTG54q70cr
ECEyXMKRZONgx6aRDz4JULyuJ/TDcVqiw0us1Bvt7z54bfmkt4+6azIaDyWrmso3
i7Ji/24LEbAZCwK8cLpemhLBorWUByrudHQSaAE7CWROdV8ci/xewH00QFqQIQ17
i9tWwHdQpu8/lDYItuaMHwKBgQC7rQXMp8W+0PmrUPpuB1wCUXpl/fgMT9hrw3ZM
lN1swsrJ48QWs2kSrWpUvStqTs9+UwrwotCsYLKqYBfvTPNpkxheJKnnlbi7AOft
QuN13s1q3wPQF6f3mzb2NX6xeEAlw3DEVmx+AsJEqmA6VU8ZTLfU8sJFxdAtjKAx
2bJEhwKBgDDo1BrYw+1M1RZmZ1cz6NB8PeyA57wu+ueKLNVlZsMaplr4wBkzBf37
+mEunzeusCY5vl4gacN0eI6efbGJVjL394G4x3oamw9pTjpEaoYbwhdLSCHvm0l6
ulBhbCnDt1+BKimy0e49pAM3QW5amWiJpMrxauWSE8WQaGnBErva
-----END RSA PRIVATE KEY-----"""


class KalshiAuth:
    """Handles RSA key authentication for Kalshi API"""
    
    def __init__(self, api_key_id: str, private_key_pem: str):
        self.api_key_id = api_key_id
        self.private_key_pem = private_key_pem
        self.private_key = self._load_private_key()
    
    def _load_private_key(self):
        """Load RSA private key from PEM"""
        try:
            from cryptography.hazmat.primitives import serialization
            from cryptography.hazmat.backends import default_backend
            
            private_key = serialization.load_pem_private_key(
                self.private_key_pem.encode(),
                password=None,
                backend=default_backend()
            )
            return private_key
        except ImportError:
            print("⚠️  cryptography library not installed, using simplified auth")
            return None
    
    def create_signature(self, timestamp: str, method: str, path: str) -> str:
        """Create RSA signature for request"""
        if self.private_key is None:
            # Fallback - return empty signature
            return ""
        
        try:
            from cryptography.hazmat.primitives import hashes
            from cryptography.hazmat.primitives.asymmetric import padding
            
            # Create message to sign
            message = f"{timestamp}{method}{path}"
            message_bytes = message.encode('utf-8')
            
            # Sign with RSA
            signature = self.private_key.sign(
                message_bytes,
                padding.PKCS1v15(),
                hashes.SHA256()
            )
            
            # Base64 encode
            return base64.b64encode(signature).decode('utf-8')
        except Exception as e:
            print(f"⚠️  Signature creation failed: {e}")
            return ""


class KalshiClient:
    """
    Kalshi Trading API Client with RSA Authentication
    """
    
    def __init__(self):
        self.auth = KalshiAuth(API_KEY_ID, PRIVATE_KEY_PEM)
        self.base_url = KALSHI_API_BASE
    
    def _get_headers(self, method: str, path: str) -> Dict:
        """Get authenticated headers for request"""
        timestamp = str(int(datetime.now(timezone.utc).timestamp()))
        signature = self.auth.create_signature(timestamp, method, path)
        
        headers = {
            "Content-Type": "application/json"
        }
        
        # Add auth headers if signature available
        if signature:
            headers["KALSHI-ACCESS-KEY"] = API_KEY_ID
            headers["KALSHI-ACCESS-TIMESTAMP"] = timestamp
            headers["KALSHI-ACCESS-SIGNATURE"] = signature
        
        return headers
    
    def _make_request(self, method: str, path: str, data: Dict = None) -> Dict:
        """Make authenticated HTTP request"""
        url = f"{self.base_url}{path}"
        headers = self._get_headers(method, path)
        
        try:
            if method == "GET":
                req = urllib.request.Request(url, headers=headers)
            else:
                req = urllib.request.Request(
                    url,
                    data=json.dumps(data).encode() if data else None,
                    headers=headers,
                    method=method
                )
            
            with urllib.request.urlopen(req, timeout=30) as response:
                return json.loads(response.read().decode('utf-8'))
                
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            
            # Check if it's an auth issue
            if e.code == 401:
                raise Exception(f"Authentication failed (401): {error_body}")
            elif e.code == 403:
                raise Exception(f"Forbidden (403): {error_body}")
            else:
                raise Exception(f"HTTP {e.code}: {error_body}")
                
        except Exception as e:
            raise Exception(f"Request failed: {e}")
    
    def get_markets(
        self, 
        status: str = "open",
        category: str = None,
        limit: int = 100
    ) -> List[Dict]:
        """
        Get available markets
        """
        path = f"/markets?status={status}&limit={limit}"
        if category:
            path += f"&category={category}"
        
        result = self._make_request("GET", path)
        return result.get("markets", [])
    
    def get_market(self, ticker: str) -> Dict:
        """Get specific market details"""
        path = f"/markets/{ticker}"
        return self._make_request("GET", path)
    
    def get_orderbook(self, ticker: str) -> Dict:
        """Get orderbook for a market"""
        path = f"/markets/{ticker}/orderbook"
        return self._make_request("GET", path)
    
    def get_series(self, series_ticker: str) -> Dict:
        """Get series information"""
        path = f"/series/{series_ticker}"
        return self._make_request("GET", path)
    
    def get_sports_markets(self, league: str = None) -> List[Dict]:
        """
        Get sports markets specifically
        """
        markets = self.get_markets(category="sports", limit=1000)
        
        if league:
            markets = [m for m in markets if league.upper() in m.get("ticker", "")]
        
        return markets
    
    def get_balance(self) -> Dict:
        """Get account balance"""
        path = "/portfolio/balance"
        return self._make_request("GET", path)
    
    def parse_sports_market(self, market: Dict) -> Dict:
        """Parse a sports market to extract structured info"""
        ticker = market.get("ticker", "")
        parts = ticker.split("-")
        
        result = {
            "ticker": ticker,
            "title": market.get("title", ""),
            "yes_price": market.get("yes_ask", 0) / 100 if market.get("yes_ask") else None,
            "yes_bid": market.get("yes_bid", 0) / 100 if market.get("yes_bid") else None,
            "no_price": market.get("no_ask", 0) / 100 if market.get("no_ask") else None,
            "no_bid": market.get("no_bid", 0) / 100 if market.get("no_bid") else None,
            "volume": market.get("volume", 0),
            "open_time": market.get("open_time"),
            "close_time": market.get("close_time"),
            "status": market.get("status"),
            "last_price": market.get("last_price", 0) / 100 if market.get("last_price") else None
        }
        
        # Try to extract league, date, teams from ticker
        if len(parts) >= 2:
            result["league"] = parts[0]
        if len(parts) >= 4:
            try:
                result["date"] = f"{parts[1]}-{parts[2]}-{parts[3]}"
            except:
                pass
        
        return result


if __name__ == "__main__":
    # Test Kalshi connection
    print("Testing Kalshi API with RSA Authentication...")
    print("=" * 70)
    
    client = KalshiClient()
    
    try:
        # Get account balance (tests auth)
        print("\n1. Testing authentication...")
        balance = client.get_balance()
        print(f"✓ Authenticated! Balance: ${balance.get('balance', 0)/100:.2f}")
        
    except Exception as e:
        print(f"✗ Auth failed: {e}")
        print("\nTrying without auth (read-only markets)...")
    
    # Get sports markets
    print("\n2. Fetching sports markets...")
    try:
        sports_markets = client.get_sports_markets()
        print(f"✓ Found {len(sports_markets)} sports markets")
        
        # Show sample markets
        if sports_markets:
            print("\nSample markets:")
            for market in sports_markets[:5]:
                parsed = client.parse_sports_market(market)
                print(f"\n  {parsed['ticker']}")
                print(f"    Title: {parsed['title'][:60]}...")
                if parsed.get('yes_price'):
                    print(f"    Yes: ${parsed['yes_price']:.2f}")
                if parsed.get('no_price'):
                    print(f"    No:  ${parsed['no_price']:.2f}")
                print(f"    Volume: {parsed['volume']:,}")
        
        # Get NBA-specific markets
        print("\n" + "=" * 70)
        print("3. Fetching NBA markets...")
        nba_markets = client.get_sports_markets(league="NBA")
        print(f"✓ Found {len(nba_markets)} NBA markets")
        
    except Exception as e:
        print(f"✗ Error: {e}")
