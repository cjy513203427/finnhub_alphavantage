# Alpha Vantage & Finnhub API 使用指南

## 概述

本项目提供了两个强大的金融数据API客户端：
- **Alpha Vantage**: 提供详细的股票数据、技术指标和基本面分析
- **Finnhub**: 提供实时市场数据、新闻和分析师推荐

## 快速开始

### 1. 环境设置

```bash
# 激活conda环境
conda activate stock_api

# 或者创建新环境
conda create -n stock_api python=3.9
conda activate stock_api
pip install -r requirements.txt
```

### 2. 测试API连接

```bash
# 测试 Alpha Vantage API
python test_alphavantage.py

# 如果测试通过，运行快速演示
python alphavantage_quick_demo.py
```

## Alpha Vantage API 详细使用

### 基本使用方法

```python
from alphavantage_client import AlphaVantageClient

# 初始化客户端（API密钥已预配置）
client = AlphaVantageClient()
```

### 1. 获取实时报价

```python
# 获取股票实时报价
quote_data = client.get_quote("AAPL")
if quote_data and 'Global Quote' in quote_data:
    quote = quote_data['Global Quote']
    price = float(quote['05. price'])
    change = float(quote['09. change'])
    print(f"Apple股价: ${price:.2f}, 涨跌: {change:+.2f}")
```

### 2. 搜索股票代码

```python
# 根据公司名称搜索股票代码
search_results = client.search_symbol("Apple")
if search_results and 'bestMatches' in search_results:
    for match in search_results['bestMatches'][:5]:
        symbol = match['1. symbol']
        name = match['2. name']
        print(f"{symbol}: {name}")
```

### 3. 获取历史数据

```python
# 获取每日数据
daily_data = client.get_daily_data("AAPL", outputsize="compact")
if daily_data and 'Time Series (Daily)' in daily_data:
    time_series = daily_data['Time Series (Daily)']
    # 获取最近5天的数据
    recent_dates = sorted(time_series.keys(), reverse=True)[:5]
    for date in recent_dates:
        data = time_series[date]
        close_price = float(data['4. close'])
        volume = int(data['6. volume'])
        print(f"{date}: 收盘价 ${close_price:.2f}, 成交量 {volume:,}")
```

### 4. 获取盘中数据

```python
# 获取5分钟间隔的盘中数据
intraday = client.get_intraday_data("AAPL", interval="5min")
if intraday and 'Time Series (5min)' in intraday:
    time_series = intraday['Time Series (5min)']
    # 获取最新3个数据点
    recent_times = sorted(time_series.keys(), reverse=True)[:3]
    for timestamp in recent_times:
        data = time_series[timestamp]
        close_price = float(data['4. close'])
        print(f"{timestamp}: ${close_price:.2f}")
```

### 5. 获取公司基本面数据

```python
# 获取公司概况
overview = client.get_company_overview("AAPL")
if overview:
    print(f"公司名称: {overview['Name']}")
    print(f"市值: ${overview['MarketCapitalization']}")
    print(f"市盈率: {overview['PERatio']}")
    print(f"ROE: {overview['ReturnOnEquityTTM']}")

# 获取收益数据
earnings = client.get_earnings("AAPL")
if earnings and 'quarterlyEarnings' in earnings:
    for quarter in earnings['quarterlyEarnings'][:4]:  # 最近4个季度
        date = quarter['fiscalDateEnding']
        eps = quarter['reportedEPS']
        print(f"{date}: EPS ${eps}")
```

### 6. 获取市场表现数据

```python
# 获取当日涨幅/跌幅最大的股票
market_data = client.get_top_gainers_losers()
if market_data:
    # 涨幅最大
    if 'top_gainers' in market_data:
        print("今日涨幅最大:")
        for stock in market_data['top_gainers'][:3]:
            print(f"{stock['ticker']}: {stock['price']} ({stock['change_percentage']})")
    
    # 跌幅最大
    if 'top_losers' in market_data:
        print("今日跌幅最大:")
        for stock in market_data['top_losers'][:3]:
            print(f"{stock['ticker']}: {stock['price']} ({stock['change_percentage']})")
```

## Finnhub API 详细使用

### 基本使用方法

```python
from finnhub_client import FinnhubClient

# 初始化客户端（API密钥已预配置）
client = FinnhubClient()
```

### 1. 获取实时报价

```python
# 获取股票实时报价
quote = client.get_quote("AAPL")
if quote:
    current_price = quote['c']  # 当前价格
    change = quote['d']         # 变化
    change_percent = quote['dp'] # 变化百分比
    print(f"Apple: ${current_price:.2f} ({change:+.2f}, {change_percent:+.2f}%)")
```

### 2. 获取公司信息

```python
# 获取公司基本信息
profile = client.get_company_profile("AAPL")
if profile:
    print(f"公司名称: {profile['name']}")
    print(f"行业: {profile['finnhubIndustry']}")
    print(f"市值: ${profile['marketCapitalization']}M")
    print(f"网站: {profile['weburl']}")
```

