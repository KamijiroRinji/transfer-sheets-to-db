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


def send_telegram_notification(
    telegram_token: str, telegram_chat_id: str, message: str
):
    """
    Sends telegram notification using 'telegram_token'
        to 'telegram_chat_id' containing 'message'.

    :param telegram_token: telegram token to use
    :param telegram_chat_id: telegram chat id to send notification to
    :param message: message to send
    """
    logger.info("Starting telegram notification sending.")
    url = (
        f"https://api.telegram.org/bot{telegram_token}/"
        f"sendMessage?chat_id={telegram_chat_id}&text={message}"
    )
    try:
        notification_sent = session.get(url)
        if notification_sent.status_code != 200:
            logger.warning(f"Couldn't send telegram notification.")
        logger.info("Telegram notification sent.")
    except (MaxRetryError, RetryError):
        logger.warning(
            f"Couldn't send telegram notification, "
            f"max retries exceeded with url {url}."
        )
