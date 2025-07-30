import sqlite3
import matplotlib.pyplot as plt

DB_NAME = 'finance.db'

def connect_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            type TEXT CHECK(type IN ('Income', 'Expense')) NOT NULL,
            amount REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_transaction(date, category, t_type, amount):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO transactions (date, category, type, amount)
        VALUES (?, ?, ?, ?)
    ''', (date, category, t_type, amount))
    conn.commit()
    conn.close()

def get_all_transactions():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT date, category, type, amount FROM transactions")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_summary():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("SELECT SUM(amount) FROM transactions WHERE type = 'Income'")
    income = cur.fetchone()[0] or 0

    cur.execute("SELECT SUM(amount) FROM transactions WHERE type = 'Expense'")
    expense = cur.fetchone()[0] or 0

    conn.close()
    return income, expense, income - expense

def get_categories():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT category FROM transactions")
    rows = [r[0] for r in cur.fetchall()]
    conn.close()
    return rows

def get_by_category(category):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT date, category, type, amount FROM transactions WHERE category = ?", (category,))
    rows = cur.fetchall()
    conn.close()
    return rows

def get_expense_by_category():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('''
        SELECT category, SUM(amount) FROM transactions
        WHERE type = 'Expense'
        GROUP BY category
    ''')
    data = cur.fetchall()
    conn.close()
    return data
