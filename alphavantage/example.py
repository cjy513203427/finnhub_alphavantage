"""
Alpha Vantage API Example Usage
Demonstrates various API calls and data retrieval using Alpha Vantage
"""

import sys
import os
# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from alphavantage.client import AlphaVantageClient
import time
from datetime import datetime, timedelta
import json


def main():
    """Main function demonstrating Alpha Vantage API usage"""
    
    # Initialize client with API key
    client = AlphaVantageClient()
    
    print("🚀 Alpha Vantage API Example Program")
    print("=" * 60)
    
    # Example 1: Get real-time quotes for popular stocks
    print("\n📈 1. Get real-time quotes for popular stocks:")
    symbols = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]
    
    for symbol in symbols:
        quote_data = client.get_quote(symbol)
        if quote_data and 'Global Quote' in quote_data:
            quote = quote_data['Global Quote']
            price = float(quote.get('05. price', 0))
            change = float(quote.get('09. change', 0))
            change_percent = quote.get('10. change percent', '0%').replace('%', '')
            
            print(f"  {symbol}: ${price:.2f} ({change:+.2f}, {change_percent}%)")
        else:
            print(f"  {symbol}: Failed to get data")
        time.sleep(12)  # Alpha Vantage rate limiting (5 calls per minute for free tier)
    
    # Example 2: Search for symbols
    print("\n🔍 2. Search stock symbols (keyword: 'Apple'):")
    search_results = client.search_symbol("Apple")
    if search_results and 'bestMatches' in search_results:
        for i, match in enumerate(search_results['bestMatches'][:5]):  # Show first 5 results
            symbol = match.get('1. symbol', 'N/A')
            name = match.get('2. name', 'N/A')
            match_score = match.get('9. matchScore', 'N/A')
            print(f"  {i+1}. {symbol} - {name} (match score: {match_score})")
    else:
        print("  Failed to get search results")
    time.sleep(12)
    
    # Example 3: Get company overview
    print("\n🏢 3. Get company basic information (Apple):")
    overview = client.get_company_overview("AAPL")
    if overview:
        print(f"  Company Name: {overview.get('Name', 'N/A')}")
        print(f"  Industry: {overview.get('Industry', 'N/A')}")
        print(f"  Sector: {overview.get('Sector', 'N/A')}")
        print(f"  Country: {overview.get('Country', 'N/A')}")
        print(f"  Market Cap: ${overview.get('MarketCapitalization', 'N/A')}")
        print(f"  P/E Ratio: {overview.get('PERatio', 'N/A')}")
        print(f"  Dividend Yield: {overview.get('DividendYield', 'N/A')}")
        print(f"  52 Week High: ${overview.get('52WeekHigh', 'N/A')}")
        print(f"  52 Week Low: ${overview.get('52WeekLow', 'N/A')}")
    else:
        print("  Failed to get company information")
    time.sleep(12)
    
    # Example 4: Get daily stock data
    print("\n📊 4. Get daily stock price data (Tesla, last 100 days):")
    daily_data = client.get_daily_data("TSLA", adjusted=True, outputsize="compact")
    if daily_data and 'Time Series (Daily)' in daily_data:
        time_series = daily_data['Time Series (Daily)']
        # Get the most recent 5 days
        recent_dates = sorted(time_series.keys(), reverse=True)[:5]
        
        for date in recent_dates:
            data = time_series[date]
            open_price = float(data.get('1. open', 0))
            high_price = float(data.get('2. high', 0))
            low_price = float(data.get('3. low', 0))
            close_price = float(data.get('4. close', 0))
            volume = int(data.get('6. volume', 0))
            
            print(f"  {date}: Open ${open_price:.2f} High ${high_price:.2f} Low ${low_price:.2f} Close ${close_price:.2f} Volume {volume:,}")
    else:
        print("  Failed to get daily data")
    time.sleep(12)
    
    # Example 5: Get intraday data
    print("\n⏰ 5. Get intraday data (Apple, 5-minute intervals):")
    intraday_data = client.get_intraday_data("AAPL", interval="5min", outputsize="compact")
    if intraday_data and 'Time Series (5min)' in intraday_data:
        time_series = intraday_data['Time Series (5min)']
        # Get the most recent 3 time points
        recent_times = sorted(time_series.keys(), reverse=True)[:3]
        
        for timestamp in recent_times:
            data = time_series[timestamp]
            open_price = float(data.get('1. open', 0))
            close_price = float(data.get('4. close', 0))
            volume = int(data.get('5. volume', 0))
            
            print(f"  {timestamp}: Open ${open_price:.2f} Close ${close_price:.2f} Volume {volume:,}")
    else:
        print("  Failed to get intraday data")
    time.sleep(12)
    
    # Example 6: Get earnings data
    print("\n💰 6. Get earnings data (Microsoft):")
    earnings = client.get_earnings("MSFT")
    if earnings:
        if 'quarterlyEarnings' in earnings:
            quarterly = earnings['quarterlyEarnings'][:3]  # Most recent 3 quarters
            print("  Quarterly Earnings:")
            for quarter in quarterly:
                date = quarter.get('fiscalDateEnding', 'N/A')
                eps = quarter.get('reportedEPS', 'N/A')
                estimated_eps = quarter.get('estimatedEPS', 'N/A')
                surprise = quarter.get('surprise', 'N/A')
                print(f"    {date}: Actual EPS ${eps}, Estimated EPS ${estimated_eps}, Surprise ${surprise}")
        
        if 'annualEarnings' in earnings:
            annual = earnings['annualEarnings'][:2]  # Most recent 2 years
            print("  Annual Earnings:")
            for year in annual:
                date = year.get('fiscalDateEnding', 'N/A')
                eps = year.get('reportedEPS', 'N/A')
                print(f"    {date}: EPS ${eps}")
    else:
        print("  Failed to get earnings data")
    time.sleep(12)
    
    # Example 7: Get top gainers and losers
    print("\n🏆 7. Get top performing/worst performing stocks:")
    market_data = client.get_top_gainers_losers()
    if market_data:
        if 'top_gainers' in market_data:
            print("  Top gainers today:")
            for i, stock in enumerate(market_data['top_gainers'][:3]):  # Top 3
                ticker = stock.get('ticker', 'N/A')
                price = stock.get('price', 'N/A')
                change_amount = stock.get('change_amount', 'N/A')
                change_percentage = stock.get('change_percentage', 'N/A')
                print(f"    {i+1}. {ticker}: ${price} ({change_amount}, {change_percentage})")
        
        if 'top_losers' in market_data:
            print("  Top losers today:")
            for i, stock in enumerate(market_data['top_losers'][:3]):  # Top 3
                ticker = stock.get('ticker', 'N/A')
                price = stock.get('price', 'N/A')
                change_amount = stock.get('change_amount', 'N/A')
                change_percentage = stock.get('change_percentage', 'N/A')
                print(f"    {i+1}. {ticker}: ${price} ({change_amount}, {change_percentage})")
    else:
        print("  Failed to get market data")
    
    print("\n" + "=" * 60)
    print("✅ Alpha Vantage example program completed!")


