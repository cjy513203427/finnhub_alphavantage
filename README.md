# Finnhub & Alpha Vantage API Clients

This project provides Python clients for calling Finnhub and Alpha Vantage APIs to retrieve stock market data, company information, news, and more.

## Project Structure

```
finnhub_alphavantage/
├── alphavantage/
│   ├── __init__.py             # Alpha Vantage package initialization
│   ├── client.py               # Alpha Vantage API client
│   ├── example.py              # Alpha Vantage usage examples
│   ├── quick_demo.py           # Quick demo with rate limiting
│   └── test.py                 # Connection test script
├── finnhub/
│   ├── __init__.py             # Finnhub package initialization
│   ├── client.py               # Finnhub API client
│   ├── config.py               # API configuration
│   └── example.py              # Finnhub usage examples
├── config.py                   # Central configuration module
├── setup_env.py                # Environment setup script
├── main.py                     # Main program (demonstrates both APIs)
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore file
├── requirements.txt            # Python dependencies
├── environment.yml             # Conda environment configuration
├── README.md                   # Project documentation
└── API使用指南.md              # Chinese usage guide
```

## 🔐 Security Setup (Important!)

This project now uses environment variables for API keys to ensure security.

### Quick Setup

1. **Run the setup script:**
   ```bash
   python setup_env.py
   ```

2. **Edit the `.env` file with your actual API keys:**
   ```bash
   # Get your free API keys from:
   # - Alpha Vantage: https://www.alphavantage.co/support/#api-key
   # - Finnhub: https://finnhub.io/register
   
   ALPHA_VANTAGE_API_KEY=your_actual_alpha_vantage_key
   FINNHUB_API_KEY=your_actual_finnhub_key
   ```

3. **Verify your setup:**
   ```bash
   python -c "from config import config; config.display_config_status()"
   ```

### Manual Setup

If you prefer manual setup:

1. **Copy the template:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` with your API keys**

3. **Ensure `.env` is in `.gitignore`** (it already is!)

## Installation

Create and activate a conda environment:

```bash
# Method 1: Using environment.yml
conda env create -f environment.yml
conda activate stock_api

# Method 2: Manual setup
conda create -n stock_api python=3.9
conda activate stock_api
pip install -r requirements.txt
```

## Features

### Alpha Vantage API Features

- ✅ **Real-time Quotes** - Get real-time stock quotes
- ✅ **Time Series Data** - Intraday, daily, weekly, monthly data
- ✅ **Company Fundamentals** - Company overview, income statements, balance sheets, cash flow
- ✅ **Technical Indicators** - Various technical analysis indicators
- ✅ **Symbol Search** - Search for stock symbols by keywords
- ✅ **Earnings Data** - Quarterly and annual earnings information
- ✅ **Market Performance** - Top gainers/losers rankings
- ✅ **News Sentiment** - News sentiment analysis (paid feature)

### Finnhub API Features

- ✅ **Real-time Quotes** - Get real-time stock quotes
- ✅ **Company Information** - Get company profiles and financial data
- ✅ **Market News** - Get latest market news
- ✅ **Company News** - Get company-specific news
- ✅ **Analyst Recommendations** - Get analyst buy/sell recommendations
- ✅ **Price Targets** - Get analyst price targets
- ✅ **Candlestick Data** - Get historical price data
- ✅ **Financial Reports** - Get company financial statement data

## Usage

### 1. Alpha Vantage API Usage

```python
from alphavantage import AlphaVantageClient

# Initialize client (API key loaded from environment)
client = AlphaVantageClient()

# Get real-time quote
quote_data = client.get_quote("AAPL")
if quote_data and 'Global Quote' in quote_data:
    quote = quote_data['Global Quote']
    price = float(quote['05. price'])
    print(f"Apple stock price: ${price:.2f}")

# Get company overview
overview = client.get_company_overview("AAPL")
if overview:
    print(f"Company Name: {overview['Name']}")
    print(f"Market Cap: ${overview['MarketCapitalization']}")
```

### 2. Finnhub API Usage

```python
from finnhub import FinnhubClient

# Initialize client (API key loaded from environment)
client = FinnhubClient()

# Get stock quote
quote = client.get_quote("AAPL")
if quote:
    current_price = quote['c']  # Current price
    change = quote['d']         # Change
    change_percent = quote['dp'] # Change percentage
    print(f"Apple: ${current_price:.2f} ({change:+.2f}, {change_percent:+.2f}%)")

# Get company profile
profile = client.get_company_profile("AAPL")
if profile:
    print(f"Company Name: {profile['name']}")
    print(f"Industry: {profile['finnhubIndustry']}")
    print(f"Market Cap: ${profile['marketCapitalization']}M")
```

### 3. Running Example Programs

```bash
# Test Alpha Vantage API connection
python alphavantage/test.py

# Run Alpha Vantage quick demo (recommended)
python alphavantage/quick_demo.py

# Run full Alpha Vantage examples (note API limits)
python alphavantage/example.py

# Run Finnhub examples
python finnhub/example.py

# Run main comparison program (recommended)
python main.py
```

**Important:** All example programs require API keys to be configured. If you see import errors, make sure you:
1. Run from the project root directory
2. Have configured your API keys in `.env` file
3. Have activated the correct conda environment

### 4. Running from Any Directory

If you need to run the examples from subdirectories, they automatically add the parent directory to the Python path for imports. However, it's recommended to run all programs from the project root directory.

### 5. Getting Different Types of Data

#### Alpha Vantage Examples

```python
from alphavantage import AlphaVantageClient
client = AlphaVantageClient()

