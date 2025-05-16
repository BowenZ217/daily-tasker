#!/usr/bin/env python3
"""
daily_tasker.core.http_client
-----------------------------

An HTTP client wrapper around `requests.Session` that adds:
  - automatic session initialization
  - configurable timeouts
  - configurable retry logic with exponential backoff
  - convenience methods for GET, POST, PUT, PATCH, DELETE
"""

import time
from typing import Any

from requests import RequestException, Response, Session

from daily_tasker.config.models import RequesterConfig
from daily_tasker.utils.session_helper import init_session


class HttpClient:
    def __init__(self, config: RequesterConfig):
        """
        Initialize with a session configuration.

        :param config: The RequesterConfig instance containing session settings.
        """
        self._config = config
        self._session: Session = init_session(config=config)

    def get(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Response:
        """
        Send a GET request, retrying on failures.

        :param url: The target URL.
        :param params: Query parameters for the request.
        :param kwargs: Additional `requests` parameters (e.g. headers).
        :return: The `requests.Response` object.
        :raises RequestException: if all retries fail.
        """
        return self._request_with_retry("get", url, params=params, **kwargs)

    def post(
        self,
        url: str,
        data: dict[str, Any] | bytes | None = None,
        json: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Response:
        """
        Send a POST request, retrying on failures.

        :param url: The target URL.
        :param data: Form-encoded body or raw bytes.
        :param json: JSON body (mutually exclusive with `data`).
        :param kwargs: Additional `requests` parameters (e.g. headers).
        :return: The `requests.Response` object.
        :raises RequestException: if all retries fail.
        """
        return self._request_with_retry("post", url, data=data, json=json, **kwargs)

    def put(
        self,
        url: str,
        data: dict[str, Any] | bytes | None = None,
        json: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Response:
        """
        Send a PUT request with retry logic.
        """
        return self._request_with_retry("put", url, data=data, json=json, **kwargs)

    def patch(
        self,
        url: str,
        data: dict[str, Any] | bytes | None = None,
        json: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Response:
        """
        Send a PATCH request with retry logic.
        """
        return self._request_with_retry("patch", url, data=data, json=json, **kwargs)

    def delete(
        self,
        url: str,
        **kwargs: Any,
    ) -> Response:
        """
        Send a DELETE request with retry logic.
        """
        return self._request_with_retry("delete", url, **kwargs)

    def _request_with_retry(
        self,
        method: str,
        url: str,
        **kwargs: Any,
    ) -> Response:
        """
        Internal helper to DRY up retry logic for non-GET methods.
        """
        for attempt in range(self.retry_times + 1):
            try:
                fn = getattr(self._session, method)
                resp: Response = fn(url, timeout=self.timeout, **kwargs)
                resp.raise_for_status()
                return resp
            except RequestException:
                if attempt < self.retry_times:
                    backoff = self.retry_interval * (2**attempt)
                    time.sleep(backoff)
                    continue
                raise

        raise RuntimeError("Unreachable code reached in _request_with_retry()")

    @property
    def session(self) -> Session:
        """
        Return the active requests.Session.

        :raises RuntimeError: If the session is uninitialized or has been shut down.
        """
        return self._session

    @property
    def timeout(self) -> float:
        """Return the default timeout setting."""
        return self._config.timeout

    @property
    def retry_times(self) -> int:
        """Return the maximum number of retry attempts."""
        return self._config.retry_times

    @property
    def retry_interval(self) -> float:
        """Return the base interval (in seconds) between retries."""
        return self._config.retry_interval

    @property
    def request_interval(self) -> float:
        """Return the base interval (in seconds) between request."""
        return self._config.request_interval
