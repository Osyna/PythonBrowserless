# browserless.py
from dataclasses import dataclass
from typing import Optional, Dict, Any
import logging
import requests
from requests.exceptions import RequestException

# Configure logging
logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class BrowserlessConfig:
    url: str
    token: str
    timeout: int = 30  # seconds


class BrowserlessError(Exception):
    pass


class BrowserlessClient:

    def __init__(self, config: BrowserlessConfig):
         self.config = config
         self._validate_config()

    def _validate_config(self) -> None:
        if not self.config.url:
            raise BrowserlessError("No URL")
        if not self.config.token:
            raise BrowserlessError("No token")

    def get_page_content(
            self,
            url: str,
            wait_selector: Optional[Dict[str, Any]] = None,
            reject_resource_types: Optional[list] = None
            ) -> str:

        try:
            payload = {
                "url":                 url,
                "waitForSelector":     wait_selector or {},
                "rejectResourceTypes": reject_resource_types or []
                }

            logger.debug(f"Sending request to Browserless for URL: {url}")

            response = requests.post(
                    f"{self.config.url}/content",
                    params = {"token": self.config.token},
                    json = payload,
                    headers = {"Content-Type": "application/json"},
                    timeout = self.config.timeout
                    )

            if response.status_code != 200:
                raise BrowserlessError(
                        f"Request failed with status {response.status_code}: {response.text}"
                        )

            return response.text

        except RequestException as e:
            logger.error(f"Failed to fetch content: {str(e)}")
            raise BrowserlessError(f"Failed to fetch content: {str(e)}")