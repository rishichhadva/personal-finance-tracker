from firebase_config import db
from datetime import datetime
def sanitize_email(email):
    return email.replace('.', '-').replace('@', '-at-')

def add_transaction(user_email, date, category, t_type, amount):
    user_path = sanitize_email(user_email)
    txn = {
        "date": date,
        "category": category,
        "type": t_type,
        "amount": amount
    }
    db.child("transactions").child(user_path).push(txn)

def get_all_transactions(user_email):
    user_path = sanitize_email(user_email)
    txns = db.child("transactions").child(user_path).get()
    return [
        [user_email, i.val()["date"], i.val()["category"], i.val()["type"], i.val()["amount"]]
        for i in txns.each()
    ] if txns.each() else []

def delete_all_transactions(user_email):
    user_path = sanitize_email(user_email)
    db.child("transactions").child(user_path).remove()

def update_transaction(user_email, txn_id, date, category, t_type, amount):
    user_path = sanitize_email(user_email)
    db.child("transactions").child(user_path).child(txn_id).update({
        "date": date,
        "category": category,
        "type": t_type,
        "amount": amount
    })

def get_by_month(user_email, month, year):
    user_path = sanitize_email(user_email)
    txns = db.child("transactions").child(user_path).get()
    filtered = []
    if txns.each():
        for i in txns.each():
            txn = i.val()
            txn_date = datetime.strptime(txn["date"], "%Y-%m-%d")
            if txn_date.month == month and txn_date.year == year:
                filtered.append([
                    i.key(), txn["date"], txn["category"], txn["type"], txn["amount"]
                ])
    return filtered
