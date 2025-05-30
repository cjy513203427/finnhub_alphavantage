"""
Alpha Vantage API Client
Provides easy access to Alpha Vantage financial data API
"""

import requests
import time
import json
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import config


class AlphaVantageClient:
    """Alpha Vantage API client for financial data retrieval"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Alpha Vantage client
        
        Args:
            api_key (Optional[str]): Alpha Vantage API key (optional, uses config if not provided)
        """
        self.api_key = api_key or config.get_alpha_vantage_key()
        
        # Validate API key
        if not self.api_key:
            raise ValueError(
                "❌ Alpha Vantage API key is required!\n"
                "🔧 Setup instructions:\n"
                "   1. Run: python setup_env.py\n"
                "   2. Edit .env file with your API key\n"
                "   3. Get your free key: https://www.alphavantage.co/support/#api-key"
            )
        
        self.base_url = config.ALPHA_VANTAGE_BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'AlphaVantage-Python-Client/1.0'
        })
        
    def _make_request(self, params: Dict[str, Any]) -> Optional[Dict]:
        """
        Make API request to Alpha Vantage
        
        Args:
            params (Dict): API parameters
            
        Returns:
            Optional[Dict]: JSON response or None if error
        """
        try:
            # Add API key to parameters
            params['apikey'] = self.api_key
            
            response = self.session.get(self.base_url, params=params, timeout=config.REQUEST_TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            
            # Check for API error messages
            if 'Error Message' in data:
                print(f"API Error: {data['Error Message']}")
                return None
            elif 'Note' in data:
                print(f"API Note: {data['Note']}")
                return None
            elif 'Information' in data:
                print(f"API Info: {data['Information']}")
                return None
                
            return data
            
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
    
    def get_intraday_data(self, symbol: str, interval: str = "5min", 
                         adjusted: bool = True, extended_hours: bool = True, 
                         month: Optional[str] = None, outputsize: str = "compact") -> Optional[Dict]:
        """
        Get intraday time series data
        
        Args:
            symbol (str): Stock symbol (e.g., 'AAPL')
            interval (str): Time interval ('1min', '5min', '15min', '30min', '60min')
            adjusted (bool): Whether to include adjusted close prices
            extended_hours (bool): Whether to include extended trading hours
            month (str): Specific month in YYYY-MM format
            outputsize (str): 'compact' (100 data points) or 'full' (full data)
            
        Returns:
            Optional[Dict]: Intraday data or None if error
        """
        params = {
            'function': 'TIME_SERIES_INTRADAY',
            'symbol': symbol,
            'interval': interval,
            'adjusted': str(adjusted).lower(),
            'extended_hours': str(extended_hours).lower(),
            'outputsize': outputsize
        }
        
        if month:
            params['month'] = month
            
        return self._make_request(params)
    
    def get_daily_data(self, symbol: str, adjusted: bool = True, 
                      outputsize: str = "compact") -> Optional[Dict]:
        """
        Get daily time series data
        
        Args:
            symbol (str): Stock symbol
            adjusted (bool): Whether to get adjusted data
            outputsize (str): 'compact' or 'full'
            
        Returns:
            Optional[Dict]: Daily data or None if error
        """
        function = 'TIME_SERIES_DAILY_ADJUSTED' if adjusted else 'TIME_SERIES_DAILY'
        
        params = {
            'function': function,
            'symbol': symbol,
            'outputsize': outputsize
        }
        
        return self._make_request(params)
    
    def get_weekly_data(self, symbol: str, adjusted: bool = True) -> Optional[Dict]:
        """
        Get weekly time series data
        
        Args:
            symbol (str): Stock symbol
            adjusted (bool): Whether to get adjusted data
            
        Returns:
            Optional[Dict]: Weekly data or None if error
        """
        function = 'TIME_SERIES_WEEKLY_ADJUSTED' if adjusted else 'TIME_SERIES_WEEKLY'
        
        params = {
            'function': function,
            'symbol': symbol
        }
        
        return self._make_request(params)
    
    def get_monthly_data(self, symbol: str, adjusted: bool = True) -> Optional[Dict]:
        """
        Get monthly time series data
        
        Args:
            symbol (str): Stock symbol
            adjusted (bool): Whether to get adjusted data
            
        Returns:
            Optional[Dict]: Monthly data or None if error
        """
        function = 'TIME_SERIES_MONTHLY_ADJUSTED' if adjusted else 'TIME_SERIES_MONTHLY'
        
        params = {
            'function': function,
            'symbol': symbol
        }
        
        return self._make_request(params)
    
    def get_quote(self, symbol: str) -> Optional[Dict]:
        """
        Get real-time quote data
        
        Args:
            symbol (str): Stock symbol
            
        Returns:
            Optional[Dict]: Quote data or None if error
        """
        params = {
            'function': 'GLOBAL_QUOTE',
            'symbol': symbol
        }
        
        return self._make_request(params)
    
    def search_symbol(self, keywords: str) -> Optional[Dict]:
        """
        Search for symbols based on keywords
        
        Args:
            keywords (str): Search keywords
            
        Returns:
            Optional[Dict]: Search results or None if error
        """
        params = {
            'function': 'SYMBOL_SEARCH',
            'keywords': keywords
        }
        
        return self._make_request(params)
    
    def get_company_overview(self, symbol: str) -> Optional[Dict]:
        """
        Get company fundamental data overview
        
        Args:
            symbol (str): Stock symbol
            
        Returns:
            Optional[Dict]: Company overview data or None if error
        """
        params = {
            'function': 'OVERVIEW',
            'symbol': symbol
        }
        
        return self._make_request(params)
    
    def get_income_statement(self, symbol: str) -> Optional[Dict]:
        """
        Get annual and quarterly income statements
        
        Args:
            symbol (str): Stock symbol
            
        Returns:
            Optional[Dict]: Income statement data or None if error
        """
        params = {
            'function': 'INCOME_STATEMENT',
            'symbol': symbol
        }
        
        return self._make_request(params)
    
    def get_balance_sheet(self, symbol: str) -> Optional[Dict]:
        """
        Get annual and quarterly balance sheets
        
        Args:
            symbol (str): Stock symbol
            
        Returns:
            Optional[Dict]: Balance sheet data or None if error
        """
        params = {
            'function': 'BALANCE_SHEET',
            'symbol': symbol
        }
        
        return self._make_request(params)
    
    def get_cash_flow(self, symbol: str) -> Optional[Dict]:
        """
        Get annual and quarterly cash flow statements
        
        Args:
            symbol (str): Stock symbol
            
        Returns:
            Optional[Dict]: Cash flow data or None if error
        """
        params = {
            'function': 'CASH_FLOW',
            'symbol': symbol
        }
        
        return self._make_request(params)
    
    def get_earnings(self, symbol: str) -> Optional[Dict]:
        """
        Get quarterly and annual earnings data
        
        Args:
            symbol (str): Stock symbol
            
        Returns:
            Optional[Dict]: Earnings data or None if error
        """
        params = {
            'function': 'EARNINGS',
            'symbol': symbol
        }
        
        return self._make_request(params)
    
    def get_top_gainers_losers(self) -> Optional[Dict]:
        """
        Get top gainers, losers, and most active stocks
        
        Returns:
            Optional[Dict]: Market data or None if error
        """
        params = {
            'function': 'TOP_GAINERS_LOSERS'
        }
        
        return self._make_request(params)
    
    def get_news_sentiment(self, tickers: Optional[str] = None, 
                          topics: Optional[str] = None, 
                          time_from: Optional[str] = None,
                          time_to: Optional[str] = None,
                          sort: str = "LATEST", limit: int = 50) -> Optional[Dict]:
        """
        Get news sentiment data
        
        Args:
            tickers (str): Comma-separated list of stock tickers
            topics (str): Comma-separated list of topics
            time_from (str): Start time in YYYYMMDDTHHMM format
            time_to (str): End time in YYYYMMDDTHHMM format
            sort (str): Sort order ('LATEST', 'EARLIEST', 'RELEVANCE')
            limit (int): Number of articles to return (max 1000)
            
        Returns:
            Optional[Dict]: News sentiment data or None if error
        """
        params = {
            'function': 'NEWS_SENTIMENT',
            'sort': sort,
            'limit': str(limit)
        }
        
        if tickers:
            params['tickers'] = tickers
        if topics:
            params['topics'] = topics
        if time_from:
            params['time_from'] = time_from
        if time_to:
            params['time_to'] = time_to
            
        return self._make_request(params) 