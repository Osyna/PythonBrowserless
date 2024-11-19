from typing import List
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
import logging
from scrapper.browserless.browserless import BrowserlessClient, BrowserlessError

logger = logging.getLogger(__name__)


class GoogleSearchResult:
    def __init__(self, title: str, url: str):
        self.title = title
        self.url = url

    def __repr__(self) -> str:
        return f"GoogleSearchResult(title='{self.title}', url='{self.url}')"


class GoogleSearch:

    def __init__(self, browserless_client: BrowserlessClient):
        self.browserless_client = browserless_client

    def search(self, query: str, num_results: int = 10) -> List[GoogleSearchResult]:
        try:
            encoded_query = quote_plus(query)
            google_url = (
                f"https://www.google.com/search"
                f"?q={encoded_query}&num={num_results}&tbs=li:1&udm=14"
            )

            logger.info(f"Performing Google search for query: {query}")

            content = self.browserless_client.get_page_content(
                    url = google_url,
                    wait_selector = {"selector": "#search", "timeout": 10000},
                    reject_resource_types = ["image", "font", "stylesheet"]
                    )

            return self._parse_search_results(content)

        except BrowserlessError as e:
            logger.error(f"Search failed: {str(e)}")
            raise

    def _parse_search_results(self, content: str) -> List[GoogleSearchResult]:
        soup = BeautifulSoup(content, 'html.parser')
        results = []

        for result in soup.select('div.g'):
            title_element = result.select_one('h3')
            link_element = result.select_one('a')

            if title_element and link_element:
                title = title_element.get_text().strip()
                url = link_element.get('href')

                if url and url.startswith('http'):
                    results.append(GoogleSearchResult(title = title, url = url))

        return results
