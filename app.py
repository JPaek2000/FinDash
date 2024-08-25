from flask import Flask, render_template, redirect, url_for, request, flash
from supabase import create_client, Client
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Needed for flashing messages

# Load Supabase configuration from the file
def load_supabase_config(file_path='supabase_key.txt'):
    config = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            config[key] = value
    return config

# Load config from file
config = load_supabase_config()
SUPABASE_URL = os.getenv('SUPABASE_URL', config.get('SUPABASE_URL'))
SUPABASE_KEY = os.getenv('SUPABASE_KEY', config.get('SUPABASE_KEY'))

# Ensure that Supabase URL and key are available
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase URL and key must be set either in environment variables or in the configuration file.")

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
    
    # Validate form data
    if not all([date, category, amount, transaction_type]):
        flash("All fields are required!")
        return redirect(url_for('index'))
    
    # Example of saving transaction to Supabase (adjust as needed)
    data = {
        "date": date,
        "category": category,
        "amount": amount,
        "type": transaction_type
    }
    
    try:
        response = supabase.table("transactions").insert(data).execute()
        if response.status_code == 201:
            flash("Transaction added successfully!")
        else:
            flash("Failed to add transaction.")
    except Exception as e:
        flash(f"An error occurred: {e}")
    
    # Redirect to the transaction history page after saving
    return redirect(url_for('view_transactions'))

@app.route('/view')
def view_transactions():
    try:
        # Fetch transaction data from the database
        response = supabase.table("transactions").select("*").execute()
        transactions = response.data
    except Exception as e:
        flash(f"An error occurred: {e}")
        transactions = []
    
    return render_template('transaction.html', transactions=transactions)

if __name__ == '__main__':
    app.run(debug=True)
