import logging
from browserless.browserless import BrowserlessClient, BrowserlessConfig, BrowserlessError
from google import GoogleSearch
from utils import get_env_var


logging.basicConfig(
        level = logging.INFO,
        format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
logger = logging.getLogger(__name__)



def main():
    try:
        config = BrowserlessConfig(
                url = get_env_var('BROWSERLESS_URL'),
                token = get_env_var('BROWSERLESS_TOKEN')
                )

        browserless_client = BrowserlessClient(config)
        google_search = GoogleSearch(browserless_client)
        query = "Python programming"
        results = google_search.search(query)

        print("\nSearch Results:")
        print("-" * 50)
        for i, result in enumerate(results, 1):
            print(f"{i}. {result.title}")
            print(f"   URL: {result.url}")
            print()

    except (BrowserlessError, ValueError) as e:
        logger.error(f"Error occurred: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()
