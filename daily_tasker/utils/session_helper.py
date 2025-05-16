#!/usr/bin/env python3
"""
daily_tasker.utils.session_helper
---------------------------------

Helpers for building a preconfigured requests.Session with retries and headers.
"""

from requests import Session
from requests.adapters import HTTPAdapter, Retry

from daily_tasker.config.models import (
    RequesterConfig,
)
from daily_tasker.utils.constants import DEFAULT_USER_HEADERS


def init_session(
    config: RequesterConfig,
    cookies: dict[str, str] | None = None,
) -> Session:
    """
    Initialize the requests.Session with default headers and retry strategy.

    :param config: RequesterConfig instance with retry settings
    :param cookies: Optional cookies to attach to the session
    :return: Configured requests.Session instance
    """
    session = Session()

    retry_strategy = Retry(
        total=config.retry_times,
        backoff_factor=config.retry_interval,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"],
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    session.headers.update(DEFAULT_USER_HEADERS)
    if config.user_agent:
        session.headers["User-Agent"] = config.user_agent

    if cookies is not None:
        session.cookies.update(cookies)

    return session
