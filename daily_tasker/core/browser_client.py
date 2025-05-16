#!/usr/bin/env python3
"""
daily_tasker.core.browser_client
--------------------------------

"""

import logging
from contextlib import suppress
from typing import cast

from DrissionPage import Chromium, ChromiumOptions
from DrissionPage._pages.mix_tab import MixTab

from daily_tasker.config.models import RequesterConfig
from daily_tasker.utils.constants import (
    DEFAULT_USER_AGENT,
    DEFAULT_USER_DATA_DIR,
    DEFAULT_USER_PROFILE_NAME,
)

logger = logging.getLogger(__name__)
_shared_browser_client = None


class BrowserClient:
    def __init__(self, config: RequesterConfig):
        """
        Initialize with a browser configuration.

        :param config: The RequesterConfig instance containing browser settings.
        """
        self._init_browser(config=config)

    def _init_browser(self, config: RequesterConfig) -> None:
        """
        Initialize the browser with specified options from RequesterConfig.

        :param config: Configuration settings for
                        browser behavior, profile, timeouts, etc.
        """
        self._config = config
        self._options = ChromiumOptions()

        user_data_path = config.user_data_folder or DEFAULT_USER_DATA_DIR
        self._options.set_user_data_path(user_data_path)

        profile_name = config.profile_name or DEFAULT_USER_PROFILE_NAME
        self._options.set_user(profile_name)

        self._options.headless(config.headless)
        self._options.set_user_agent(DEFAULT_USER_AGENT)
        self._options.set_timeouts(base=config.timeout)
        self._options.set_retry(
            times=config.retry_times, interval=config.retry_interval
        )

        self._disable_images_orig = config.disable_images
        if config.disable_images:
            self._options.no_imgs(True)
        if config.mute_audio:
            self._options.mute(True)

        self._setup()

    def _setup(self) -> None:
        """
        Set up the browser instance and open the default tab.
        """
        self._browser = Chromium(self._options)
        self._page = cast(MixTab, self._browser.get_tab())

    @property
    def page(self) -> MixTab:
        """
        Return the current Chromium page object.

        :return: ChromiumPage instance of the current tab.
        """
        return self._page

    @property
    def browser(self) -> Chromium:
        """
        Return the Chromium browser instance.

        :return: Chromium instance used by this browser.
        """
        return self._browser

    def close(self) -> None:
        with suppress(Exception):
            self.browser.quit()


def get_shared_browser_client(config: RequesterConfig) -> BrowserClient:
    global _shared_browser_client
    if _shared_browser_client is None:
        _shared_browser_client = BrowserClient(config)
    return _shared_browser_client
