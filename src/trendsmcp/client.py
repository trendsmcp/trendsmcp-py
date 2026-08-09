"""Trends MCP API client — sync and async.

Aligned with https://trendsmcp.ai/docs and https://trendsmcp.ai/llms.txt
"""

from __future__ import annotations

import json
from dataclasses import fields
from typing import Any, Dict, List, Optional, Type, TypeVar, Union

import httpx

from .exceptions import TrendsMcpError
from .types import (
    CustomGrowthPeriod,
    GetGrowthResponse,
    GetTopTrendsResponse,
    GetTrendsResponse,
    GrowthMetadata,
    GrowthResult,
    TrendsDataPoint,
)

T = TypeVar("T")


def _from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
    """Build a dataclass, ignoring unknown API fields and filling defaults."""
    allowed = {f.name for f in fields(cls)}
    return cls(**{k: v for k, v in data.items() if k in allowed})  # type: ignore[arg-type]

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
    return [_from_dict(TrendsDataPoint, dp) for dp in data]


def _parse_growth(data: Dict) -> GetGrowthResponse:
    results = [_from_dict(GrowthResult, r) for r in data["results"]]
    metadata = _from_dict(GrowthMetadata, data["metadata"])
    return GetGrowthResponse(
        search_term=data["search_term"],
        data_source=data["data_source"],
        results=results,
        metadata=metadata,
    )


def _parse_top_trends(data: Dict) -> GetTopTrendsResponse:
    return _from_dict(GetTopTrendsResponse, data)


class TrendsMcpClient:
    """Synchronous Trends MCP API client.

    Get your free API key at https://trendsmcp.ai/account?tab=signup
    Full docs at https://trendsmcp.ai/docs

    Example::

        from trendsmcp import TrendsMcpClient

        client = TrendsMcpClient(api_key="YOUR_API_KEY")

        series = client.get_time_series(source="google search", keyword="bitcoin")
        growth = client.get_growth(source="reddit", keyword="AI agents", percent_growth=["3M", "1Y"])
        trending = client.get_top_trends(type="Google Trends", limit=10)
    """

    def __init__(self, api_key: str, base_url: str = BASE_URL, timeout: float = 30.0) -> None:
        if not api_key:
            raise ValueError(
                "TrendsMcpClient: api_key is required. Get a free key at https://trendsmcp.ai/account?tab=signup"
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

    def get_time_series(
        self,
        source: str,
        keyword: str,
        data_mode: Optional[str] = None,
    ) -> GetTrendsResponse:
        """Return ~5 years of weekly historical data for one source + keyword.

        REST mode: ``get_time_series`` (alias ``get_trends``). Prefer this in new code.
        """
        body: Dict = {"mode": "get_time_series", "source": source, "keyword": keyword}
        if data_mode:
            body["data_mode"] = data_mode
        return _parse_trends(self._post(body))

    def get_trends(
        self,
        source: str,
        keyword: str,
        data_mode: Optional[str] = None,
    ) -> GetTrendsResponse:
        """Alias for :meth:`get_time_series`. Prefer ``get_time_series`` in new code."""
        return self.get_time_series(source=source, keyword=keyword, data_mode=data_mode)

    def get_growth(
        self,
        source: str,
        keyword: str,
        percent_growth: Optional[List[Union[str, CustomGrowthPeriod]]] = None,
        data_mode: Optional[str] = None,
    ) -> GetGrowthResponse:
        """Calculate period-over-period growth. Omitting ``percent_growth`` defaults to ``["12M"]``."""
        body: Dict = {"mode": "get_growth", "source": source, "keyword": keyword}
        if percent_growth is not None:
            body["percent_growth"] = [_build_growth_period(p) for p in percent_growth]
        if data_mode:
            body["data_mode"] = data_mode
        return _parse_growth(self._post(body))

    def get_top_trends(
        self,
        type: Optional[str] = None,
        category: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> GetTopTrendsResponse:
        """Return today's live trending items. Omit ``type`` on REST to get all feeds."""
        body: Dict = {"mode": "get_top_trends"}
        if type:
            body["type"] = type
        if category:
            body["category"] = category
        if limit is not None:
            body["limit"] = limit
        if offset is not None:
            body["offset"] = offset
        return _parse_top_trends(self._post(body))


class AsyncTrendsMcpClient:
    """Async Trends MCP API client (requires ``await``)."""

    def __init__(self, api_key: str, base_url: str = BASE_URL, timeout: float = 30.0) -> None:
        if not api_key:
            raise ValueError(
                "AsyncTrendsMcpClient: api_key is required. Get a free key at https://trendsmcp.ai/account?tab=signup"
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

    async def get_time_series(
        self,
        source: str,
        keyword: str,
        data_mode: Optional[str] = None,
    ) -> GetTrendsResponse:
        body: Dict = {"mode": "get_time_series", "source": source, "keyword": keyword}
        if data_mode:
            body["data_mode"] = data_mode
        return _parse_trends(await self._post(body))

    async def get_trends(
        self,
        source: str,
        keyword: str,
        data_mode: Optional[str] = None,
    ) -> GetTrendsResponse:
        return await self.get_time_series(source=source, keyword=keyword, data_mode=data_mode)

    async def get_growth(
        self,
        source: str,
        keyword: str,
        percent_growth: Optional[List[Union[str, CustomGrowthPeriod]]] = None,
        data_mode: Optional[str] = None,
    ) -> GetGrowthResponse:
        body: Dict = {"mode": "get_growth", "source": source, "keyword": keyword}
        if percent_growth is not None:
            body["percent_growth"] = [_build_growth_period(p) for p in percent_growth]
        if data_mode:
            body["data_mode"] = data_mode
        return _parse_growth(await self._post(body))

    async def get_top_trends(
        self,
        type: Optional[str] = None,
        category: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> GetTopTrendsResponse:
        body: Dict = {"mode": "get_top_trends"}
        if type:
            body["type"] = type
        if category:
            body["category"] = category
        if limit is not None:
            body["limit"] = limit
        if offset is not None:
            body["offset"] = offset
        return _parse_top_trends(await self._post(body))