def get_comprehensive_stock_analysis(symbol: str):
    """Get comprehensive analysis for a specific stock"""
    client = AlphaVantageClient()
    
    print(f"\n📊 {symbol} Comprehensive Analysis:")
    print("-" * 50)
    
    # Get quote
    print("1. Real-time Quote:")
    quote_data = client.get_quote(symbol)
    if quote_data and 'Global Quote' in quote_data:
        quote = quote_data['Global Quote']
        price = float(quote.get('05. price', 0))
        change = float(quote.get('09. change', 0))
        change_percent = quote.get('10. change percent', '0%')
        volume = quote.get('06. volume', 'N/A')
        
        print(f"   Current Price: ${price:.2f}")
        print(f"   Change: {change:+.2f} ({change_percent})")
        print(f"   Volume: {volume}")
    
    time.sleep(12)
    
    # Get company overview
    print("\n2. Company Overview:")
    overview = client.get_company_overview(symbol)
    if overview:
        print(f"   Company Name: {overview.get('Name', 'N/A')}")
        print(f"   Market Cap: ${overview.get('MarketCapitalization', 'N/A')}")
        print(f"   P/E Ratio: {overview.get('PERatio', 'N/A')}")
        print(f"   P/B Ratio: {overview.get('PriceToBookRatio', 'N/A')}")
        print(f"   ROE: {overview.get('ReturnOnEquityTTM', 'N/A')}")
        print(f"   ROA: {overview.get('ReturnOnAssetsTTM', 'N/A')}")
    
    time.sleep(12)
    
    # Get recent price performance
    print("\n3. Recent Price Performance:")
    daily_data = client.get_daily_data(symbol, outputsize="compact")
    if daily_data and 'Time Series (Daily)' in daily_data:
        time_series = daily_data['Time Series (Daily)']
        recent_dates = sorted(time_series.keys(), reverse=True)
        
        if len(recent_dates) >= 2:
            today = time_series[recent_dates[0]]
            week_ago = time_series[recent_dates[min(4, len(recent_dates)-1)]]
            
            today_close = float(today.get('4. close', 0))
            week_ago_close = float(week_ago.get('4. close', 0))
            week_change = ((today_close - week_ago_close) / week_ago_close) * 100
            
            print(f"   5-day change: {week_change:+.2f}%")
            print(f"   Latest trading day high: ${float(today.get('2. high', 0)):.2f}")
            print(f"   Latest trading day low: ${float(today.get('3. low', 0)):.2f}")
    
    return {"quote": quote_data, "overview": overview, "daily": daily_data}


