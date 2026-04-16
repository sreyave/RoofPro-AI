import os
import json
import gspread
from google.oauth2.service_account import Credentials

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# -----------------------------
# LOCAL + PRODUCTION SUPPORT
# -----------------------------

if os.path.exists("credentials.json"):
    # 👉 LOCAL (your laptop)
    creds = Credentials.from_service_account_file(
        "credentials.json",
        scopes=scope
    )
else:
    # 👉 RENDER / CLOUD
    creds_json = json.loads(os.environ["GOOGLE_CREDENTIALS_JSON"])
    creds = Credentials.from_service_account_info(
        creds_json,
        scopes=scope
    )

# Authorize client
client = gspread.authorize(creds)

# Open sheet
sheet = client.open("Roofing Leads").sheet1


def save_lead(name, phone, issue):
    sheet.append_row([name, phone, issue])


def get_all_leads():
    return sheet.get_all_records()
