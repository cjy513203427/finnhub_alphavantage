#!/usr/bin/env python3
"""
Import Test Script
Tests that all modules can be imported correctly
"""

import sys
from pathlib import Path

def test_imports():
    """Test all module imports"""
    print("🧪 Testing Module Imports...")
    print("=" * 50)
    
    errors = []
    
    # Test central config
    try:
        from config import config
        print("✅ Central config module imported successfully")
    except Exception as e:
        errors.append(f"❌ Central config: {e}")
    
    # Test AlphaVantage client
    try:
        from alphavantage import AlphaVantageClient
        print("✅ AlphaVantage client imported successfully")
    except Exception as e:
        errors.append(f"❌ AlphaVantage client: {e}")
    
    # Test Finnhub client
    try:
        from finnhub import FinnhubClient
        print("✅ Finnhub client imported successfully")
    except Exception as e:
        errors.append(f"❌ Finnhub client: {e}")
    
    # Test client initialization (should fail gracefully without API keys)
    try:
        # This should raise ValueError due to missing API keys
        from alphavantage import AlphaVantageClient
        try:
            client = AlphaVantageClient()
            print("⚠️  AlphaVantage client initialized (unexpected)")
        except ValueError:
            print("✅ AlphaVantage client correctly requires API key")
    except Exception as e:
        errors.append(f"❌ AlphaVantage client validation: {e}")
    
    try:
        # This should raise ValueError due to missing API keys
        from finnhub import FinnhubClient
        try:
            client = FinnhubClient()
            print("⚠️  Finnhub client initialized (unexpected)")
        except ValueError:
            print("✅ Finnhub client correctly requires API key")
    except Exception as e:
        errors.append(f"❌ Finnhub client validation: {e}")
    
    print("\n" + "=" * 50)
    
    if errors:
        print("❌ Import test failed with errors:")
        for error in errors:
            print(f"   {error}")
        return False
    else:
        print("✅ All imports successful!")
        print("\n💡 To run programs, configure API keys:")
        print("   1. Run: python setup_env.py")
        print("   2. Edit .env with your API keys")
        print("   3. Run example programs")
        return True


if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1) 