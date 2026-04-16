import os
import gspread
from google.oauth2.service_account import Credentials

# Scopes
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Load credentials from file
creds = Credentials.from_service_account_file(
    os.path.join(os.getcwd(), "credentials.json"),
    scopes=scope
)

# Authorize client
client = gspread.authorize(creds)

# Open sheet
sheet = client.open("Roofing Leads").sheet1


def save_lead(name, phone, issue):
    sheet.append_row([name, phone, issue])
