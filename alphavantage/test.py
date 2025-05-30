"""
Alpha Vantage API Connection Test
Quick test script to verify API connectivity and response
"""

import sys
import os
# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from alphavantage.client import AlphaVantageClient
import json


def test_api_connection():
    """Test basic API connection and functionality"""
    print("🧪 Testing Alpha Vantage API connection...")
    print("=" * 50)
    
    # Initialize client
    try:
        client = AlphaVantageClient()
        print("✅ Client initialization successful")
    except Exception as e:
        print(f"❌ Client initialization failed: {e}")
        return False
    
    # Test 1: Simple quote request
    print("\n📊 Test 1: Get AAPL stock quote...")
    try:
        quote_data = client.get_quote("AAPL")
        if quote_data and 'Global Quote' in quote_data:
            quote = quote_data['Global Quote']
            symbol = quote.get('01. symbol', 'N/A')
            price = quote.get('05. price', 'N/A')
            print(f"✅ Successfully retrieved {symbol} quote: ${price}")
            return True
        else:
            print("❌ Failed to get valid quote data")
            if quote_data:
                print(f"   Response data: {list(quote_data.keys())}")
            return False
    except Exception as e:
        print(f"❌ Quote request failed: {e}")
        return False


def test_search_functionality():
    """Test symbol search functionality"""
    print("\n🔍 Test 2: Search functionality test...")
    try:
        client = AlphaVantageClient()
        search_results = client.search_symbol("Apple")
        
        if search_results and 'bestMatches' in search_results:
            matches = search_results['bestMatches']
            if matches:
                first_match = matches[0]
                symbol = first_match.get('1. symbol', 'N/A')
                name = first_match.get('2. name', 'N/A')
                print(f"✅ Search successful, found: {symbol} - {name}")
                return True
            else:
                print("❌ Search results are empty")
                return False
        else:
            print("❌ Search request failed")
            if search_results:
                print(f"   Response data: {list(search_results.keys())}")
            return False
    except Exception as e:
        print(f"❌ Search request exception: {e}")
        return False


def main():
    """Main test function"""
    print("🚀 Alpha Vantage API Connection Test")
    print("=" * 50)
    
    # Test basic connection
    connection_ok = test_api_connection()
    
    if connection_ok:
        print("\n✅ Basic connection test passed!")
        
        # Test additional functionality
        search_ok = test_search_functionality()
        
        if search_ok:
            print("\n🎉 All tests passed!")
            print("\n💡 Tip: Now you can run the full example program:")
            print("   python alphavantage/example.py")
        else:
            print("\n⚠️  Basic connection is OK, but search functionality test failed")
    else:
        print("\n❌ Basic connection test failed")
        print("\n🔧 Possible issues:")
        print("   1. Check if API key is correct")
        print("   2. Check network connection")
        print("   3. Confirm API call limits haven't been reached")
    
    print("\n" + "=" * 50)


if __name__ == "__main__":
    main() 