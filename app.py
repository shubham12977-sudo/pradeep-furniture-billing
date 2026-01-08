import os
import sqlite3
import pandas as pd
from flask import Flask, request, render_template_string, send_file
from datetime import datetime

app = Flask(__name__)

# 1. Database Setup
def init_db():
    # SQLite file ko initialize karna
    conn = sqlite3.connect('pradeep_furniture.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       customer_name TEXT, 
                       mobile TEXT, 
                       grand_total REAL, 
                       advance REAL, 
                       balance REAL, 
                       date TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return "Server is Live! Developed by Shubham Developer."

@app.route('/submit', methods=['POST'])
def submit():
    try:
        # Form se data nikalna
        name = request.form.get('customer_name', 'Unknown')
        mobile = request.form.get('mobile', '0000000000')
        total = float(request.form.get('grand_total', 0))
        advance = float(request.form.get('advance', 0))
        balance = total - advance
        date_today = datetime.now().strftime("%Y-%m-%d")

        # 2. Database mein Save karna
        conn = sqlite3.connect('pradeep_furniture.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO orders (customer_name, mobile, grand_total, advance, balance, date) VALUES (?, ?, ?, ?, ?, ?)",
                       (name, mobile, total, advance, balance, date_today))
        conn.commit()
        conn.close()

        return render_template_string(RESULT_HTML, name=name, mobile=mobile, total=total, adv=advance, bal=balance, dt=date_today)
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/download_excel')
def download():
    # 3. Database se Excel generate karna
    conn = sqlite3.connect('pradeep_furniture.db')
    df = pd.read_sql_query("SELECT * FROM orders", conn)
    conn.close()
    
    # Render ke liye temporary writable path
    path = "/tmp/billing_report.xlsx"
    df.to_excel(path, index=False)
    return send_file(path, as_attachment=True)

# Aapka Design
RESULT_HTML = """
<body style="background:#1a202c; color:white; font-family:sans-serif; text-align:center; padding:50px;">
    <div style="background:white; color:black; padding:20px; border-radius:15px; width:350px; margin:auto;">
        <h2>PRADEEP FURNITURE</h2>
        <hr>
        <p>Customer: {{ name }}</p>
        <h2 style="color:red;">Balance: ₹{{ bal }}</h2>
        <a href="/download_excel" style="background:#2ecc71; color:white; padding:10px; text-decoration:none; border-radius:5px; display:block;">DOWNLOAD EXCEL</a>
    </div>
</body>
"""

if __name__ == '__main__':
    # Shubham Developer's Server
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
