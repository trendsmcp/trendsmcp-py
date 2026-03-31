# trendsmcp

Python client for the Trends MCP API. Get live keyword trend data across 13 platforms: Google Search, YouTube, Reddit, Amazon, TikTok, Wikipedia, npm, Steam, and more. One API key, one client, no scraping, no proxies, no 429 errors.

Powered by [trendsmcp.ai](https://trendsmcp.ai).

**[Get a free API key](https://trendsmcp.ai)** - 100 requests/month, no credit card.

**[Full API docs](https://trendsmcp.ai/docs)**

Works with Python 3.8 through 3.13.

---

## Install

```bash
pip install trendsmcp
```

---

## Connect

```python
from trendsmcp import TrendsMcpClient

client = TrendsMcpClient(api_key="YOUR_API_KEY")
```

Get your key at [trendsmcp.ai](https://trendsmcp.ai).

---

## get_trends

Returns a weekly time series for a keyword (5 years by default). Pass `data_mode="daily"` for the last 30 days at daily granularity.

```python
series = client.get_trends(source="google search", keyword="bitcoin")

print(series[0])
# TrendsDataPoint(date='2021-01-03', value=12, volume=None, keyword='bitcoin', source='google search')

print(series[-1])
# TrendsDataPoint(date='2026-03-23', value=47, volume=None, keyword='bitcoin', source='google search')

# Daily granularity
series = client.get_trends(source="youtube", keyword="bitcoin", data_mode="daily")
```

**Parameters**

| Parameter | Type | Description |
|---|---|---|
| `source` | str | Data source (see full list below) |
| `keyword` | str | Keyword to look up |
| `data_mode` | str | `"weekly"` (default) or `"daily"` |

**Returns** a list of `TrendsDataPoint` objects:

| Field | Type | Description |
|---|---|---|
| `date` | str | ISO date string |
| `value` | float | Normalized value 0-100 |
| `volume` | float or None | Absolute volume estimate where available |
| `keyword` | str | The keyword queried |
| `source` | str | The data source |

---

## get_growth

Returns period-over-period growth for a keyword. Pass preset strings or custom date pairs.

```python
growth = client.get_growth(
    source="google search",
    keyword="nike",
    percent_growth=["3M", "12M", "YTD"],
)

print(growth.results[0])
# GrowthResult(period='3M', growth=14.5, direction='increase', ...)

for r in growth.results:
    print(f"{r.period}: {r.growth:+.1f}% ({r.direction})")
```

**Growth presets:** `7D` `14D` `30D` `1M` `2M` `3M` `6M` `9M` `12M` `1Y` `18M` `24M` `2Y` `36M` `3Y` `48M` `60M` `5Y` `MTD` `QTD` `YTD`

**Custom date ranges:**

```python
from trendsmcp import TrendsMcpClient, CustomGrowthPeriod

growth = client.get_growth(
    source="amazon",
    keyword="air fryer",
    percent_growth=[
        CustomGrowthPeriod(name="holiday lift", recent="2025-12-31", baseline="2025-10-01")
    ],
)
```

**Parameters**

| Parameter | Type | Description |
|---|---|---|
| `source` | str | Data source |
| `keyword` | str | Keyword to look up |
| `percent_growth` | list | List of preset strings or `CustomGrowthPeriod` objects |
| `data_mode` | str | `"weekly"` (default) or `"daily"` |

---

## get_top_trends

Returns today's live trending items from platform feeds. Omit `type` to get all feeds at once.

```python
# Single feed
trending = client.get_top_trends(type="Google Trends", limit=10)
print(trending.data)
# [[1, 'tiger woods'], [2, 'miley cyrus'], ...]

# All feeds at once
all_trending = client.get_top_trends()
```

**Available feeds:** `Google Trends` `YouTube` `TikTok Trending Hashtags` `Reddit Hot Posts` `Amazon Best Sellers Top Rated` `App Store Top Free` `App Store Top Paid` `Wikipedia Trending` `Spotify Top Podcasts` `X (Twitter)`

**Parameters**

| Parameter | Type | Description |
|---|---|---|
| `type` | str | Feed name (omit for all feeds) |
| `limit` | int | Max items per feed, up to 200 (default 50) |

---

## Async support

```python
import asyncio
from trendsmcp import AsyncTrendsMcpClient

async def main():
    client = AsyncTrendsMcpClient(api_key="YOUR_API_KEY")

    # Run multiple platforms concurrently
    google, youtube, reddit = await asyncio.gather(
        client.get_trends(source="google search", keyword="AI"),
        client.get_trends(source="youtube", keyword="AI"),
        client.get_trends(source="reddit", keyword="AI"),
    )
    print(f"Google: {google[-1].value}  YouTube: {youtube[-1].value}  Reddit: {reddit[-1].value}")

asyncio.run(main())
```

All three methods (`get_trends`, `get_growth`, `get_top_trends`) have async equivalents on `AsyncTrendsMcpClient`.

---

## Error handling

```python
from trendsmcp import TrendsMcpClient, TrendsMcpError

client = TrendsMcpClient(api_key="YOUR_API_KEY")

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
from trendsmcp import TrendsMcpClient

client = TrendsMcpClient(api_key="YOUR_API_KEY")
series = client.get_trends(source="google search", keyword="bitcoin")
df = pd.DataFrame([vars(p) for p in series])
print(df.tail())
```

---

## All 13 supported sources

| source | What it measures |
|---|---|
| `"google search"` | Google Search volume |
| `"google images"` | Google Images search volume |
| `"google news"` | Google News search volume |
| `"google shopping"` | Google Shopping purchase intent |
| `"youtube"` | YouTube search volume |
| `"tiktok"` | TikTok hashtag volume |
| `"reddit"` | Reddit mention volume |
| `"amazon"` | Amazon product search volume |
| `"wikipedia"` | Wikipedia page views |
| `"news volume"` | News article mention count |
| `"news sentiment"` | News sentiment score |
| `"npm"` | npm package weekly downloads |
| `"steam"` | Steam concurrent player count |

All values are normalized 0 to 100 so you can compare across platforms directly.

---

## Why not pytrends?

pytrends scrapes Google and has been archived since 2023. It breaks regularly, returns 429 errors, requires proxies, and only covers Google Search with relative scores (0 to 100), no absolute volume.

trendsmcp is a managed REST API. No scraping, no 429s, no proxies required, 13 platforms, absolute volume estimates, and actively maintained.

---

## Related packages

Platform-specific packages that expose the same client with a pre-set `SOURCE` constant:

- [youtube-trends-api](https://pypi.org/project/youtube-trends-api/)
- [reddit-trends-api](https://pypi.org/project/reddit-trends-api/)
- [google-search-trends-api](https://pypi.org/project/google-search-trends-api/)
- [amazon-trends-api](https://pypi.org/project/amazon-trends-api/)
- [tiktok-trends-api](https://pypi.org/project/tiktok-trends-api/)
- [wikipedia-trends-api](https://pypi.org/project/wikipedia-trends-api/)
- [npm-trends-api](https://pypi.org/project/npm-trends-api/)
- [steam-trends-api](https://pypi.org/project/steam-trends-api/)
- [app-store-trends-api](https://pypi.org/project/app-store-trends-api/)
- [news-volume-api](https://pypi.org/project/news-volume-api/)
- [news-sentiment-api](https://pypi.org/project/news-sentiment-api/)

---

## License

MIT
