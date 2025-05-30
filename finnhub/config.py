"""
Configuration settings for Finnhub API client
Now uses central config module for API keys with secure handling
"""

import sys
import os

# Add parent directory to path to import central config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import config

# Finnhub API configuration (using central config)
FINNHUB_API_KEY = config.get_finnhub_key()
FINNHUB_BASE_URL = config.FINNHUB_BASE_URL

# Request settings (using central config)
REQUEST_TIMEOUT = config.REQUEST_TIMEOUT
MAX_RETRIES = config.MAX_RETRIES

# Validate configuration
if not FINNHUB_API_KEY:
    print("⚠️  Finnhub API key not configured in finnhub/config.py")
    print("💡 This will cause import errors. Please configure your environment variables.") 