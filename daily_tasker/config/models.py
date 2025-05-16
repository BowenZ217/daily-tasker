#!/usr/bin/env python3
"""
daily_tasker.config.models
--------------------------

"""

from collections.abc import Mapping
from dataclasses import dataclass, field, fields
from typing import Any, Literal

from daily_tasker.utils.cookies import resolve_cookies

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR"]


def _auto_strip_strings(instance: Any) -> None:
    """
    Strip whitespace from all str fields in a dataclass instance.

    :param instance: The dataclass instance to process.
    """
    for f in fields(instance):
        value = getattr(instance, f.name)
        if isinstance(value, str):
            setattr(instance, f.name, value.strip())
    return


@dataclass
class RequesterConfig:
    user_agent: str = ""
    request_interval: float = 5.0
    retry_times: int = 3
    retry_interval: float = 5.0
    timeout: float = 30.0
    headless: bool = True
    user_data_folder: str = ""
    profile_name: str = ""
    auto_close: bool = True
    disable_images: bool = True
    mute_audio: bool = True

    def __post_init__(self) -> None:
        _auto_strip_strings(self)


@dataclass
class TaskerConfig:
    parallel: bool = False
    max_workers: int = 5
    save_results: bool = False
    results_path: str = "results/"
    generate_report: bool = False

    def __post_init__(self) -> None:
        _auto_strip_strings(self)


@dataclass
class DebugConfig:
    log_level: LogLevel = "INFO"


class SiteConfig:
    def __init__(
        self,
        enabled: bool = True,
        signin_url: str | None = None,
        **kwargs: Any,
    ):
        self.enabled = enabled
        self.signin_url = signin_url
        self._extra: dict[str, Any] = kwargs

    def __getattr__(self, name: str) -> Any:
        if name in self._extra:
            return self._extra[name]
        raise AttributeError(f"'SiteConfig' object has no attribute '{name}'")

    def to_dict(self) -> dict[str, Any]:
        base = {"enabled": self.enabled, "signin_url": self.signin_url}
        return {**base, **self._extra}

    def __repr__(self) -> str:
        parts = [
            f"enabled={self.enabled!r}",
            f"signin_url={self.signin_url!r}",
        ]
        parts += [f"{k}={v!r}" for k, v in self._extra.items()]
        joined = ",\n    ".join(parts)
        return f"SiteConfig(\n    {joined}\n)"


@dataclass
class Account:
    username: str = ""
    password: str = ""
    raw_cookies: str | Mapping[str, str] = field(default_factory=dict)
    cookies: dict[str, str] = field(init=False)

    def __post_init__(self) -> None:
        _auto_strip_strings(self)
        self.cookies = resolve_cookies(self.raw_cookies)