def demonstrate_news_sentiment():
    """Demonstrate news sentiment analysis feature"""
    client = AlphaVantageClient()
    
    print("\n📰 News Sentiment Analysis Example:")
    print("-" * 40)
    
    # Get news sentiment for popular tech stocks
    tech_stocks = "AAPL,GOOGL,MSFT"
    news_data = client.get_news_sentiment(tickers=tech_stocks, limit=10)
    
    if news_data and 'feed' in news_data:
        print(f"Retrieved {len(news_data['feed'])} news articles")
        
        for i, article in enumerate(news_data['feed'][:3]):  # Show first 3
            title = article.get('title', 'No title')
            source = article.get('source', 'Unknown')
            time_published = article.get('time_published', 'Unknown')
            
            # Format time
            if len(time_published) >= 8:
                formatted_time = f"{time_published[:4]}-{time_published[4:6]}-{time_published[6:8]}"
            else:
                formatted_time = time_published
            
            print(f"\n{i+1}. [{source}] {title}")
            print(f"   Published: {formatted_time}")
            
            # Show sentiment scores if available
            if 'overall_sentiment_score' in article:
                sentiment_score = article['overall_sentiment_score']
                sentiment_label = article.get('overall_sentiment_label', 'Unknown')
                print(f"   Overall Sentiment: {sentiment_label} (score: {sentiment_score})")
    else:
        print("Failed to get news data")


if __name__ == "__main__":
    # Run main examples
    main()
    
    # Demonstrate comprehensive analysis
    print("\n" + "=" * 60)
    get_comprehensive_stock_analysis("NVDA")
    
    # Demonstrate news sentiment (if available in your API plan)
    print("\n" + "=" * 60)
    print("Note: News sentiment analysis requires a paid API subscription")
    # Uncomment the line below if you have a paid subscription
    # demonstrate_news_sentiment()
    
    print("\n" + "=" * 60)
    print("🎉 All examples completed!")
    print("\nTips:")
    print("- Alpha Vantage free tier limits to 5 API calls per minute")
    print("- Some features (like news sentiment analysis) require paid subscription")
    print("- It's recommended to add appropriate delays between API calls to avoid limits") 