import os
import re
import requests

from loguru import logger
from requests.exceptions import RetryError
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from urllib3.exceptions import MaxRetryError

session = requests.Session()
retry = Retry(total=5, backoff_factor=1, status_forcelist=[400])
adapter = HTTPAdapter(max_retries=retry)
session.mount("http://", adapter)
session.mount("https://", adapter)


def get_conversion_rate(url: str) -> float:
    """
    Retrieves conversion rate from given 'url'.

    :param url: source to get conversion rate
    :return: a float-type conversion rate or fixed value if requests failed
    """
    logger.info("Starting conversion rate retrieval.")
    conversion_rate = float(os.environ["DEFAULT_CONVERSION_RATE"])
    try:
        conversion_rates = session.get(url)

        if conversion_rates.status_code != 200:
            logger.warning(f"Couldn't get conversion rate for url {url}.")
            logger.info("Conversion rate wasn't retrieved, using default value.")
            return conversion_rate

        # retrieve simbols after "Доллар США</Name><Value>" and before "<"
        match_conversion_rate = re.search(
            "Доллар США</Name><Value>(?P<conversion_rate>[^>]+)<", conversion_rates.text
        )
        if not match_conversion_rate:
            logger.warning(
                f"Couldn't find conversion rate in result: {conversion_rates.text}"
            )
            logger.info("Conversion rate wasn't retrieved, using default value.")
            return conversion_rate

        conversion_rate = match_conversion_rate.group("conversion_rate").replace(
            ",", "."
        )
        logger.info("Conversion rate retrieved.")
        return float(conversion_rate)
    except (MaxRetryError, RetryError):
        logger.warning(
            f"Couldn't get conversion rate, max retries exceeded with url {url}."
        )
    logger.info("Conversion rate wasn't retrieved, using default value.")
    return conversion_rate
