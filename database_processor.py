import sqlite3

from loguru import logger


def create_connection(name: str) -> sqlite3.Connection:
    """
    Creates database with given 'name' and a connection to it.

    :param name: desired database name
    :return: a sqlite3.Connection-type object
    """
    logger.info("Starting database and connection creation.")
    connection = None
    try:
        connection = sqlite3.connect(name, isolation_level=None)
        logger.info("Database and connection created.")
        return connection
    except sqlite3.Error as e:
        logger.warning(e)
    logger.info("Database and connection weren't created.")
    return connection


def execute_query(db_connection: sqlite3.Connection, sql_query: str):
    """
    Executes query 'sql_query' using connection 'db'.

    :param db_connection: db connection to create table
    :param sql_query: SQL-query to execute
    """
    logger.info(f"Starting query execution.")
    try:
        cursor = db_connection.cursor()
        cursor.execute(sql_query)
        logger.info(f"Query executed.")
    except sqlite3.Error as e:
        logger.warning(e)


def execute_insert(db_connection: sqlite3.Connection, sql_query: str, data: list):
    """
    Executes query 'sql_query' using connection 'db' to insert 'data'.

    :param db_connection: db connection to create table
    :param sql_query: SQL-query to execute
    :param data: data to insert
    """
    logger.info(f"Starting {data} insert execution.")
    try:
        cursor = db_connection.cursor()
        cursor.execute(sql_query, data)
        logger.info(f"{data} insert executed.")
    except sqlite3.Error as e:
        logger.warning(e)


def fetch_all(db_connection: sqlite3.Connection):
    """
    Fetches all rows from 'db' table 'orders'.

    :param db_connection: db connection to create table
    :return:
    """
    logger.info(f"Starting fetching all rows from table 'orders'.")
    try:
        cursor = db_connection.cursor()
        all_rows = cursor.execute("SELECT * FROM orders").fetchall()
        logger.info(f"All rows fetched.")
        return all_rows
    except sqlite3.Error as e:
        logger.warning(e)
