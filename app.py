from flask import Flask, request, jsonify
import loan_service

app = Flask(__name__)

@app.route('/lend', methods=['POST'])
def lend():
    data = request.json
    result = loan_service.lend(data['customer_id'], data['loan_amount'], data['loan_period'], data['interest_rate'])
    return jsonify(result)

@app.route('/payment', methods=['POST'])
def payment():
    data = request.json
    result = loan_service.pay(data['loan_id'], data['payment_type'], data['amount'])
    return jsonify(result)

@app.route('/ledger/<loan_id>', methods=['GET'])
def ledger(loan_id):
    result = loan_service.get_ledger(loan_id)
    return jsonify(result)

@app.route('/account/<customer_id>', methods=['GET'])
def account(customer_id):
    result = loan_service.account_overview(customer_id)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5050)
