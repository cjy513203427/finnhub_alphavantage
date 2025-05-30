"""
Alpha Vantage API Quick Demo
A condensed version with key features to avoid rate limiting
"""

from alphavantage.client import AlphaVantageClient
import time


def quick_demo():
    """Quick demonstration of Alpha Vantage API key features"""
    
    client = AlphaVantageClient()
    
    print("🚀 Alpha Vantage API Quick Demo")
    print("=" * 50)
    
    # Demo 1: Real-time quote
    print("\n📈 Get real-time quote (Apple):")
    quote_data = client.get_quote("AAPL")
    if quote_data and 'Global Quote' in quote_data:
        quote = quote_data['Global Quote']
        symbol = quote.get('01. symbol', 'N/A')
        price = float(quote.get('05. price', 0))
        change = float(quote.get('09. change', 0))
        change_percent = quote.get('10. change percent', '0%')
        volume = quote.get('06. volume', 'N/A')
        
        print(f"  Symbol: {symbol}")
        print(f"  Current Price: ${price:.2f}")
        print(f"  Change: {change:+.2f} ({change_percent})")
        print(f"  Volume: {volume}")
    else:
        print("  Failed to get quote")
    
    print("\n⏳ Waiting 12 seconds to avoid API limit...")
    time.sleep(12)
    
    # Demo 2: Symbol search
    print("\n🔍 Search stock symbols (keyword: Tesla):")
    search_results = client.search_symbol("Tesla")
    if search_results and 'bestMatches' in search_results:
        matches = search_results['bestMatches'][:3]  # Show top 3
        for i, match in enumerate(matches):
            symbol = match.get('1. symbol', 'N/A')
            name = match.get('2. name', 'N/A')
            match_score = match.get('9. matchScore', 'N/A')
            print(f"  {i+1}. {symbol} - {name} (match score: {match_score})")
    else:
        print("  Search failed")
    
    print("\n⏳ Waiting 12 seconds to avoid API limit...")
    time.sleep(12)
    
    # Demo 3: Company overview
    print("\n🏢 Get company overview (Microsoft):")
    overview = client.get_company_overview("MSFT")
    if overview:
        print(f"  Company Name: {overview.get('Name', 'N/A')}")
        print(f"  Industry: {overview.get('Industry', 'N/A')}")
        print(f"  Sector: {overview.get('Sector', 'N/A')}")
        print(f"  Market Cap: ${overview.get('MarketCapitalization', 'N/A')}")
        print(f"  P/E Ratio: {overview.get('PERatio', 'N/A')}")
        print(f"  52 Week High: ${overview.get('52WeekHigh', 'N/A')}")
        print(f"  52 Week Low: ${overview.get('52WeekLow', 'N/A')}")
        print(f"  Employees: {overview.get('FullTimeEmployees', 'N/A')}")
    else:
        print("  Failed to get company information")
    
    print("\n" + "=" * 50)
    print("✅ Quick demo completed!")
    print("\n💡 Tips:")
    print("- This demo uses only 3 API calls")
    print("- For full functionality run: python alphavantage/example.py")
    print("- Alpha Vantage free tier limits to 5 calls per minute")


if __name__ == "__main__":
    quick_demo() 