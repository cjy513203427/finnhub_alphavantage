"""
Central configuration module for API keys and settings
Loads configuration from environment variables with secure fallback handling
"""

import os
from typing import Optional
from dotenv import load_dotenv
from pathlib import Path

# Get the directory of this config file
config_dir = Path(__file__).parent
env_file = config_dir / '.env'

# Load environment variables from .env file with explicit path
if env_file.exists():
    load_dotenv(env_file)
    print(f"✅ Loaded environment variables from {env_file}")
else:
    print(f"⚠️  .env file not found at {env_file}")
    load_dotenv()  # Try to load from current directory anyway


class Config:
    """Configuration class for API keys and settings"""
    
    def __init__(self):
        """Initialize configuration from environment variables"""
        self.load_from_env()
    
    def load_from_env(self):
        """Load configuration from environment variables"""
        # Alpha Vantage API configuration
        self.ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')
        self.ALPHA_VANTAGE_BASE_URL = "https://www.alphavantage.co/query"
        
        # Finnhub API configuration  
        self.FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY')
        self.FINNHUB_BASE_URL = "https://finnhub.io/api/v1"
        
        # Request settings
        self.REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', '30'))
        self.MAX_RETRIES = int(os.getenv('MAX_RETRIES', '3'))
        
        # Validate required keys
        self._validate_config()
    
    def _validate_config(self):
        """Validate that required API keys are present"""
        missing_keys = []
        
        if not self.ALPHA_VANTAGE_API_KEY:
            missing_keys.append('ALPHA_VANTAGE_API_KEY')
        
        if not self.FINNHUB_API_KEY:
            missing_keys.append('FINNHUB_API_KEY')
        
        if missing_keys:
            print("🚨 CRITICAL: Missing required API keys in environment variables!")
            print("❌ Missing keys:")
            for key in missing_keys:
                print(f"   - {key}")
            print("\n🔧 Required Setup:")
            print("1. Run: python setup_env.py")
            print("2. Edit .env file with your actual API keys:")
            print("   - Get Alpha Vantage key: https://www.alphavantage.co/support/#api-key")
            print("   - Get Finnhub key: https://finnhub.io/register")
            print("3. Restart the application")
            print("\n⚠️  Application may not function properly without valid API keys!")
    
    def get_alpha_vantage_key(self) -> Optional[str]:
        """
        Get Alpha Vantage API key
        
        Returns:
            Optional[str]: API key if configured, None otherwise
        """
        if not self.ALPHA_VANTAGE_API_KEY:
            print("❌ Alpha Vantage API key not configured!")
            print("💡 Run 'python setup_env.py' to configure your API keys")
            return None
        return self.ALPHA_VANTAGE_API_KEY
    
    def get_finnhub_key(self) -> Optional[str]:
        """
        Get Finnhub API key
        
        Returns:
            Optional[str]: API key if configured, None otherwise
        """
        if not self.FINNHUB_API_KEY:
            print("❌ Finnhub API key not configured!")
            print("💡 Run 'python setup_env.py' to configure your API keys")
            return None
        return self.FINNHUB_API_KEY
    
    def is_configured(self) -> bool:
        """
        Check if all required API keys are configured
        
        Returns:
            bool: True if all keys are configured, False otherwise
        """
        return bool(self.ALPHA_VANTAGE_API_KEY and self.FINNHUB_API_KEY)
    
    def display_config_status(self):
        """Display current configuration status"""
        print("📊 Current Configuration Status:")
        print(f"   Alpha Vantage API: {'✅ Configured' if self.ALPHA_VANTAGE_API_KEY else '❌ Missing'}")
        print(f"   Finnhub API: {'✅ Configured' if self.FINNHUB_API_KEY else '❌ Missing'}")
        print(f"   Request Timeout: {self.REQUEST_TIMEOUT}s")
        print(f"   Max Retries: {self.MAX_RETRIES}")
        
        if not self.is_configured():
            print("\n🔧 To configure missing API keys:")
            print("   1. Run: python setup_env.py")
            print("   2. Edit .env file with your actual keys")
            print("   3. Restart the application")


# Global configuration instance
config = Config() 