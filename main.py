#!/usr/bin/env python3
"""
Finnhub & Alpha Vantage API Comparison Tool
Demonstrates both APIs working together for stock comparison
"""

import time
from config import config
from alphavantage import AlphaVantageClient
from finnhub import FinnhubClient


def check_api_configuration():
    """Check if API keys are properly configured"""
    print("🔐 Checking API Configuration...")
    print("=" * 60)
    
    if not config.is_configured():
        print("❌ API keys not properly configured!")
        print("\n🔧 Please run the setup:")
        print("   1. python setup_env.py")
        print("   2. Edit .env file with your actual API keys")
        print("   3. Restart this program")
        print("\n📋 You can also check status with:")
        print("   python -c \"from config import config; config.display_config_status()\"")
        return False
    
    config.display_config_status()
    print("✅ All API keys configured successfully!")
    return True


def compare_stock_data(symbol="AAPL"):
    """
    Compare stock data from both Alpha Vantage and Finnhub APIs
    
    Args:
        symbol (str): Stock symbol to compare
    """
    print(f"\n🔍 Comparing {symbol} data from both APIs:")
    print("=" * 60)
    
    try:
        # Initialize clients
        alpha_client = AlphaVantageClient()
        finnhub_client = FinnhubClient()
        
        print("📊 Fetching data...")
        
        # Get Alpha Vantage data
        print("📈 Getting Alpha Vantage quote...")
        alpha_data = alpha_client.get_quote(symbol)
        
        # Get Finnhub data  
        print("📊 Getting Finnhub quote...")
        finnhub_data = finnhub_client.get_quote(symbol)
        
        # Rate limiting pause
        time.sleep(1)
        
        # Display results
        print("\n" + "=" * 60)
        print("📊 RESULTS COMPARISON")
        print("=" * 60)
        
        if alpha_data and 'Global Quote' in alpha_data:
            quote = alpha_data['Global Quote']
            alpha_price = float(quote['05. price'])
            alpha_change = float(quote['09. change'])
            alpha_change_percent = quote['10. change percent'].rstrip('%')
            
            print(f"\n📈 Alpha Vantage Data:")
            print(f"  Price: ${alpha_price:.2f}")
            print(f"  Change: {alpha_change:+.2f} ({alpha_change_percent}%)")
        else:
            print("\n❌ Alpha Vantage data not available")
            alpha_price = None
        
        if finnhub_data and 'c' in finnhub_data:
            finnhub_price = finnhub_data['c']
            finnhub_change = finnhub_data['d'] 
            finnhub_change_percent = finnhub_data['dp']
            
            print(f"\n📊 Finnhub Data:")
            print(f"  Price: ${finnhub_price:.2f}")
            print(f"  Change: {finnhub_change:+.2f} ({finnhub_change_percent:+.2f}%)")
        else:
            print("\n❌ Finnhub data not available")
            finnhub_price = None
        
        # Compare prices if both available
        if alpha_price and finnhub_price:
            price_diff = abs(alpha_price - finnhub_price)
            print(f"\n💡 Price Difference: ${price_diff:.2f}")
            
            if price_diff < 0.50:
                print("  ✅ Prices are very close (difference < $0.50)")
            elif price_diff < 2.00:
                print("  ⚠️ Prices have moderate difference")
            else:
                print("  🔍 Prices have significant difference - may be from different times")
                
    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("\n🔧 Please configure your API keys:")
        print("   1. Run: python setup_env.py")
        print("   2. Edit .env with your keys")
        print("   3. Restart this program")
    except Exception as e:
        print(f"\n❌ Error during comparison: {e}")


def demonstrate_additional_features():
    """Demonstrate additional features from both APIs"""
    print("\n🚀 Additional Features Demonstration")
    print("=" * 60)
    
    try:
        alpha_client = AlphaVantageClient()
        finnhub_client = FinnhubClient()
        
        # Alpha Vantage: Company overview
        print("\n📋 Company Overview (Alpha Vantage):")
        overview = alpha_client.get_company_overview("AAPL")
        if overview:
            print(f"  Company: {overview.get('Name', 'N/A')}")
            print(f"  Sector: {overview.get('Sector', 'N/A')}")
            print(f"  Market Cap: ${overview.get('MarketCapitalization', 'N/A')}")
        
        time.sleep(1)  # Rate limiting
        
        # Finnhub: Company profile
        print("\n🏢 Company Profile (Finnhub):")
        profile = finnhub_client.get_company_profile("AAPL")
        if profile:
            print(f"  Company: {profile.get('name', 'N/A')}")
            print(f"  Industry: {profile.get('finnhubIndustry', 'N/A')}")
            print(f"  Market Cap: ${profile.get('marketCapitalization', 'N/A')}M")
            
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
    except Exception as e:
        print(f"❌ Error in demonstration: {e}")


def main():
    """Main program function"""
    print("🚀 Finnhub & Alpha Vantage API Comparison Tool")
    print("=" * 70)
    
    # Check API configuration first
    if not check_api_configuration():
        return
    
    print("\n⏳ Starting API comparison...")
    
    # Compare stock data
    compare_stock_data("AAPL")
    
    # Demonstrate additional features
    demonstrate_additional_features()
    
    print("\n✅ Comparison completed!")
    print("\n💡 Tips:")
    print("   - Both APIs provide reliable real-time data")
    print("   - Alpha Vantage: Better for technical analysis")
    print("   - Finnhub: Better for news and fundamental data")
    print("   - Consider API rate limits for production use")


if __name__ == "__main__":
    main() 