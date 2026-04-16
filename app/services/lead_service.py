import os
import json
import gspread
from google.oauth2.service_account import Credentials

def get_client():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    # ----------------------------
    # LOCAL ENVIRONMENT
    # ----------------------------
    if os.path.exists("credentials.json"):
        creds = Credentials.from_service_account_file(
            "credentials.json",
            scopes=scope
        )

    # ----------------------------
    # RENDER / PRODUCTION
    # ----------------------------
    else:
        creds_json = json.loads(os.environ["GOOGLE_CREDENTIALS_JSON"])

        creds = Credentials.from_service_account_info(
            creds_json,
            scopes=scope
        )

    return gspread.authorize(creds)


def get_all_leads():
    client = get_client()
    sheet = client.open("Roofing Leads").sheet1
    return sheet.get_all_records()
