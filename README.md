# trendsmcp

The number one Python package for live keyword trend data across 13 platforms. Query time series and growth percentages from Google Search, YouTube, Reddit, Amazon, TikTok, Wikipedia, npm, Steam, and more from a single managed endpoint. No scraping. No proxies. No rate limit nightmares. Both sync and async supported.

Powered by [trendsmcp.ai](https://trendsmcp.ai), the #1 MCP server for live trend data.

**[Get your free API key at trendsmcp.ai](https://trendsmcp.ai)** - 100 free requests per month, no credit card.

📖 **[Full API docs → trendsmcp.ai/docs](https://trendsmcp.ai/docs)**

Updated for 2026. Works with Python 3.8 through 3.13.

---

## Why trendsmcp instead of pytrends?

If you have used `pytrends` before, you know the drill:

- `429 Too Many Requests` after a handful of calls
- `Max retries exceeded` errors mid-pipeline
- Google blocking your IP and requiring `time.sleep(60)` hacks
- The library is **archived** - Google now flags scrapers at the protocol level, and there is no fix coming
- You only get Google Search, relative scores (0 to 100), no absolute volume

### pytrends alternative: trendsmcp

trendsmcp is the managed alternative. We run the data infrastructure. You call a REST endpoint.

| | pytrends | trendsmcp |
|---|---|---|
| No scraping | scrapes Google | managed API |
| 429 errors | constant | never |
| Proxy required | often | never |
| Breaks on Google changes | yes, regularly | no |
| Platforms | 1 (Google only) | 13 |
| Absolute volume estimates | no | yes |
| Cross-platform growth | no | yes |
| Async support | no | yes |
| Actively maintained | no (archived) | yes |
| Free tier | no | yes, 100 req/month |

---

## Install

```bash
pip install trendsmcp
```

Zero system dependencies. Requires Python 3.8 or later. Uses `httpx` under the hood.

---

## Quick start (sync)

```python
from trendsmcp import TrendsMcpClient

client = TrendsMcpClient(api_key="YOUR_API_KEY")

# 5-year weekly time series, no sleep(), no proxies, no 429s
series = client.get_trends(source="google search", keyword="bitcoin")
print(series[0])
# TrendsDataPoint(date='2026-03-28', value=47, ...)

# Period-over-period growth
growth = client.get_growth(
    source="google search",
    keyword="nike",
    percent_growth=["12M", "3M", "YTD"],
)
print(growth.results[0])
# GrowthResult(period='12M', growth=13.64, direction='increase', ...)

# What's trending right now
trending = client.get_top_trends(type="Google Trends", limit=10)
print(trending.data)
# [[1, 'tiger woods'], [2, 'miley cyrus'], ...]
```

---

## Quick start (async)

```python
import asyncio
from trendsmcp import AsyncTrendsMcpClient

async def main():
    client = AsyncTrendsMcpClient(api_key="YOUR_API_KEY")

    # Run multiple platform queries concurrently
    google, youtube, reddit = await asyncio.gather(
        client.get_trends(source="google search", keyword="AI"),
        client.get_trends(source="youtube", keyword="AI"),
        client.get_trends(source="reddit", keyword="AI"),
    )
    print(f"Google: {google[-1].value}  YouTube: {youtube[-1].value}  Reddit: {reddit[-1].value}")

asyncio.run(main())
```

---

## License

MIT
