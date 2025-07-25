import uuid
from utils import load_data, save_data

def lend(customer_id, principal, period, interest_rate):
    data = load_data()
    loan_id = str(uuid.uuid4())

    interest = principal * period * interest_rate / 100
    total_amount = principal + interest
    monthly_emi = total_amount / (period * 12)

    loan_data = {
        "loan_id": loan_id,
        "principal": principal,
        "interest_rate": interest_rate,
        "loan_period": period,
        "total_interest": interest,
        "total_amount": total_amount,
        "monthly_emi": monthly_emi,
        "balance": total_amount,
        "emi_left": int(period * 12),
        "payments": []
    }

    if customer_id not in data["customers"]:
        data["customers"][customer_id] = {"loans": []}
    
    data["customers"][customer_id]["loans"].append(loan_data)
    save_data(data)

    return {
        "loan_id": loan_id,
        "total_amount": total_amount,
        "monthly_emi": monthly_emi
    }

def pay(loan_id, payment_type, amount):
    data = load_data()
    for customer in data["customers"].values():
        for loan in customer["loans"]:
            if loan["loan_id"] == loan_id:
                loan["payments"].append({"type": payment_type, "amount": amount})
                loan["balance"] -= amount
                if payment_type == "EMI":
                    loan["emi_left"] = max(loan["emi_left"] - 1, 0)
                else:
                    emi_amt = loan["monthly_emi"]
                    loan["emi_left"] = max(int(loan["balance"] / emi_amt), 0)
                save_data(data)
                return {"balance": loan["balance"], "emi_left": loan["emi_left"]}
    return {"error": "Loan not found"}

def get_ledger(loan_id):
    data = load_data()
    for customer in data["customers"].values():
        for loan in customer["loans"]:
            if loan["loan_id"] == loan_id:
                return {
                    "loan_id": loan_id,
                    "payments": loan["payments"],
                    "balance": loan["balance"],
                    "emi_left": loan["emi_left"],
                    "monthly_emi": loan["monthly_emi"]
                }
    return {"error": "Loan not found"}

def account_overview(customer_id):
    data = load_data()
    if customer_id not in data["customers"]:
        return {"error": "Customer not found"}
    
    result = []
    for loan in data["customers"][customer_id]["loans"]:
        total_paid = sum(p["amount"] for p in loan["payments"])
        result.append({
            "loan_id": loan["loan_id"],
            "principal": loan["principal"],
            "total_amount": loan["total_amount"],
            "total_interest": loan["total_interest"],
            "monthly_emi": loan["monthly_emi"],
            "balance": loan["balance"],
            "emi_left": loan["emi_left"],
            "amount_paid": total_paid
        })
    return result