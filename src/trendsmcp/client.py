"""Trends MCP API client — sync and async."""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional, Union

import httpx

from .exceptions import TrendsMcpError
from .types import (
    CustomGrowthPeriod,
    GetGrowthParams,
    GetGrowthResponse,
    GetTopTrendsParams,
    GetTopTrendsResponse,
    GetTrendsParams,
    GetTrendsResponse,
    GrowthMetadata,
    GrowthResult,
    TrendsDataPoint,
)

BASE_URL = "https://api.trendsmcp.ai/api"


def _parse_error(status: int, body: Any) -> TrendsMcpError:
    if isinstance(body, dict):
        return TrendsMcpError(status, body.get("error", str(status)), body.get("message", "Unknown error"))
    return TrendsMcpError(status, str(status), str(body))


def _unwrap(raw: Any, status: int) -> Any:
    """Unwrap Lambda proxy envelope { statusCode, body: '<json>' } when present."""
    if (
        isinstance(raw, dict)
        and isinstance(raw.get("statusCode"), int)
        and isinstance(raw.get("body"), str)
    ):
        parsed = json.loads(raw["body"])
        if raw["statusCode"] >= 400:
            raise _parse_error(raw["statusCode"], parsed)
        return parsed
    if status >= 400:
        raise _parse_error(status, raw)
    return raw


def _build_growth_period(p: Union[str, CustomGrowthPeriod]) -> Any:
    if isinstance(p, str):
        return p
    d: Dict[str, str] = {"recent": p.recent, "baseline": p.baseline}
    if p.name:
        d["name"] = p.name
    return d


def _parse_trends(data: List[Dict]) -> GetTrendsResponse:
    return [TrendsDataPoint(**dp) for dp in data]


def _parse_growth(data: Dict) -> GetGrowthResponse:
    results = [GrowthResult(**r) for r in data["results"]]
    metadata = GrowthMetadata(**data["metadata"])
    return GetGrowthResponse(
        search_term=data["search_term"],
        data_source=data["data_source"],
        results=results,
        metadata=metadata,
    )


def _parse_top_trends(data: Dict) -> GetTopTrendsResponse:
    return GetTopTrendsResponse(
        as_of_ts=data["as_of_ts"],
        type=data["type"],
        limit=data["limit"],
        count=data["count"],
        data=data["data"],
    )


class TrendsMcpClient:
    """Synchronous Trends MCP API client.

    Get your free API key at https://trendsmcp.ai
    Full docs at https://trendsmcp.ai/docs

    Example::

        from trendsmcp import TrendsMcpClient

        client = TrendsMcpClient(api_key="YOUR_API_KEY")

        series = client.get_trends(source="youtube", keyword="asmr")
        growth = client.get_growth(source="reddit", keyword="AI agents", percent_growth=["3M", "1Y"])
        trending = client.get_top_trends(type="Google Trends", limit=10)
    """

    def __init__(self, api_key: str, base_url: str = BASE_URL, timeout: float = 30.0) -> None:
        if not api_key:
            raise ValueError(
                "TrendsMcpClient: api_key is required. Get a free key at https://trendsmcp.ai"
            )
        self._headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout

    def _post(self, body: Dict) -> Any:
        with httpx.Client(timeout=self._timeout) as client:
            resp = client.post(self._base_url, json=body, headers=self._headers)
        return _unwrap(resp.json(), resp.status_code)

    def get_trends(
        self,
        source: str,
        keyword: str,
        data_mode: Optional[str] = None,
    ) -> GetTrendsResponse:
        """Return a historical time series for a keyword.

        Defaults to 5 years of weekly data. Set ``data_mode="daily"`` for the
        last 30 days at daily granularity.
        """
        body: Dict = {"source": source, "keyword": keyword}
        if data_mode:
            body["data_mode"] = data_mode
        return _parse_trends(self._post(body))

    def get_growth(
        self,
        source: str,
        keyword: str,
        percent_growth: List[Union[str, CustomGrowthPeriod]],
        data_mode: Optional[str] = None,
    ) -> GetGrowthResponse:
        """Calculate period-over-period growth for a keyword."""
        body: Dict = {
            "source": source,
            "keyword": keyword,
            "percent_growth": [_build_growth_period(p) for p in percent_growth],
        }
        if data_mode:
            body["data_mode"] = data_mode
        return _parse_growth(self._post(body))

    def get_top_trends(
        self,
        type: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> GetTopTrendsResponse:
        """Return today's live trending items from platform feeds."""
        body: Dict = {"mode": "top_trends"}
        if type:
            body["type"] = type
        if limit:
            body["limit"] = limit
        return _parse_top_trends(self._post(body))


class AsyncTrendsMcpClient:
    """Async Trends MCP API client (requires ``await``)."""

    def __init__(self, api_key: str, base_url: str = BASE_URL, timeout: float = 30.0) -> None:
        if not api_key:
            raise ValueError(
                "AsyncTrendsMcpClient: api_key is required. Get a free key at https://trendsmcp.ai"
            )
        self._headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout

    async def _post(self, body: Dict) -> Any:
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            resp = await client.post(self._base_url, json=body, headers=self._headers)
        return _unwrap(resp.json(), resp.status_code)

    async def get_trends(
        self,
        source: str,
        keyword: str,
        data_mode: Optional[str] = None,
    ) -> GetTrendsResponse:
        """Async version of get_trends."""
        body: Dict = {"source": source, "keyword": keyword}
        if data_mode:
            body["data_mode"] = data_mode
        return _parse_trends(await self._post(body))

    async def get_growth(
        self,
        source: str,
        keyword: str,
        percent_growth: List[Union[str, CustomGrowthPeriod]],
        data_mode: Optional[str] = None,
    ) -> GetGrowthResponse:
        """Async version of get_growth."""
        body: Dict = {
            "source": source,
            "keyword": keyword,
            "percent_growth": [_build_growth_period(p) for p in percent_growth],
        }
        if data_mode:
            body["data_mode"] = data_mode
        return _parse_growth(await self._post(body))

    async def get_top_trends(
        self,
        type: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> GetTopTrendsResponse:
        """Async version of get_top_trends."""
        body: Dict = {"mode": "top_trends"}
        if type:
            body["type"] = type
        if limit:
            body["limit"] = limit
        return _parse_top_trends(await self._post(body))
