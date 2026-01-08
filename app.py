import os
import json
import gspread
from google.oauth2.service_account import Credentials
from flask import Flask, request, render_template_string
from datetime import datetime

app = Flask(__name__)

# Google Sheets Setup (Render Environment Variable se)
def get_sheet_client():
    creds_json = os.environ.get('GOOGLE_CREDS_JSON')
    if not creds_json:
        return None
    
    info = json.loads(creds_json)
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(info, scopes=scope)
    client = gspread.authorize(creds)
    # Sheet ka naam wahi rakhein jo aapne banaya hai
    return client.open("Pradeep Furniture Billing").sheet1

@app.route('/submit', methods=['POST'])
def submit():
    try:
        sheet = get_sheet_client()
        if not sheet:
            return "Error: Render par GOOGLE_CREDS_JSON variable nahi mila!"

        # Form data
        name = request.form.get('customer_name')
        mobile = request.form.get('mobile')
        total = request.form.get('grand_total')
        advance = request.form.get('advance')
        balance = float(total) - float(advance)
        date = datetime.now().strftime("%Y-%m-%d")

        # Google Sheet mein data bhejna
        sheet.append_row([date, name, mobile, total, advance, balance])

        return f"<h1>Success!</h1><p>Data saved for {name} in Google Sheets.</p>"
    except Exception as e:
        return f"<h1>Error</h1><p>{str(e)}</p>"

if __name__ == '__main__':
    # Created by: Shubham Developer
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