### 3. 获取新闻

```python
# 获取市场新闻
news = client.get_market_news()
if news:
    for article in news[:5]:  # 显示前5条
        print(f"[{article['source']}] {article['headline']}")
        print(f"链接: {article['url']}")

# 获取特定公司新闻
from datetime import datetime, timedelta
to_date = datetime.now().strftime('%Y-%m-%d')
from_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

company_news = client.get_company_news("TSLA", from_date, to_date)
if company_news:
    for article in company_news[:3]:
        print(f"Tesla新闻: {article['headline']}")
```

### 4. 获取分析师推荐

```python
# 获取分析师推荐
recommendations = client.get_recommendation_trends("AAPL")
if recommendations:
    latest = recommendations[0]  # 最新推荐
    print(f"强烈买入: {latest['strongBuy']}")
    print(f"买入: {latest['buy']}")
    print(f"持有: {latest['hold']}")
    print(f"卖出: {latest['sell']}")
    print(f"强烈卖出: {latest['strongSell']}")

# 获取目标价格
price_target = client.get_price_target("AAPL")
if price_target:
    print(f"目标价格中位数: ${price_target['targetMedian']}")
    print(f"最高目标价: ${price_target['targetHigh']}")
    print(f"最低目标价: ${price_target['targetLow']}")
```

## 实用技巧

### 1. API频率限制管理

```python
import time

# Alpha Vantage: 每分钟5次调用
def safe_alpha_vantage_call(client, func, *args, **kwargs):
    result = func(*args, **kwargs)
    time.sleep(12)  # 等待12秒避免限制
    return result

# Finnhub: 每分钟60次调用
def safe_finnhub_call(client, func, *args, **kwargs):
    result = func(*args, **kwargs)
    time.sleep(1)   # 等待1秒
    return result
```

### 2. 错误处理

```python
def get_stock_data_safely(symbol):
    """安全获取股票数据，包含错误处理"""
    try:
        # Alpha Vantage
        av_client = AlphaVantageClient()
        quote_data = av_client.get_quote(symbol)
        
        if not quote_data or 'Global Quote' not in quote_data:
            print(f"无法获取 {symbol} 的Alpha Vantage数据")
            return None
        
        # Finnhub
        fh_client = FinnhubClient()
        profile = fh_client.get_company_profile(symbol)
        
        if not profile:
            print(f"无法获取 {symbol} 的Finnhub数据")
        
        return {
            'alphavantage': quote_data,
            'finnhub': profile
        }
        
    except Exception as e:
        print(f"获取 {symbol} 数据时出错: {e}")
        return None
```

### 3. 数据整合示例

```python
def get_comprehensive_analysis(symbol):
    """获取综合分析数据"""
    av_client = AlphaVantageClient()
    fh_client = FinnhubClient()
    
    analysis = {}
    
    # Alpha Vantage 数据
    av_quote = av_client.get_quote(symbol)
    if av_quote and 'Global Quote' in av_quote:
        analysis['av_price'] = float(av_quote['Global Quote']['05. price'])
    
    time.sleep(12)  # API限制
    
    av_overview = av_client.get_company_overview(symbol)
    if av_overview:
        analysis['market_cap'] = av_overview.get('MarketCapitalization')
        analysis['pe_ratio'] = av_overview.get('PERatio')
    
    # Finnhub 数据
    fh_quote = fh_client.get_quote(symbol)
    if fh_quote:
        analysis['fh_price'] = fh_quote['c']
    
    time.sleep(1)  # API限制
    
    fh_profile = fh_client.get_company_profile(symbol)
    if fh_profile:
        analysis['company_name'] = fh_profile['name']
        analysis['industry'] = fh_profile['finnhubIndustry']
    
    return analysis

# 使用示例
result = get_comprehensive_analysis("AAPL")
print(f"公司: {result.get('company_name', 'N/A')}")
print(f"行业: {result.get('industry', 'N/A')}")
print(f"Alpha Vantage价格: ${result.get('av_price', 'N/A')}")
print(f"Finnhub价格: ${result.get('fh_price', 'N/A')}")
```

## 常见问题解决

### 1. API调用失败
- 检查网络连接
- 确认API密钥有效
- 检查是否超出频率限制

### 2. 数据为空
- 确认股票代码正确（如AAPL而不是Apple）
- 检查市场是否开盘（实时数据）
- 尝试不同的股票代码

### 3. 超出API限制
- Alpha Vantage: 增加调用间隔到12秒以上
- Finnhub: 增加调用间隔到1秒以上
- 考虑升级到付费版本

## 运行示例程序

```bash
# 快速测试（推荐）
python test_alphavantage.py
python alphavantage_quick_demo.py

# 完整示例（注意API限制）
python alphavantage_example.py
python example_usage.py
```

## 更多资源

- [Alpha Vantage API文档](https://www.alphavantage.co/documentation/)
- [Finnhub API文档](https://finnhub.io/docs/api)
- [项目GitHub仓库](https://github.com/your-repo)

---

*最后更新: 2025年5月* 