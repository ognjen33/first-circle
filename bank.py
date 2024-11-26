from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

# In memory data storage
accounts = {}


def generate_account_id():
    return str(uuid.uuid4())


@app.route('/api/create_account', methods=['POST'])
def create_account():
    """
    Create new account with initial balance, and generate uuid.
    """
    data = request.json
    try:
        initial_deposit = float(data.get('initial_deposit', 0))
        if initial_deposit < 0:
            return jsonify({"error": "Initial deposit must be positive number."}), 400

        account_id = generate_account_id()
        accounts[account_id] = {"balance": initial_deposit}
        return jsonify({"message": "Account created successfully", "account_id": account_id}), 201
    except (ValueError, TypeError):
        if account_id in accounts:
           del accounts[account_id] 
        return jsonify({"error": "Invalid input"}), 400


@app.route('/api/deposit', methods=['POST'])
def deposit():
    """
    Deposit money into an account.
    """
    data = request.json
    try:
        account_id = data['account_id']
        deposit = float(data['deposit'])

        if account_id not in accounts:
            return jsonify({"error": "Account not found"}), 404

        if deposit <= 0:
            return jsonify({"error": "Deposit amount must be positive"}), 400

        accounts[account_id]['balance'] += deposit 
        return jsonify({"message": "Deposit successful", "balance": accounts[account_id]['balance']}), 200
    except (KeyError, ValueError, TypeError):
        return jsonify({"error": "Invalid input"}), 400


@app.route('/api/withdraw', methods=['POST'])
def withdraw():
    """
    Withdraw money from an account.
    """
    data = request.json
    try:
        account_id = data['account_id']
        amount = float(data['amount'])

        if account_id not in accounts:
            return jsonify({"error": "Account not found"}), 404

        if amount <= 0:
            return jsonify({"error": "Withdrawal amount must be a positive number"}), 400

        if accounts[account_id]['balance'] < amount:
            return jsonify({"error": "Insufficient balance"}), 400

        accounts[account_id]['balance'] -= amount
        return jsonify({"message": "Withdrawal successful", "balance": accounts[account_id]['balance']}), 200
    except (KeyError, ValueError, TypeError):
        return jsonify({"error": "Invalid input"}), 400


@app.route('/api/transfer', methods=['POST'])
def transfer():
    """
    Transfer money between accounts.
    """
    data = request.json
    try:
        from_account_id = data['from_account_id']
        to_account_id = data['to_account_id']
        amount = float(data['amount'])

        if from_account_id not in accounts or to_account_id not in accounts:
            return jsonify({"error": "One or both accounts not found"}), 404

        if amount <= 0:
            return jsonify({"error": "Transfer amount must be positive"}), 400

        if accounts[from_account_id]['balance'] < amount:
            return jsonify({"error": "Insufficient balance"}), 400

        accounts[from_account_id]['balance'] -= amount
        accounts[to_account_id]['balance'] += amount
        return jsonify({"message": "Transfer finished successfuly",
                        "from_balance": accounts[from_account_id]['balance'],
                        "to_balance": accounts[to_account_id]['balance']}), 200
    except (KeyError, ValueError, TypeError):
        return jsonify({"error": "Invalid input"}), 400


@app.route('/api/balance/<account_id>', methods=['GET'])
def check_balance(account_id):
    """
    Check the balance of an account.
    """
    try:
        if account_id not in accounts:
            return jsonify({"error": "Account not found"}), 404

        return jsonify({"account_id": account_id, "balance": accounts[account_id]['balance']")

