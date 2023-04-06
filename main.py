import datetime
import json
import os
import schedule
import time

from loguru import logger

from conversion_rate_extractor import get_conversion_rate
from database_processor import create_connection, execute_query, execute_insert
from sheets_data_extractor import extract_data
from telegram_notifier import send_telegram_notification

logger.add(f"test-kanalservis_{str(datetime.date.today())}.log")


def main():
    start_time = datetime.datetime.now()
    logger.info(f"Start time: {start_time}.")
    logger.info("Initiating test-kanalservis.")

    logger.info("Authorizing Google API key.")
    json_key_file = json.loads(os.environ["JSON_KEY_FILE"])

    logger.info("Extracting Sheets data.")
    orders_raw = extract_data(
        json_key_file, os.environ["SPREADSHEET_KEY"], os.environ["WORKSHEET_KEY"]
    )

    logger.info("Verifying delivery deadline compliance.")
    today = datetime.date.today()
    for order in orders_raw:
        if (
            datetime.datetime.strptime(order["срок поставки"], "%d.%m.%Y").date()
            < today
        ):
            send_telegram_notification(
                os.environ["TELEGRAM_TOKEN"],
                os.environ["TELEGRAM_CHAT_ID"],
                f"Истек срок поставки ({order['срок поставки']}) "
                f"по заказу №{order['заказ №']}.",
            )

    logger.info("Creating database and connection to it.")
    db_connection = create_connection(os.environ["DB_NAME"])

    logger.info("Creating table.")
    execute_query(db_connection, os.environ["SQL_CREATE_TABLE"])

    logger.info("Clearing table.")
    execute_query(db_connection, os.environ["SQL_CLEAR_TABLE"])

    logger.info("Getting USD to RUB conversion rate.")
    cbr_url = "http://www.cbr.ru/scripts/XML_daily.asp"
    conversion_rate = get_conversion_rate(cbr_url)

    logger.info("Filling table.")
    orders_list = [list(order.values()) for order in orders_raw]
    for order in orders_list:
        rub_sum = round(order[2] * conversion_rate, 2)
        order.insert(3, rub_sum)
        execute_insert(db_connection, os.environ["SQL_INSERT"], order)

    logger.info("Closing connection to database.")
    db_connection.close()
    end_time = datetime.datetime.now()
    logger.info(f"End time: {end_time}.")
    logger.info(f"Processing time: {end_time - start_time}.")


if __name__ == "__main__":
    schedule.every(10).minutes.do(main)

    while True:
        schedule.run_pending()
        time.sleep(1)
