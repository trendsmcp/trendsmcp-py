"""Exceptions raised by the Trends MCP client."""


class TrendsMcpError(Exception):
    """Raised when the Trends MCP API returns an error response.

    Attributes:
        status: HTTP status code (e.g. 429, 401, 400).
        code: Machine-readable error code string (e.g. "rate_limited").
        message: Human-readable error message.
    """

    def __init__(self, status: int, code: str, message: str) -> None:
        super().__init__(message)
        self.status = status
        self.code = code
        self.message = message

    def __repr__(self) -> str:
        return f"TrendsMcpError(status={self.status}, code={self.code!r}, message={self.message!r})"
