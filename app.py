from flask import Flask, request, send_file, render_template_string
import sqlite3
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)

# Database Setup
def init_db():
    conn = sqlite3.connect('pradeep_furniture.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS bills 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       customer_name TEXT, 
                       mobile TEXT, 
                       total REAL, 
                       advance REAL, 
                       balance REAL, 
                       date TEXT)''')
    conn.commit()
    conn.close()

init_db()

# HTML Template (Screenshot jaisa look)
html_template = """
<!DOCTYPE html>
<html>
<body style="background-color: #1a202c; color: white; font-family: sans-serif; text-align: center;">
    <div style="background: white; color: black; width: 400px; margin: 50px auto; padding: 20px; border-radius: 10px;">
        <h2>PRADEEP FURNITURE</h2>
        <p>Date: {{ date }}</p>
        <hr>
        <p align="left">Customer: <b>{{ name }}</b></p>
        <p align="left">Mobile: <b>{{ mobile }}</b></p>
        <hr>
        <h3 style="color: green;">Grand Total: ₹{{ total }}</h3>
        <h3 style="color: orange;">Advance Paid: -₹{{ advance }}</h3>
        <h2 style="color: red;">BALANCE LEFT: ₹{{ balance }}</h2>
        <a href="/download_excel" style="background: #2ecc71; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">DOWNLOAD EXCEL</a>
    </div>
</body>
</html>
"""

@app.route('/submit', methods=['POST', 'GET'])
def submit():
    # Example data (Inhe aap form se request.form.get() karke le sakte hain)
    data = {
        "name": "bablu bhai",
        "mobile": "9528836338",
        "total": 11400,
        "advance": 1200,
        "date": datetime.now().strftime("%Y-%m-%d")
    }
    balance = data['total'] - data['advance']

    # 1. Database mein save karein
    conn = sqlite3.connect('pradeep_furniture.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO bills (customer_name, mobile, total, advance, balance, date) VALUES (?, ?, ?, ?, ?, ?)",
                   (data['name'], data['mobile'], data['total'], data['advance'], balance, data['date']))
    conn.commit()
    conn.close()

    # 2. Excel File Update Karein
    df = pd.DataFrame([data])
    df['balance'] = balance
    excel_file = 'billing_data.xlsx'
    
    if not os.path.isfile(excel_file):
        df.to_excel(excel_file, index=False)
    else:
        with pd.ExcelWriter(excel_file, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
            df.to_excel(writer, index=False, header=False, startrow=writer.sheets['Sheet1'].max_row)

    return render_template_string(html_template, name=data['name'], mobile=data['mobile'], total=data['total'], advance=data['advance'], balance=balance, date=data['date'])

@app.route('/download_excel')
def download_excel():
    return send_file('billing_data.xlsx', as_attachment=True)

if __name__ == '__main__':
    print("Developed by: Shubham Developer")
    app.run(debug=True)
