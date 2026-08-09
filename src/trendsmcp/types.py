"""Type definitions matching the Trends MCP API (docs.trendsmcp.ai / llms.txt)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Literal, Optional, Union


TrendsSource = Literal[
    "google search",
    "google images",
    "google news",
    "google shopping",
    "youtube",
    "tiktok",
    "reddit",
    "amazon",
    "wikipedia",
    "news volume",
    "news sentiment",
    "app downloads",
    "app rankings",
    "npm",
    "steam",
]


@dataclass
class TrendsDataPoint:
    date: str
    value: float
    keyword: str
    # Present for some sources (npm, app downloads, steam, …); omitted for others (e.g. google search).
    volume: Optional[float] = None
    source: Optional[str] = None
    datatype: Optional[str] = None
    volume_cumulative: Optional[float] = None


@dataclass
class GetTrendsParams:
    source: TrendsSource
    keyword: str
    data_mode: Optional[Literal["weekly", "daily"]] = None


# Alias used in docs / npm client
GetTimeSeriesParams = GetTrendsParams
GetTrendsResponse = List[TrendsDataPoint]
GetTimeSeriesResponse = GetTrendsResponse

GrowthPreset = Literal[
    "7D", "14D", "30D",
    "1M", "2M", "3M", "6M", "9M", "12M",
    "1Y", "18M", "24M", "2Y", "36M", "3Y", "48M", "60M", "5Y",
    "MTD", "QTD", "YTD",
]


@dataclass
class CustomGrowthPeriod:
    recent: str
    baseline: str
    name: Optional[str] = None


@dataclass
class GetGrowthParams:
    source: TrendsSource
    keyword: str
    percent_growth: Optional[List[Union[GrowthPreset, CustomGrowthPeriod]]] = None
    data_mode: Optional[Literal["weekly", "daily"]] = None


@dataclass
class GrowthResult:
    period: str
    growth: float
    direction: Literal["increase", "decrease"]
    recent_date: str
    baseline_date: str
    recent_value: float
    baseline_value: float
    volume_available: bool = False
    recent_volume: Optional[float] = None
    baseline_volume: Optional[float] = None
    volume_growth: Optional[float] = None
    status: Optional[str] = None
    calculation_method: Optional[str] = None
    growth_unit: Optional[str] = None
    volume_estimated: Optional[bool] = None
    volume_direction: Optional[str] = None
    volume_growth_omitted_reason: Optional[str] = None


@dataclass
class GrowthMetadata:
    total_data_points: int
    calculations_completed: int
    all_successful: bool


@dataclass
class GetGrowthResponse:
    search_term: str
    data_source: str
    results: List[GrowthResult]
    metadata: GrowthMetadata


TopTrendsFeed = Literal[
    "Google Trends",
    "Google News Top News",
    "TikTok Trending Hashtags",
    "TikTok Trending Searches",
    "TikTok Shop Hot Products",
    "YouTube Trending",
    "X (Twitter) Trending",
    "Reddit Hot Posts",
    "Reddit World News",
    "Wikipedia Trending",
    "Amazon Best Sellers Top Rated",
    "Amazon Best Sellers by Category",
    "App Store Top Free",
    "App Store Top Paid",
    "Google Play",
    "Top Websites",
    "Spotify Top Podcasts",
    "Steam Most Played",
    "GitHub Trending Repos",
    "IMDb MOVIEmeter",
    "Open Library Trending Books",
]


@dataclass
class GetTopTrendsParams:
    type: Optional[TopTrendsFeed] = None
    category: Optional[str] = None
    limit: Optional[int] = None
    offset: Optional[int] = None


@dataclass
class GetTopTrendsResponse:
    as_of_ts: str
    type: str
    limit: int
    count: int
    data: List[tuple]
    offset: Optional[int] = None
