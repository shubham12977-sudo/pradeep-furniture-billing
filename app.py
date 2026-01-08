import os
import json
import gspread
from google.oauth2.service_account import Credentials
from flask import Flask, request, render_template

app = Flask(__name__)

# Google Sheets Setup from Environment Variable
def get_gspread_client():
    creds_json = os.environ.get('GOOGLE_CREDS_JSON')
    if not creds_json:
        raise ValueError("Render par GOOGLE_CREDS_JSON variable nahi mila!")
    
    info = json.loads(creds_json)
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(info, scopes=scope)
    return gspread.authorize(creds)

# Global client and sheet
client = get_gspread_client()
# Apni sheet ka naam yahan check kar lena
sheet = client.open("Pradeep Furniture Billing").sheet1

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        # Form se data lena
        customer_name = request.form.get('customer_name')
        mobile = request.form.get('mobile')
        grand_total = request.form.get('grand_total')
        advance = request.form.get('advance')
        balance = float(grand_total) - float(advance)
        date = "2026-01-08" # Ya dynamic date

        # Google Sheet mein entry
        sheet.append_row([date, customer_name, mobile, grand_total, advance, balance])

        return f"Bill saved for {customer_name}! Balance: {balance}"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    # Created by Shubham Developer
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
