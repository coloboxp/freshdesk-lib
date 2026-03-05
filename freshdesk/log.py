"""Logging utilities for freshdesk-lib.

The library logs under the ``"freshdesk"`` logger hierarchy using the
standard :mod:`logging` module.  By default no handlers are attached, so
everything is silent unless the caller opts in.

Quick start – stdout logging
----------------------------

::

    from freshdesk import enable_logging
    enable_logging("debug")          # or logging.DEBUG, "info", etc.

Callback handler
----------------

::

    from freshdesk import Freshdesk, CallbackHandler

    def on_event(record):
        print(f"[{record.levelname}] {record.getMessage()}")

    handler = CallbackHandler(on_event)
    client = Freshdesk(domain="x", api_key="y", log_handler=handler)

Or attach it globally::

    import logging
    logging.getLogger("freshdesk").addHandler(CallbackHandler(my_fn))
"""

from __future__ import annotations

import logging
import sys
from typing import Callable, Optional, Union

LOGGER_NAME = "freshdesk"

logger = logging.getLogger(LOGGER_NAME)


# ---------------------------------------------------------------------------
# Convenience: one-liner to turn on stdout logging
# ---------------------------------------------------------------------------

def enable_logging(
    level: Union[int, str] = logging.DEBUG,
    fmt: str = "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
) -> logging.Handler:
    """Attach a :class:`~logging.StreamHandler` (stdout) to the freshdesk logger.

    Parameters
    ----------
    level
        Minimum severity.  Accepts an int (``logging.DEBUG``) or a
        case-insensitive string (``"debug"``, ``"info"``, …).
    fmt
        Log format string.

    Returns the handler so the caller can remove it later if needed.
    """
    if isinstance(level, str):
        level = getattr(logging, level.upper())

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(fmt))

    root = logging.getLogger(LOGGER_NAME)
    root.setLevel(level)
    root.addHandler(handler)
    return handler


# ---------------------------------------------------------------------------
# Callback handler – bridge user functions into stdlib logging
# ---------------------------------------------------------------------------

class CallbackHandler(logging.Handler):
    """A :class:`~logging.Handler` that forwards every log record to a callback.

    The callback receives the :class:`~logging.LogRecord` directly, so you
    can inspect ``record.levelname``, ``record.getMessage()``,
    ``record.name``, and any extras attached via the ``extra=`` kwarg.

    ::

        def my_sink(record: logging.LogRecord):
            send_to_my_system(level=record.levelname, msg=record.getMessage())

        handler = CallbackHandler(my_sink)
    """

    def __init__(
        self,
        callback: Callable[[logging.LogRecord], None],
        level: Union[int, str] = logging.DEBUG,
    ) -> None:
        super().__init__(level=level if isinstance(level, int) else getattr(logging, level.upper()))
        self.callback = callback

    def emit(self, record: logging.LogRecord) -> None:
        try:
            self.callback(record)
        except Exception:
            self.handleError(record)
