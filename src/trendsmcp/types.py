"""Type definitions matching the Trends MCP API."""

from __future__ import annotations

from dataclasses import dataclass, field
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
    "npm",
    "steam",
]


@dataclass
class TrendsDataPoint:
    date: str
    value: float
    volume: Optional[float]
    keyword: str
    source: Optional[str] = None
    datatype: Optional[str] = None


@dataclass
class GetTrendsParams:
    source: TrendsSource
    keyword: str
    data_mode: Optional[Literal["weekly", "daily"]] = None


GetTrendsResponse = List[TrendsDataPoint]

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
    percent_growth: List[Union[GrowthPreset, CustomGrowthPeriod]]
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
    volume_available: bool
    recent_volume: Optional[float]
    baseline_volume: Optional[float]
    volume_growth: Optional[float]
    status: Optional[str] = None
    calculation_method: Optional[str] = None
    volume_direction: Optional[str] = None


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
    "Amazon Best Sellers Top Rated",
    "App Store Top Free",
    "App Store Top Paid",
    "Google News RSS",
    "Google Play",
    "Google Trends",
    "Reddit Hot Posts",
    "Reddit World News",
    "SimilarWeb Top Websites",
    "Spotify Top Podcasts",
    "TikTok Trending Hashtags",
    "Wikipedia Trending",
    "X (Twitter)",
]


@dataclass
class GetTopTrendsParams:
    type: Optional[TopTrendsFeed] = None
    limit: Optional[int] = None


@dataclass
class GetTopTrendsResponse:
    as_of_ts: str
    type: str
    limit: int
    count: int
    data: List[tuple]
