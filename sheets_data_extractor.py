import gspread

from loguru import logger
from oauth2client.service_account import ServiceAccountCredentials


def authorize_credentials(json_key_file: str, scope: list) -> gspread.client.Client:
    """
    Authorizes Google client with given credentials and returns authorized Google client.

    :param json_key_file: Google service account key
    :param scope: scope to be authorized
    :return: gspread.client.Client object
    """
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(json_key_file, scope)
    return gspread.authorize(credentials)


def get_worksheet(
    json_key_file: str, scope: list, spreadsheet_key: str, worksheet_key: str
) -> gspread.worksheet.Worksheet:
    """
    Gets access to the needed worksheet and returns it.

    :param json_key_file: Google service account key
    :param scope: scope to be authorized
    :param spreadsheet_key: Google spreadsheet key
    :param worksheet_key: Google spreadsheet worksheet key (worksheet name)
    :return: gspread.worksheet.Worksheet object
    """
    google_client = authorize_credentials(json_key_file, scope)
    document = google_client.open_by_key(spreadsheet_key)
    return document.worksheet(worksheet_key)


def extract_data(json_key_file: str, spreadsheet_key: str, worksheet_key: str) -> tuple:
    """
    Extracts Google spreadsheet's 'spreadsheet_key' worksheet 'worksheet_key' data.

    :param json_key_file: Google service account key
    :param spreadsheet_key: Google spreadsheet key
    :param worksheet_key: Google spreadsheet worksheet key (worksheet name)
    :return: a list of rows
    """
    logger.info("Starting data extraction.")
    worksheet = get_worksheet(
        json_key_file,
        ["https://www.googleapis.com/auth/spreadsheets"],
        spreadsheet_key,
        worksheet_key,
    )
    all_rows = tuple(worksheet.get_all_records())
    logger.info("Data extracted.")
    return all_rows
