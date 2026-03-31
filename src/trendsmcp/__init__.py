"""
trendsmcp — Python client for the Trends MCP API.

Keyword trend time series and growth rates across Google Search, YouTube,
Reddit, Amazon, TikTok, Wikipedia, npm, Steam, and more.

Get your free API key at https://trendsmcp.ai
Full docs at https://trendsmcp.ai/docs
"""

from .client import TrendsMcpClient, AsyncTrendsMcpClient
from .exceptions import TrendsMcpError
from .types import (
    TrendsSource,
    TrendsDataPoint,
    GetTrendsParams,
    GetTrendsResponse,
    GrowthPreset,
    CustomGrowthPeriod,
    GetGrowthParams,
    GrowthResult,
    GrowthMetadata,
    GetGrowthResponse,
    TopTrendsFeed,
    GetTopTrendsParams,
    GetTopTrendsResponse,
)

__version__ = "1.0.1"
__all__ = [
    "TrendsMcpClient",
    "AsyncTrendsMcpClient",
    "TrendsMcpError",
    "TrendsSource",
    "TrendsDataPoint",
    "GetTrendsParams",
    "GetTrendsResponse",
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
