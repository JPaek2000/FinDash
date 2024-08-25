from flask import Flask, render_template, redirect, url_for, request, flash, session
import firebase_admin
from firebase_admin import credentials, firestore, auth
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Needed for flashing messages and sessions

# Initialize Firebase
cred = credentials.Certificate('firebase_credentials.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/')
def index():
    if 'user_id' in session:
        return render_template('index.html')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            user = auth.get_user_by_email(email)
            # Client-side verification of the password is needed
            session['user_id'] = user.uid
            return redirect(url_for('index'))
        except auth.AuthError as e:
            flash(f"Login failed: {e}")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            user = auth.create_user(email=email, password=password)
            session['user_id'] = user.uid
            return redirect(url_for('index'))
        except auth.AuthError as e:
            flash(f"Registration failed: {e}")
    return render_template('register.html')

@app.route('/add', methods=['POST'])
def add_transaction():
    # Ensure user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))

    date = request.form.get('date')
    category = request.form.get('category')
    amount = request.form.get('amount')
    transaction_type = request.form.get('type')
    
    if not all([date, category, amount, transaction_type]):
        flash("All fields are required!")
        return redirect(url_for('index'))
    
    data = {
        "date": date,
        "category": category,
        "amount": amount,
        "type": transaction_type,
        "user_id": session['user_id']
    }
    
    try:
        db.collection("transactions").add(data)
        flash("Transaction added successfully!")
    except Exception as e:
        flash(f"An error occurred: {e}")
    
    return redirect(url_for('view_transactions'))

@app.route('/view')
def view_transactions():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    try:
        transactions_ref = db.collection("transactions").where("user_id", "==", session['user_id'])
        docs = transactions_ref.stream()
        transactions = [doc.to_dict() for doc in docs]
    except Exception as e:
        flash(f"An error occurred: {e}")
        transactions = []
    
    return render_template('transaction.html', transactions=transactions)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
