from flask import Flask, render_template, redirect, url_for, request
from supabase import create_client, Client

app = Flask(__name__)

# Load Supabase configuration from the file
def load_supabase_config(file_path='supabase_key.txt'):
    config = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            config[key] = value
    return config

config = load_supabase_config()
SUPABASE_URL = config.get('SUPABASE_URL')
SUPABASE_KEY = config.get('SUPABASE_KEY')

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_transaction():
    # Extract form data from the request
    date = request.form.get('date')
    category = request.form.get('category')
    amount = request.form.get('amount')
    transaction_type = request.form.get('type')
    
    # Example of saving transaction to Supabase (adjust as needed)
    data = {
        "date": date,
        "category": category,
        "amount": amount,
        "type": transaction_type
    }
    response = supabase.table("transactions").insert(data).execute()
    
    # Redirect to the transaction history page after saving
    return redirect(url_for('view_transactions'))

@app.route('/view')
def view_transactions():
    # Fetch transaction data from the database
    response = supabase.table("transactions").select("*").execute()
    transactions = response.data
    
    return render_template('transaction.html', transactions=transactions)

if __name__ == '__main__':
    app.run(debug=True)

