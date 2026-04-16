import os
import json
import gspread
from google.oauth2.service_account import Credentials


def get_google_client():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds_json = json.loads(os.environ["GOOGLE_CREDENTIALS_JSON"])

    creds = Credentials.from_service_account_info(
        creds_json,
        scopes=scope
    )

    client = gspread.authorize(creds)
    return client
