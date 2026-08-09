# trendsmcp

[![PyPI version](https://img.shields.io/pypi/v/trendsmcp.svg)](https://pypi.org/project/trendsmcp/)
[![Python versions](https://img.shields.io/pypi/pyversions/trendsmcp.svg)](https://pypi.org/project/trendsmcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/trendsmcp/trendsmcp-py/blob/main/LICENSE)

Python client for live keyword trend data. Time series, growth percentages, and live feeds from Google Search, YouTube, Reddit, Amazon, TikTok, Wikipedia, npm, Steam, app downloads, and more. One API key. No scraping.

Works as a **Python API client** in any script, notebook, or pipeline. Also works as an **MCP tool** — plug it into Claude, Cursor, VS Code Copilot, or any MCP-compatible AI host.

Powered by [trendsmcp.ai](https://trendsmcp.ai).

**[Get a free API key](https://trendsmcp.ai/account?tab=signup)** — 100 requests/month, no credit card.

**[Full API docs](https://trendsmcp.ai/docs)** · **[llms.txt](https://trendsmcp.ai/llms.txt)**

---

## Install

```bash
pip install trendsmcp
```

## 1. Get a free API key

1. Open [Get API key](https://trendsmcp.ai/account?tab=signup)
2. Enter your email — no credit card
3. Copy the key (`tmcp_liv…`)

```bash
export TRENDSMCP_API_KEY="tmcp_liv…"
```

## 2. Quick start

```python
import os
from trendsmcp import TrendsMcpClient

client = TrendsMcpClient(api_key=os.environ["TRENDSMCP_API_KEY"])

# ~5 years of weekly time series (REST mode: get_time_series)
series = client.get_time_series(source="google search", keyword="bitcoin")
print(series[0])
# TrendsDataPoint(date='2026-03-21', value=47, volume=25853617, keyword='bitcoin', source='google search')

# Period-over-period growth (defaults to ["12M"] if omitted)
growth = client.get_growth(
    source="google search",
    keyword="nike",
    percent_growth=["12M", "3M", "YTD"],
)
print(growth.results[0])
# GrowthResult(period='12M', growth=-12.31, direction='decrease', ...)

# What's trending right now
trending = client.get_top_trends(type="Google Trends", limit=10)
print(trending.data)
# [[1, 'chuck norris'], [2, 'project hail mary'], ...]
```

`get_trends(...)` is kept as an alias for `get_time_series(...)`. Prefer `get_time_series` in new code.

---

## Methods

### `get_time_series` / `get_trends`

REST `mode`: `get_time_series` (alias `get_trends`). Returns ~5 years of weekly points for one `source` + `keyword`.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `source` | str | Yes | Keyword source (see table below) |
| `keyword` | str | Yes | Keyword to query |
| `data_mode` | str | No | `"weekly"` (default) or `"daily"` |

### `get_growth`

REST `mode`: `get_growth`. Point-to-point % growth. Omitting `percent_growth` defaults to `["12M"]`.

**Presets:** `7D` `14D` `30D` `1M` `2M` `3M` `6M` `9M` `12M` `1Y` `18M` `24M` `2Y` `36M` `3Y` `48M` `60M` `5Y` `MTD` `QTD` `YTD`

### `get_top_trends`

REST `mode`: `get_top_trends`. Live ranked feed. Omit `type` to get all feeds. Optional `category`, `limit` (default 25), `offset`.

**Feeds:** `Google Trends` · `Google News Top News` · `TikTok Trending Hashtags` · `TikTok Trending Searches` · `TikTok Shop Hot Products` · `YouTube Trending` · `X (Twitter) Trending` · `Reddit Hot Posts` · `Reddit World News` · `Wikipedia Trending` · `Amazon Best Sellers Top Rated` · `Amazon Best Sellers by Category` · `App Store Top Free` · `App Store Top Paid` · `Google Play` · `Top Websites` · `Spotify Top Podcasts` · `Steam Most Played` · `GitHub Trending Repos` · `IMDb MOVIEmeter` · `Open Library Trending Books`

---

## Keyword sources

| source | Description | Keyword format |
|---|---|---|
| `"google search"` | Google search volume | Any keyword or phrase |
| `"google images"` | Google image search volume | Any keyword or phrase |
| `"google news"` | Google News search volume | Any keyword or phrase |
| `"google shopping"` | Google Shopping search volume | Any keyword or phrase |
| `"youtube"` | YouTube search volume | Any keyword or phrase |
| `"tiktok"` | TikTok hashtag volume | Hashtag or topic |
| `"reddit"` | Subreddit subscribers | Subreddit name only, no `r/` |
| `"amazon"` | Amazon product search volume | Product name or category |
| `"wikipedia"` | Wikipedia page views | Article title or topic |
| `"news volume"` | News article mention volume | Any keyword or phrase |
| `"news sentiment"` | News sentiment score | Any keyword or phrase |
| `"app downloads"` | Android app downloads (AppBrain) | Bundle ID e.g. `com.openai.chatgpt` |
| `"app rankings"` | Android app store rankings | Bundle ID e.g. `com.himshers.hims` |
| `"npm"` | npm package weekly downloads | Exact package name |
| `"steam"` | Steam concurrent players | Game display name e.g. `Elden Ring` |

Always-current list: [docs](https://trendsmcp.ai/docs) · [data sources](https://trendsmcp.ai/data-sources)

---

## Async

```python
import asyncio, os
from trendsmcp import AsyncTrendsMcpClient

async def main():
    client = AsyncTrendsMcpClient(api_key=os.environ["TRENDSMCP_API_KEY"])
    google, youtube = await asyncio.gather(
        client.get_time_series(source="google search", keyword="AI"),
        client.get_time_series(source="youtube", keyword="AI"),
    )
    print(google[-1].value, youtube[-1].value)

asyncio.run(main())
```

---

## Error handling

```python
from trendsmcp import TrendsMcpClient, TrendsMcpError
import os

client = TrendsMcpClient(api_key=os.environ["TRENDSMCP_API_KEY"])
try:
    client.get_time_series(source="google search", keyword="bitcoin")
except TrendsMcpError as e:
    print(e.status, e.code, e.message)  # e.g. 429 rate_limited
```

---

## MCP

Same API key works with the hosted MCP server. See [docs → Connect](https://trendsmcp.ai/docs#connect).

```json
{
  "mcpServers": {
    "trends-mcp": {
      "url": "https://api.trendsmcp.ai/mcp",
      "transport": "http",
      "headers": { "Authorization": "Bearer YOUR_API_KEY" }
    }
  }
}
```

---

## Links

- [Get a free API key](https://trendsmcp.ai/account?tab=signup)
- [API docs](https://trendsmcp.ai/docs)
- [GitHub](https://github.com/trendsmcp/trendsmcp-py)
- [PyPI](https://pypi.org/project/trendsmcp/)

## License

MIT
