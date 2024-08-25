from flask import Flask, render_template, redirect, url_for, request, flash
import firebase_admin
from firebase_admin import credentials, firestore
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Needed for flashing messages

# Initialize Firebase
cred = credentials.Certificate('firebase_credentials.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

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
    
    # Example of saving transaction to Firestore
    data = {
        "date": date,
        "category": category,
        "amount": amount,
        "type": transaction_type
    }
    
    try:
        db.collection("transactions").add(data)
        flash("Transaction added successfully!")
    except Exception as e:
        flash(f"An error occurred: {e}")
    
    # Redirect to the transaction history page after saving
    return redirect(url_for('view_transactions'))

@app.route('/view')
def view_transactions():
    try:
        # Fetch transaction data from Firestore
        transactions_ref = db.collection("transactions")
        docs = transactions_ref.stream()
        transactions = [doc.to_dict() for doc in docs]
    except Exception as e:
        flash(f"An error occurred: {e}")
        transactions = []
    
    return render_template('transaction.html', transactions=transactions)

if __name__ == '__main__':
    app.run(debug=True)
