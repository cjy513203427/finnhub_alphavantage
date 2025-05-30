#!/usr/bin/env python3
"""
Environment Setup Script
Helps users configure API keys and environment variables
"""

import os
import shutil


def create_env_file():
    """Create .env file from template"""
    env_example_content = """# API Keys Configuration
# Get your API keys from:
# - Alpha Vantage: https://www.alphavantage.co/support/#api-key
# - Finnhub: https://finnhub.io/register

# Alpha Vantage API Key
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key_here

# Finnhub API Key  
FINNHUB_API_KEY=your_finnhub_api_key_here

# Request settings
REQUEST_TIMEOUT=30
MAX_RETRIES=3
"""
    
    # Create .env.example if it doesn't exist
    if not os.path.exists('.env.example'):
        with open('.env.example', 'w', encoding='utf-8') as f:
            f.write(env_example_content)
        print("✅ Created .env.example template file")
    
    # Check if .env already exists
    if os.path.exists('.env'):
        response = input("📁 .env file already exists. Overwrite? (y/N): ").lower()
        if response != 'y':
            print("💡 Keeping existing .env file")
            return
    
    # Copy template to .env
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_example_content)
        print("✅ Created .env file from template")
        print("📝 Please edit .env and add your actual API keys")
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")


def check_gitignore():
    """Check if .gitignore includes .env"""
    gitignore_exists = os.path.exists('.gitignore')
    
    if not gitignore_exists:
        print("⚠️  .gitignore file not found")
        return
    
    with open('.gitignore', 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '.env' in content:
        print("✅ .env is already in .gitignore")
    else:
        print("⚠️  .env not found in .gitignore")
        response = input("📝 Add .env to .gitignore? (Y/n): ").lower()
        if response != 'n':
            with open('.gitignore', 'a', encoding='utf-8') as f:
                f.write('\n# Environment files\n.env\n')
            print("✅ Added .env to .gitignore")


def display_instructions():
    """Display setup instructions"""
    print("\n" + "="*60)
    print("🔐 API Keys Security Setup Complete!")
    print("="*60)
    print("\n📋 Next Steps:")
    print("1. Edit the .env file and add your actual API keys:")
    print("   - Get Alpha Vantage key: https://www.alphavantage.co/support/#api-key")
    print("   - Get Finnhub key: https://finnhub.io/register")
    print("\n2. Your .env file will look like:")
    print("   ALPHA_VANTAGE_API_KEY=your_actual_key_here")
    print("   FINNHUB_API_KEY=your_actual_key_here")
    print("\n3. The .env file is automatically ignored by git for security")
    print("\n4. Test your setup by running:")
    print("   python -c \"from config import config; config.display_config_status()\"")
    print("\n🔒 Security Notes:")
    print("- Never commit API keys to version control")
    print("- The .env file is listed in .gitignore")
    print("- Share .env.example (template) but never .env (with real keys)")


def main():
    """Main setup function"""
    print("🚀 Setting up secure API key configuration...")
    print("="*60)
    
    # Check current directory
    if not os.path.exists('config.py'):
        print("❌ Please run this script from the project root directory")
        return
    
    # Create environment files
    create_env_file()
    
    # Check gitignore
    check_gitignore()
    
    # Display instructions
    display_instructions()


if __name__ == "__main__":
    main() 