# Get intraday data (5-minute intervals)
intraday = client.get_intraday_data("AAPL", interval="5min")

# Search stocks
search_results = client.search_symbol("Apple")

# Get earnings data
earnings = client.get_earnings("AAPL")

# Get top market performers
market_movers = client.get_top_gainers_losers()
```

#### Finnhub Examples

```python
from finnhub import FinnhubClient
client = FinnhubClient()

# Get market news
news = client.get_market_news()

# Get company news (last 7 days)
from datetime import datetime, timedelta
to_date = datetime.now().strftime('%Y-%m-%d')
from_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
company_news = client.get_company_news("TSLA", from_date, to_date)

# Get analyst recommendations
recommendations = client.get_recommendation_trends("AAPL")

# Get candlestick data
import time
from_time = int(time.time()) - 86400 * 30  # 30 days ago
to_time = int(time.time())
candles = client.get_candles("AAPL", "D", from_time, to_time)
```

## 🔑 API Key Management

### Where to Get API Keys

- **Alpha Vantage**: [Get free key](https://www.alphavantage.co/support/#api-key)
- **Finnhub**: [Get free key](https://finnhub.io/register)

### Security Best Practices

✅ **Do:**
- Store API keys in `.env` file
- Add `.env` to `.gitignore`
- Use environment variables in production
- Share `.env.example` template file

❌ **Don't:**
- Commit API keys to version control
- Share actual `.env` file
- Hardcode keys in source code
- Post keys in public forums

### Environment Variables

The project uses these environment variables:

```bash
ALPHA_VANTAGE_API_KEY=your_key_here
FINNHUB_API_KEY=your_key_here
REQUEST_TIMEOUT=30
MAX_RETRIES=3
```

## Supported Stock Symbols

- US Stocks: AAPL, GOOGL, MSFT, TSLA, AMZN, NVDA, etc.
- Other exchanges are also supported with correct symbol format

## Important Notes

### Alpha Vantage API

1. **Rate Limits**: Free tier limits to 5 API calls per minute, 500 per day
2. **Data Delay**: Real-time data may have 15-minute delay
3. **Paid Features**: News sentiment analysis and other advanced features require paid subscription

### Finnhub API

1. **API Limits**: Free tier has request frequency limits, recommend adding appropriate delays between requests
2. **Error Handling**: All API calls include error handling, returning empty dict/list on failure
3. **Data Format**: All returned data is in JSON format, converted to Python dictionaries

## Example Output

### Alpha Vantage Example Output

```
🚀 Alpha Vantage API Example Program
============================================================

📈 1. Get real-time quotes for popular stocks:
  AAPL: $150.25 (+2.15, +1.45%)
  GOOGL: $2750.80 (-5.20, -0.19%)
  MSFT: $310.45 (+1.85, +0.60%)
  ...

🔍 2. Search stock symbols (keyword: 'Apple'):
  1. AAPL - Apple Inc (match score: 1.0000)
  2. APLE - Apple Hospitality REIT Inc (match score: 0.5714)
  ...

🏢 3. Get company basic information (Apple):
  Company Name: Apple Inc
  Industry: Consumer Electronics
  Sector: Technology
  Market Cap: $2500000000000
  ...
```

### Main Program Output

```
🚀 Finnhub & Alpha Vantage API Comparison Tool
======================================================================

🔍 Comparing AAPL data from both APIs:
============================================================

📊 Alpha Vantage Data:
  Price: $199.95
  Change: -0.47 (-0.2345%)

📈 Finnhub Data:  
  Price: $199.95
  Change: -0.47 (-0.23%)

💡 Price Difference: $0.00
  ✅ Prices are very close (difference < $0.50)
```

## API Comparison

| Feature | Alpha Vantage | Finnhub |
|---------|---------------|---------|
| Real-time Quotes | ✅ | ✅ |
| Historical Data | ✅ (Detailed) | ✅ |
| Company Fundamentals | ✅ (Detailed) | ✅ |
| News | ✅ (Paid) | ✅ (Free) |
| Technical Indicators | ✅ | ❌ |
| Free Limits | 5/minute | 60/minute |
| Data Quality | High | High |

## Troubleshooting

If you encounter issues, check the following in order:

1. **API Key Setup**
   ```bash
   python setup_env.py  # Run setup script
   python -c "from config import config; config.display_config_status()"
   ```

2. **Network Connection**
   - Ensure internet access is available
   - Check firewall settings

3. **Dependencies Installation**
   ```bash
   pip install -r requirements.txt
   ```

4. **API Limits**
   - Alpha Vantage: 5 calls per minute
   - Finnhub: 60 calls per minute

5. **Stock Symbol Format**
   - Use correct stock symbols (e.g., AAPL not Apple)

## Technical Support

If you encounter problems, please check:
1. API keys are correctly configured in `.env`
2. Network connection is normal
3. Stock symbol format is correct
4. API request limits haven't been exceeded

## Development Roadmap

- [x] ~~Add Alpha Vantage API client~~
- [x] ~~Separate APIs into different modules~~
- [x] ~~Use English comments only~~
- [x] ~~Implement secure API key management~~
- [ ] Add data visualization features
- [ ] Add data storage functionality
- [ ] Create Web interface
- [ ] Add more technical indicators
- [ ] Integrate additional data sources 