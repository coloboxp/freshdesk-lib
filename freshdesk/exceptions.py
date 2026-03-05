class FreshdeskError(Exception):
    """Base exception for all Freshdesk API errors."""

class FreshdeskAuthError(FreshdeskError):
    """Raised when authentication fails (401, 403)."""

class FreshdeskRateLimitError(FreshdeskError):
    """Raised when the rate limit has been exceeded and retries are exhausted or disabled."""
    
    def __init__(self, message: str, retry_after: int) -> None:
        super().__init__(message)
        self.retry_after = retry_after

class FreshdeskAPIError(FreshdeskError):
    """Raised for general API errors (e.g. 400, 404, 500) that return an error payload."""
    
    def __init__(self, message: str, status_code: int, error_payload: dict) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.error_payload = error_payload
