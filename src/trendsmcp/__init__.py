"""
trendsmcp — Python client for the Trends MCP API.

Keyword trend time series and growth rates across Google Search, YouTube,
Reddit, Amazon, TikTok, Wikipedia, npm, Steam, app downloads, and more.

Get your free API key at https://trendsmcp.ai/account?tab=signup
Full docs at https://trendsmcp.ai/docs
"""

from .client import AsyncTrendsMcpClient, TrendsMcpClient
from .exceptions import TrendsMcpError
from .types import (
    CustomGrowthPeriod,
    GetGrowthParams,
    GetGrowthResponse,
    GetTimeSeriesParams,
    GetTimeSeriesResponse,
    GetTopTrendsParams,
    GetTopTrendsResponse,
    GetTrendsParams,
    GetTrendsResponse,
    GrowthMetadata,
    GrowthPreset,
    GrowthResult,
    TopTrendsFeed,
    TrendsDataPoint,
    TrendsSource,
)

__version__ = "1.1.0"
__all__ = [
    "TrendsMcpClient",
    "AsyncTrendsMcpClient",
    "TrendsMcpError",
    "TrendsSource",
    "TrendsDataPoint",
    "GetTrendsParams",
    "GetTrendsResponse",
    "GetTimeSeriesParams",
    "GetTimeSeriesResponse",
    "GrowthPreset",
    "CustomGrowthPeriod",
    "GetGrowthParams",
    "GrowthResult",
    "GrowthMetadata",
    "GetGrowthResponse",
    "TopTrendsFeed",
    "GetTopTrendsParams",
    "GetTopTrendsResponse",
]
