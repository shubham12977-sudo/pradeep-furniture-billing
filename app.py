from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)
EXCEL_FILE = 'pradeepfurnitureentry.xlsx'

@app.route('/')
def index():
    # Yeh function main form (index.html) ko load karega
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        # 1. Form se basic details lena
        date_val = request.form.get('field1')
        name_val = request.form.get('field2')
        mobile_val = request.form.get('field5')
        
        # 2. Quantity aur Rates ko numbers mein badalna
        w_count = int(request.form.get('w_qty') or 0)
        w_rate = int(request.form.get('w_rate') or 0) 
        d_count = int(request.form.get('d_qty') or 0)
        d_rate = int(request.form.get('d_rate') or 0)
        advance_paid = int(request.form.get('field_adv') or 0)

        # 3. Systematic Calculations
        w_total = w_count * w_rate
        d_total = d_count * d_rate
        grand_total = w_total + d_total
        left_amount = grand_total - advance_paid

        # 4. Excel ke liye data organize karna
        new_row = {
            'Date': [date_val], 
            'Customer Name': [name_val],
            'Windows (Qty)': [w_count], 
            'Window Rate': [w_rate],
            'Doors (Qty)': [d_count], 
            'Door Rate': [d_rate],
            'Total Bill (₹)': [grand_total], 
            'Advance Paid (₹)': [advance_paid],
            'Amount Left (₹)': [left_amount], 
            'Mobile Number': [mobile_val]
        }
        
        # 5. Excel File mein save karne ka logic
        df_new = pd.DataFrame(new_row)
        if os.path.exists(EXCEL_FILE):
            df_old = pd.read_excel(EXCEL_FILE)
            df_final = pd.concat([df_old, df_new], ignore_index=True)
        else:
            df_final = df_new
        
        df_final.to_excel(EXCEL_FILE, index=False)

        # 6. Raseed (Receipt) ke liye data success page par bhejna
        bill_details = {
            'date': date_val, 
            'name': name_val, 
            'mobile': mobile_val,
            'windows': w_count, 
            'w_rate': w_rate, 
            'w_price': w_total,
            'doors': d_count, 
            'd_rate': d_rate, 
            'd_price': d_total,
            'total': grand_total, 
            'advance': advance_paid, 
            'left': left_amount
        }
        return render_template('success.html', bill=bill_details)

    except Exception as e:
        # Agar koi galti ho toh error dikhaye
        return f"Error: {str(e)}"

if __name__ == "__main__":
    app.run()
