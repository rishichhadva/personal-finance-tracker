import json
import os
from datetime import datetime

TRANSACTION_FILE = "transactions.json"

def load_data():
    if os.path.exists(TRANSACTION_FILE):
        with open(TRANSACTION_FILE, "r") as file:
            return json.load(file)
    return []

def save_data(data):
    with open(TRANSACTION_FILE, "w") as file:
        json.dump(data, file, indent=2)

def add_transaction(date, category, t_type, amount):
    data = load_data()
    new_id = data[-1]["id"] + 1 if data else 1
    data.append({
        "id": new_id,
        "date": date,
        "category": category,
        "type": t_type,
        "amount": amount
    })
    save_data(data)

def get_all_transactions():
    data = load_data()
    return [
        [txn["id"], txn["date"], txn["category"], txn["type"], txn["amount"]]
        for txn in data
    ]

def delete_all_transactions():
    save_data([])

def update_transaction(txn_id, date, category, t_type, amount):
    data = load_data()
    for txn in data:
        if txn["id"] == txn_id:
            txn["date"] = date
            txn["category"] = category
            txn["type"] = t_type
            txn["amount"] = amount
            break
    save_data(data)

def get_by_month(month, year):
    data = load_data()
    filtered = [
        [txn["id"], txn["date"], txn["category"], txn["type"], txn["amount"]]
        for txn in data
        if datetime.strptime(txn["date"], "%Y-%m-%d").month == month and
           datetime.strptime(txn["date"], "%Y-%m-%d").year == year
    ]
    return filtered
