from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_transaction():
    # Process form data here (e.g., save to database)
    # For now, redirect to transaction history page
    return redirect(url_for('view_transactions'))

@app.route('/view')
def view_transactions():
    # Fetch transaction data from database if applicable
    return render_template('transaction.html')

if __name__ == '__main__':
    app.run(debug=True)

