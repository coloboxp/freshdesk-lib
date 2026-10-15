"""Attachment downloads against a real local HTTP server: the bytes, the size limit, and no credentials sent."""

import asyncio
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest

from freshdesk import AsyncFreshdesk, Freshdesk
from freshdesk.models import Attachment

BODY = b"line one\nline two\n" * 1000
seen_headers: list = []


class Files(BaseHTTPRequestHandler):
    def do_GET(self):  # noqa: N802 - http.server API
        seen_headers.append(dict(self.headers))
        if self.path == "/missing":
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"message": "gone"}')
            return
        self.send_response(200)
        self.send_header("Content-Length", str(len(BODY)))
        self.end_headers()
        self.wfile.write(BODY)

    def log_message(self, *args):
        pass


@pytest.fixture(scope="module")
def storage():
    server = ThreadingHTTPServer(("127.0.0.1", 0), Files)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{server.server_address[1]}"
    server.shutdown()


def test_sync_download_returns_the_bytes_without_credentials(storage):
    seen_headers.clear()
    with Freshdesk(domain="example", api_key="secret-key") as fd:
        got = fd.download_attachment(Attachment(id=1, name="app.log", attachment_url=f"{storage}/file"))
    assert (got.name, got.data, got.truncated) == ("app.log", BODY, False)
    assert "authorization" not in {k.lower() for k in seen_headers[0]}


def test_async_download_stops_at_the_limit(storage):
    async def run():
        async with AsyncFreshdesk(domain="example", api_key="secret-key") as fd:
            return await fd.download_attachment(f"{storage}/file", max_bytes=100)
    got = asyncio.run(run())
    assert (got.data, got.truncated) == (BODY[:100], True)


def test_failed_download_raises_and_a_url_is_required(storage):
    with Freshdesk(domain="example", api_key="secret-key") as fd:
        with pytest.raises(Exception, match="404|gone"):
            fd.download_attachment(f"{storage}/missing")
        with pytest.raises(ValueError, match="no attachment_url"):
            fd.download_attachment(Attachment(id=2, name="x"))
