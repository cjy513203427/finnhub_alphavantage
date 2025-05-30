"""
Finnhub API Client
Provides easy access to Finnhub stock market data API
"""

import requests
import time
import json
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path to import central config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import config


class FinnhubClient:
    """Finnhub API client for stock market data retrieval"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Finnhub client
        
        Args:
            api_key (Optional[str]): Finnhub API key (optional, uses config if not provided)
        """
        self.api_key = api_key or config.get_finnhub_key()
        
        # Validate API key
        if not self.api_key:
            raise ValueError(
                "❌ Finnhub API key is required!\n"
                "🔧 Setup instructions:\n"
                "   1. Run: python setup_env.py\n"
                "   2. Edit .env file with your API key\n"
                "   3. Get your free key: https://finnhub.io/register"
            )
        
        self.base_url = config.FINNHUB_BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            'X-Finnhub-Token': self.api_key,
            'User-Agent': 'Finnhub-Python-Client/1.0'
        })
        
    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict]:
        """
        Make API request to Finnhub
        
        Args:
            endpoint (str): API endpoint
            params (Optional[Dict]): Query parameters
            
        Returns:
            Optional[Dict]: JSON response or None if error
        """
        try:
            url = f"{self.base_url}/{endpoint}"
            response = self.session.get(url, params=params, timeout=config.REQUEST_TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            
            # Check for API errors
            if isinstance(data, dict) and data.get('error'):
                print(f"API Error: {data['error']}")
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
    
    def get_quote(self, symbol: str) -> Optional[Dict]:
        """
        Get real-time quote for a stock
        
        Args:
            symbol (str): Stock symbol (e.g., 'AAPL')
            
        Returns:
            Optional[Dict]: Quote data with current price, change, etc.
        """
        params = {'symbol': symbol}
        return self._make_request('quote', params)
    
    def get_company_profile(self, symbol: str) -> Optional[Dict]:
        """
        Get company profile and basic information
        
        Args:
            symbol (str): Stock symbol
            
        Returns:
            Optional[Dict]: Company profile data
        """
        params = {'symbol': symbol}
        return self._make_request('stock/profile2', params)
    
    def get_candles(self, symbol: str, resolution: str, from_timestamp: int, to_timestamp: int) -> Optional[Dict]:
        """
        Get historical candlestick data
        
        Args:
            symbol (str): Stock symbol
            resolution (str): Resolution ('1', '5', '15', '30', '60', 'D', 'W', 'M')
            from_timestamp (int): Start timestamp (Unix)
            to_timestamp (int): End timestamp (Unix)
            
        Returns:
            Optional[Dict]: Candlestick data
        """
        params = {
            'symbol': symbol,
            'resolution': resolution,
            'from': from_timestamp,
            'to': to_timestamp
        }
        return self._make_request('stock/candle', params)
    
    def get_market_news(self, category: str = "general", min_id: int = 0) -> Optional[List[Dict]]:
        """
        Get latest market news
        
        Args:
            category (str): News category ('general', 'forex', 'crypto', 'merger')
            min_id (int): Minimum news ID for pagination
            
        Returns:
            Optional[List[Dict]]: List of news articles
        """
        params = {
            'category': category,
            'minId': min_id
        }
        return self._make_request('news', params)
    
    def get_company_news(self, symbol: str, from_date: str, to_date: str) -> Optional[List[Dict]]:
        """
        Get company-specific news
        
        Args:
            symbol (str): Stock symbol
            from_date (str): Start date (YYYY-MM-DD)
            to_date (str): End date (YYYY-MM-DD)
            
        Returns:
            Optional[List[Dict]]: List of company news articles
        """
        params = {
            'symbol': symbol,
            'from': from_date,
            'to': to_date
        }
        return self._make_request('company-news', params)
    
    def get_recommendation_trends(self, symbol: str) -> Optional[List[Dict]]:
        """
        Get analyst recommendation trends
        
        Args:
            symbol (str): Stock symbol
            
        Returns:
            Optional[List[Dict]]: Recommendation trends data
        """
        params = {'symbol': symbol}
        return self._make_request('stock/recommendation', params)
    
    def get_price_target(self, symbol: str) -> Optional[Dict]:
        """
        Get analyst price targets
        
        Args:
            symbol (str): Stock symbol
            
        Returns:
            Optional[Dict]: Price target data
        """
        params = {'symbol': symbol}
        return self._make_request('stock/price-target', params)
    
    def get_earnings(self, symbol: str) -> Optional[List[Dict]]:
        """
        Get earnings data
        
        Args:
            symbol (str): Stock symbol
            
        Returns:
            Optional[List[Dict]]: Earnings data
        """
        params = {'symbol': symbol}
        return self._make_request('stock/earnings', params)
    
    def get_financials_reported(self, symbol: str) -> Optional[Dict]:
        """
        Get reported financial data
        
        Args:
            symbol (str): Stock symbol
            
        Returns:
            Optional[Dict]: Financial data
        """
        params = {'symbol': symbol}
        return self._make_request('stock/financials-reported', params)
    
    def get_basic_financials(self, symbol: str, metric: str = "all") -> Optional[Dict]:
        """
        Get basic financial metrics
        
        Args:
            symbol (str): Stock symbol
            metric (str): Specific metric or 'all'
            
        Returns:
            Optional[Dict]: Financial metrics
        """
        params = {
            'symbol': symbol,
            'metric': metric
        }
        return self._make_request('stock/metric', params)
    
    def get_insider_transactions(self, symbol: str, from_date: str = None, to_date: str = None) -> Optional[Dict]:
        """
        Get insider trading data
        
        Args:
            symbol (str): Stock symbol
            from_date (str): Start date (YYYY-MM-DD)
            to_date (str): End date (YYYY-MM-DD)
            
        Returns:
            Optional[Dict]: Insider trading data
        """
        params = {'symbol': symbol}
        if from_date:
            params['from'] = from_date
        if to_date:
            params['to'] = to_date
            
        return self._make_request('stock/insider-transactions', params)
    
    def get_stock_symbols(self, exchange: str) -> Optional[List[Dict]]:
        """
        Get list of stock symbols for an exchange
        
        Args:
            exchange (str): Exchange code (e.g., 'US', 'L', 'TO')
            
        Returns:
            Optional[List[Dict]]: List of stock symbols
        """
        params = {'exchange': exchange}
        return self._make_request('stock/symbol', params)
    
    def search_symbol(self, query: str) -> Optional[Dict]:
        """
        Search for stock symbols
        
        Args:
            query (str): Search query
            
        Returns:
            Optional[Dict]: Search results
        """
        params = {'q': query}
        return self._make_request('search', params) 