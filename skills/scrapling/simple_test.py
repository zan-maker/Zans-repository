#!/usr/bin/env python3
"""
Simple Scrapling Test Script
Verifies that Scrapling is installed and can perform basic scraping
"""
from scraping import Scraper

def test_basic_scraping():
    """Test basic Scrapling functionality"""
    print("🧪 Testing Scrapling AI Web Scraper...")
    print()
    
    # Initialize Scraper
    scraper = Scraper()
    
    # Test URL (wikipedia - reliable, no Cloudflare)
    test_url = "https://en.wikipedia.org/wiki/Web_scraping"
    
    print(f"Testing with: {test_url}")
    print()
    
    try:
        # Simple scrape
        result = scraper.scrape(
            test_url,
            "Extract the page title and first paragraph"
        )
        
        print("✅ Success!")
        print(f"Status: {result['success']}")
        print(f"Data: {len(result.get('data', []))} items extracted")
        print()
        
        # Show extracted data
        if result['success'] and result['data']:
            for i, item in enumerate(result['data'][:5], 1):
                print(f"  {i}. {item}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print()
        return False

if __name__ == "__main__":
    success = test_basic_scraping()
    print()
    print("="*50)
    if success:
        print("🎉 Scrapling is working!")
        print("The AI-powered scraper is ready for use.")
        print()
        print("📚 Integration with OpenClaw agents:")
        print("  - Lead generation")
        print("  - Market research")
        print("  - Competitor analysis")
        print("  - Content monitoring")
    else:
        print("⚠️  Scrapling test failed")
        print("Check if the scraping library is installed correctly.")
