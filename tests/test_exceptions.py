from freshdesk.exceptions import (
    FreshdeskAPIError,
    FreshdeskAuthError,
    FreshdeskError,
    FreshdeskRateLimitError,
)


class TestExceptionHierarchy:
    def test_auth_error_is_freshdesk_error(self):
        assert issubclass(FreshdeskAuthError, FreshdeskError)

    def test_rate_limit_error_is_freshdesk_error(self):
        assert issubclass(FreshdeskRateLimitError, FreshdeskError)

    def test_api_error_is_freshdesk_error(self):
        assert issubclass(FreshdeskAPIError, FreshdeskError)


class TestFreshdeskError:
    def test_message(self):
        exc = FreshdeskError("something broke")
        assert str(exc) == "something broke"
        assert isinstance(exc, Exception)


class TestFreshdeskAuthError:
    def test_message(self):
        exc = FreshdeskAuthError("bad creds")
        assert str(exc) == "bad creds"


class TestFreshdeskRateLimitError:
    def test_attributes(self):
        exc = FreshdeskRateLimitError("slow down", retry_after=42)
        assert str(exc) == "slow down"
        assert exc.retry_after == 42

    def test_zero_retry(self):
        exc = FreshdeskRateLimitError("limit", retry_after=0)
        assert exc.retry_after == 0


class TestFreshdeskAPIError:
    def test_attributes(self):
        payload = {"description": "Validation failed", "errors": [{"field": "email"}]}
        exc = FreshdeskAPIError("bad request", status_code=400, error_payload=payload)
        assert str(exc) == "bad request"
        assert exc.status_code == 400
        assert exc.error_payload == payload

    def test_server_error(self):
        exc = FreshdeskAPIError("oops", status_code=500, error_payload={"text": "err"})
        assert exc.status_code == 500
