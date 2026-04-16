import gspread
from google.oauth2.service_account import Credentials

def get_all_leads():
    scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
    ]


    creds = Credentials.from_service_account_file(
        "credentials.json", scopes=scope
    )

    client = gspread.authorize(creds)

    sheet = client.open("Roofing Leads").sheet1

    records = sheet.get_all_records()

    return records
