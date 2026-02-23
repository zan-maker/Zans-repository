"""
RapidAPI Sportsbook API Discovery
Tests various sportsbook APIs to find what's available with the key
"""
import urllib.request
import json

RAPIDAPI_KEY = "c4c3e4c57bmshc1a4bd30b0c8bd4p1c4595jsncab6793d5df8"

# Common sportsbook APIs on RapidAPI
APIS_TO_TEST = [
    {
        "name": "The Odds API",
        "host": "odds.p.rapidapi.com",
        "test_endpoint": "https://odds.p.rapidapi.com/v4/sports"
    },
    {
        "name": "Live Sports Odds",
        "host": "live-sports-odds.p.rapidapi.com",
        "test_endpoint": "https://live-sports-odds.p.rapidapi.com/sports"
    },
    {
        "name": "API-Basketball",
        "host": "api-basketball.p.rapidapi.com",
        "test_endpoint": "https://api-basketball.p.rapidapi.com/timezone"
    },
    {
        "name": "API-Football",
        "host": "api-football-v1.p.rapidapi.com",
        "test_endpoint": "https://api-football-v1.p.rapidapi.com/v3/timezone"
    },
    {
        "name": "API-NBA",
        "host": "api-nba-v1.p.rapidapi.com",
        "test_endpoint": "https://api-nba-v1.p.rapidapi.com/timezone"
    },
    {
        "name": "American Football Events",
        "host": "americanfootballapi.p.rapidapi.com",
        "test_endpoint": "https://americanfootballapi.p.rapidapi.com/api/american-football/tournaments"
    },
    {
        "name": "Sports Data",
        "host": "sportspage-feeds.p.rapidapi.com",
        "test_endpoint": "https://sportspage-feeds.p.rapidapi.com/events"
    },
    {
        "name": "Live Sports Data",
        "host": "livesports6.p.rapidapi.com",
        "test_endpoint": "https://livesports6.p.rapidapi.com/sports"
    },
    {
        "name": "Sports Info",
        "host": "sportscore1.p.rapidapi.com",
        "test_endpoint": "https://sportscore1.p.rapidapi.com/sports"
    }
]

def test_api(api_info):
    """Test if API is accessible"""
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": api_info["host"]
    }
    
    req = urllib.request.Request(api_info["test_endpoint"], headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            return {
                "status": "✓ WORKING",
                "data_sample": str(data)[:200] if data else "Empty response"
            }
    except urllib.error.HTTPError as e:
        error_msg = e.read().decode('utf-8')
        if "not subscribed" in error_msg.lower():
            return {"status": "✗ NOT SUBSCRIBED", "error": error_msg[:100]}
        elif e.code == 401:
            return {"status": "✗ AUTH FAILED", "error": error_msg[:100]}
        else:
            return {"status": f"✗ HTTP {e.code}", "error": error_msg[:100]}
    except Exception as e:
        return {"status": "✗ ERROR", "error": str(e)[:100]}

if __name__ == "__main__":
    print("Testing RapidAPI Sportsbook APIs...")
    print("=" * 60)
    print(f"API Key: {RAPIDAPI_KEY[:10]}...{RAPIDAPI_KEY[-6:]}")
    print("=" * 60)
    
    working_apis = []
    
    for api in APIS_TO_TEST:
        print(f"\n{api['name']}:")
        result = test_api(api)
        print(f"  Status: {result['status']}")
        
        if "WORKING" in result['status']:
            working_apis.append(api)
            print(f"  Sample: {result.get('data_sample', 'N/A')}")
        else:
            print(f"  Error: {result.get('error', 'Unknown')}")
    
    print("\n" + "=" * 60)
    print(f"SUMMARY: {len(working_apis)} working APIs")
    if working_apis:
        print("\nWorking APIs:")
        for api in working_apis:
            print(f"  - {api['name']}")
    else:
        print("\nNo working sportsbook APIs found.")
        print("\nNext steps:")
        print("1. Go to https://rapidapi.com/hub")
        print("2. Search for 'odds' or 'sportsbook'")
        print("3. Subscribe to free tier of available APIs")
        print("4. Update this script with working API details")
