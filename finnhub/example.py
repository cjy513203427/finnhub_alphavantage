"""
Finnhub API Example Usage
Demonstrates various API calls and data retrieval
"""

from finnhub.client import FinnhubClient
import time
from datetime import datetime, timedelta
import json


def main():
    """Main function demonstrating Finnhub API usage"""
    
    # Initialize client
    client = FinnhubClient()
    
    print("🚀 Finnhub API Example Program")
    print("=" * 60)
    
    # Example 1: Get real-time quotes for popular stocks
    print("\n📈 1. Get real-time quotes for popular stocks:")
    symbols = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]
    
    for symbol in symbols:
        quote = client.get_quote(symbol)
        if quote and 'c' in quote:
            price = quote['c']
            change = quote.get('d', 0)
            change_percent = quote.get('dp', 0)
            print(f"  {symbol}: ${price:.2f} ({change:+.2f}, {change_percent:+.2f}%)")
        else:
            print(f"  {symbol}: Failed to get data")
        time.sleep(0.1)  # Rate limiting
    
    # Example 2: Get detailed company information
    print("\n🏢 2. Get detailed company information (Apple):")
    profile = client.get_company_profile("AAPL")
    if profile:
        print(f"  Company Name: {profile.get('name', 'N/A')}")
        print(f"  Industry: {profile.get('finnhubIndustry', 'N/A')}")
        print(f"  Country: {profile.get('country', 'N/A')}")
        print(f"  Market Cap: ${profile.get('marketCapitalization', 'N/A')}M")
        print(f"  Employee Count: {profile.get('employeeTotal', 'N/A')}")
        print(f"  Website: {profile.get('weburl', 'N/A')}")
    else:
        print("  Failed to get company information")
    
    # Example 3: Get recent market news
    print("\n📰 3. Get latest market news:")
    news = client.get_market_news()
    if news and len(news) > 0:
        for i, article in enumerate(news[:5]):  # Show first 5 articles
            headline = article.get('headline', 'No headline')
            source = article.get('source', 'Unknown')
            # Convert timestamp to readable date
            timestamp = article.get('datetime', 0)
            if timestamp:
                date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')
            else:
                date = 'Unknown date'
            print(f"  {i+1}. [{source}] {headline}")
            print(f"     Published: {date}")
            print()
    else:
        print("  Failed to get news")
    
    # Example 4: Get company-specific news
    print("\n📊 4. Get company-specific news (Tesla):")
    # Get news from last 7 days
    to_date = datetime.now().strftime('%Y-%m-%d')
    from_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    
    company_news = client.get_company_news("TSLA", from_date, to_date)
    if company_news and len(company_news) > 0:
        for i, article in enumerate(company_news[:3]):  # Show first 3 articles
            headline = article.get('headline', 'No headline')
            source = article.get('source', 'Unknown')
            print(f"  {i+1}. [{source}] {headline}")
    else:
        print("  Failed to get Tesla news")
    
    # Example 5: Get recommendation trends
    print("\n🎯 5. Get analyst recommendations (Apple):")
    recommendations = client.get_recommendation_trends("AAPL")
    if recommendations and len(recommendations) > 0:
        latest = recommendations[0]  # Most recent recommendation
        print(f"  Strong Buy: {latest.get('strongBuy', 0)}")
        print(f"  Buy: {latest.get('buy', 0)}")
        print(f"  Hold: {latest.get('hold', 0)}")
        print(f"  Sell: {latest.get('sell', 0)}")
        print(f"  Strong Sell: {latest.get('strongSell', 0)}")
    else:
        print("  Failed to get recommendation data")
    
    # Example 6: Get price target
    print("\n💰 6. Get price targets (Apple):")
    price_target = client.get_price_target("AAPL")
    if price_target:
        print(f"  Target Median: ${price_target.get('targetMedian', 'N/A')}")
        print(f"  Target Mean: ${price_target.get('targetMean', 'N/A')}")
        print(f"  Target High: ${price_target.get('targetHigh', 'N/A')}")
        print(f"  Target Low: ${price_target.get('targetLow', 'N/A')}")
    else:
        print("  Failed to get price target")
    
    print("\n" + "=" * 60)
    print("✅ Finnhub example program completed!")


def get_stock_data_detailed(symbol: str):
    """Get comprehensive stock data for a specific symbol"""
    client = FinnhubClient()
    
    print(f"\n📊 Get detailed data for {symbol}:")
    print("-" * 40)
    
    # Get quote
    quote = client.get_quote(symbol)
    if quote and 'c' in quote:
        print(f"Current Price: ${quote['c']:.2f}")
        print(f"Open Price: ${quote.get('o', 'N/A')}")
        print(f"High Price: ${quote.get('h', 'N/A')}")
        print(f"Low Price: ${quote.get('l', 'N/A')}")
        print(f"Previous Close: ${quote.get('pc', 'N/A')}")
        print(f"Change: ${quote.get('d', 'N/A')} ({quote.get('dp', 'N/A')}%)")
    
    # Get company profile
    profile = client.get_company_profile(symbol)
    if profile:
        print(f"\nCompany Information:")
        print(f"  Name: {profile.get('name', 'N/A')}")
        print(f"  Industry: {profile.get('finnhubIndustry', 'N/A')}")
        print(f"  Market Cap: ${profile.get('marketCapitalization', 'N/A')}M")
    
    return {"quote": quote, "profile": profile}


if __name__ == "__main__":
    # Run main example
    main()
    
    # Get detailed data for a specific stock
    print("\n" + "=" * 60)
    get_stock_data_detailed("NVDA") 