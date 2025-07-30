from firebase_config import db
from datetime import datetime

def add_transaction(date, category, t_type, amount):
    txn = {
        "date": date,
        "category": category,
        "type": t_type,
        "amount": amount
    }
    db.child("transactions").push(txn)

def get_all_transactions():
    txns = db.child("transactions").get()
    return [
        [i.key(), i.val()["date"], i.val()["category"], i.val()["type"], i.val()["amount"]]
        for i in txns.each()
    ] if txns.each() else []

def delete_all_transactions():
    db.child("transactions").remove()

def update_transaction(txn_id, date, category, t_type, amount):
    db.child("transactions").child(txn_id).update({
        "date": date,
        "category": category,
        "type": t_type,
        "amount": amount
    })

def get_by_month(month, year):
    txns = db.child("transactions").get()
    filtered = []
    for i in txns.each():
        txn = i.val()
        txn_date = datetime.strptime(txn["date"], "%Y-%m-%d")
        if txn_date.month == month and txn_date.year == year:
            filtered.append([
                i.key(), txn["date"], txn["category"], txn["type"], txn["amount"]
            ])
    return filtered
