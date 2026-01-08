import os
import json
import gspread
from google.oauth2.service_account import Credentials
from flask import Flask, request, render_template, redirect

app = Flask(__name__)

def get_sheet():
    creds_json = os.environ.get('GOOGLE_CREDS_JSON')
    info = json.loads(creds_json)
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(info, scopes=scope)
    client = gspread.authorize(creds)
    return client.open("Pradeep Furniture Billing").sheet1 # Naam match hona chahiye

@app.route('/submit', methods=['POST'])
def submit():
    try:
        sheet = get_sheet()
        # Form fields (Apne index.html ke names ke hisaab se)
        data = [
            "2026-01-08", 
            request.form.get('customer_name'),
            request.form.get('mobile'),
            request.form.get('grand_total'),
            request.form.get('advance'),
            float(request.form.get('grand_total')) - float(request.form.get('advance'))
        ]
        sheet.append_row(data)
        return "Data Saved Successfully!"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
