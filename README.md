# trendsmcp

[![PyPI version](https://img.shields.io/pypi/v/trendsmcp.svg)](https://pypi.org/project/trendsmcp/)
[![Python versions](https://img.shields.io/pypi/pyversions/trendsmcp.svg)](https://pypi.org/project/trendsmcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/trendsmcp/trendsmcp-py/blob/main/LICENSE)

The number one Python client for live keyword trend data. Time series and growth percentages from Google Search, YouTube, Reddit, Amazon, TikTok, Wikipedia, npm, Steam, and more. One API key. No scraping. No proxies. No 429 errors.

Works as a **Python API client** in any script, notebook, or pipeline. Also works as an **MCP tool** — plug it directly into Claude, Cursor, VS Code Copilot, or any MCP-compatible AI host.

Powered by [trendsmcp.ai](https://trendsmcp.ai).

**[Get a free API key](https://trendsmcp.ai)** — 100 requests/month, no credit card.

**[Full API docs](https://trendsmcp.ai/docs)**

---

## Requirements

Python 3.8 or later. Depends on `httpx`.

---

## Install

```bash
pip install trendsmcp
```

---

## Connect

Store your API key in an environment variable:

```bash
export TRENDSMCP_API_KEY="your-api-key"
```

```python
import os
from trendsmcp import TrendsMcpClient

client = TrendsMcpClient(api_key=os.environ["TRENDSMCP_API_KEY"])
```

Get your key at [trendsmcp.ai](https://trendsmcp.ai).

---

## get_trends

Returns a weekly time series for a keyword. Default is 5 years of weekly data. Pass `data_mode="daily"` for the last 30 days at daily granularity.

```python
import os
from trendsmcp import TrendsMcpClient

client = TrendsMcpClient(api_key=os.environ["TRENDSMCP_API_KEY"])

series = client.get_trends(source="google search", keyword="bitcoin")

print(series[0])
# TrendsDataPoint(date='2021-01-03', value=12, volume=None, keyword='bitcoin', source='google search')

print(series[-1])
# TrendsDataPoint(date='2026-03-23', value=47, volume=None, keyword='bitcoin', source='google search')

# Daily granularity
series = client.get_trends(source="youtube", keyword="bitcoin", data_mode="daily")
```

**Parameters**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `source` | str | Yes | Data source (see supported sources below) |
| `keyword` | str | Yes | Keyword to query |
| `data_mode` | str | No | `"weekly"` (default) or `"daily"` |

**Response fields**

| Field | Type | Description |
|---|---|---|
| `date` | str | ISO date string |
| `value` | float | Normalized value 0 to 100 |
| `volume` | float or None | Absolute volume estimate where available |
| `keyword` | str | The keyword queried |
| `source` | str | The data source |

---

## get_growth

Returns period-over-period growth percentages for a keyword.

```python
growth = client.get_growth(
    source="google search",
    keyword="bitcoin",
    percent_growth=["3M", "12M", "YTD"],
)

for r in growth.results:
    print(f"{r.period}: {r.growth:+.1f}% ({r.direction})")
# 3M: +8.2% (increase)
# 12M: +31.4% (increase)
# YTD: +14.5% (increase)
```

**Growth presets:** `7D` `14D` `30D` `1M` `2M` `3M` `6M` `9M` `12M` `1Y` `18M` `24M` `2Y` `36M` `3Y` `48M` `60M` `5Y` `MTD` `QTD` `YTD`

Custom date ranges:

```python
from trendsmcp import TrendsMcpClient, CustomGrowthPeriod
import os

client = TrendsMcpClient(api_key=os.environ["TRENDSMCP_API_KEY"])

growth = client.get_growth(
    source="amazon",
    keyword="air fryer",
    percent_growth=[
        CustomGrowthPeriod(name="holiday lift", recent="2025-12-31", baseline="2025-10-01")
    ],
)
```

---

## get_top_trends

Returns today's live trending items from platform feeds. Omit `type` to get all feeds at once.

```python
trending = client.get_top_trends(type="Google Trends", limit=10)
print(trending.data)
# [[1, 'tiger woods'], [2, 'miley cyrus'], ...]

# All feeds at once
all_feeds = client.get_top_trends()
```

**Available feeds:** `Google Trends` `YouTube` `TikTok Trending Hashtags` `Reddit Hot Posts` `Amazon Best Sellers Top Rated` `App Store Top Free` `App Store Top Paid` `Wikipedia Trending` `Spotify Top Podcasts` `X (Twitter)`

---

## Async

All three methods are available on `AsyncTrendsMcpClient`. Run multiple platform queries concurrently:

```python
import asyncio
import os
from trendsmcp import AsyncTrendsMcpClient

async def main():
    client = AsyncTrendsMcpClient(api_key=os.environ["TRENDSMCP_API_KEY"])

    google, youtube, reddit = await asyncio.gather(
        client.get_trends(source="google search", keyword="AI"),
        client.get_trends(source="youtube", keyword="AI"),
        client.get_trends(source="reddit", keyword="AI"),
    )
    print(f"Google: {google[-1].value}  YouTube: {youtube[-1].value}  Reddit: {reddit[-1].value}")

asyncio.run(main())
```

---

## Error handling

```python
from trendsmcp import TrendsMcpClient, TrendsMcpError
import os

client = TrendsMcpClient(api_key=os.environ["TRENDSMCP_API_KEY"])

try:
    series = client.get_trends(source="google search", keyword="bitcoin")
except TrendsMcpError as e:
    print(e.status)   # HTTP status code, e.g. 429
    print(e.code)     # Machine-readable code, e.g. "rate_limited"
    print(e.message)  # Human-readable message
```

---

## Use with Pandas

```python
import pandas as pd
import os
from trendsmcp import TrendsMcpClient

client = TrendsMcpClient(api_key=os.environ["TRENDSMCP_API_KEY"])
series = client.get_trends(source="google search", keyword="bitcoin")
df = pd.DataFrame([vars(p) for p in series])
print(df.tail())
```

---

## Supported sources

| source | What it measures |
|---|---|
| `"google search"` | Google Search volume |
| `"google images"` | Google Images search volume |
| `"google news"` | Google News search volume |
| `"google shopping"` | Google Shopping purchase intent |
| `"youtube"` | YouTube search volume |
| `"tiktok"` | TikTok hashtag volume |
| `"reddit"` | Reddit mention and discussion volume |
| `"amazon"` | Amazon product search volume |
| `"wikipedia"` | Wikipedia page views |
| `"news volume"` | News article mention count |
| `"news sentiment"` | News sentiment score (positive / negative) |
| `"npm"` | npm package weekly downloads |
| `"steam"` | Steam concurrent player count |

All values are normalized 0 to 100 so you can compare across sources directly. See [trendsmcp.ai/docs](https://trendsmcp.ai/docs) for the full and always up-to-date source list.

---

## Why not pytrends?

pytrends scrapes Google and has been archived since 2023. It breaks regularly, returns 429 errors, requires proxies, and only covers Google Search with relative scores. No absolute volume. No other platforms.

trendsmcp is a managed REST API. One key, all sources, no scraping, no 429s, actively maintained.

---

## Related packages

Platform-specific packages that expose the same client with a pre-set `SOURCE` constant:

- [youtube-trends-api](https://pypi.org/project/youtube-trends-api/) / [youtube-trends-mcp](https://pypi.org/project/youtube-trends-mcp/)
- [reddit-trends-api](https://pypi.org/project/reddit-trends-api/) / [reddit-trends-mcp](https://pypi.org/project/reddit-trends-mcp/)
- [google-search-trends-api](https://pypi.org/project/google-search-trends-api/) / [google-search-trends-mcp](https://pypi.org/project/google-search-trends-mcp/)
- [amazon-trends-api](https://pypi.org/project/amazon-trends-api/) / [amazon-trends-mcp](https://pypi.org/project/amazon-trends-mcp/)
- [tiktok-trends-api](https://pypi.org/project/tiktok-trends-api/) / [tiktok-trends-mcp](https://pypi.org/project/tiktok-trends-mcp/)
- [wikipedia-trends-api](https://pypi.org/project/wikipedia-trends-api/) / [wikipedia-trends-mcp](https://pypi.org/project/wikipedia-trends-mcp/)
- [npm-trends-api](https://pypi.org/project/npm-trends-api/) / [npm-trends-mcp](https://pypi.org/project/npm-trends-mcp/)
- [steam-trends-api](https://pypi.org/project/steam-trends-api/) / [steam-trends-mcp](https://pypi.org/project/steam-trends-mcp/)
- [app-store-trends-api](https://pypi.org/project/app-store-trends-api/) / [app-store-trends-mcp](https://pypi.org/project/app-store-trends-mcp/)
- [news-volume-api](https://pypi.org/project/news-volume-api/) / [news-volume-mcp](https://pypi.org/project/news-volume-mcp/)
- [news-sentiment-api](https://pypi.org/project/news-sentiment-api/) / [news-sentiment-mcp](https://pypi.org/project/news-sentiment-mcp/)

---

## License

MIT
