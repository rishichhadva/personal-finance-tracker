import sqlite3

def connect_db():
    conn = sqlite3.connect("transactions.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            date TEXT,
            category TEXT,
            type TEXT,
            amount REAL
        )
    """)
    conn.commit()
    conn.close()

def add_transaction(date, category, t_type, amount, user):
    conn = sqlite3.connect("transactions.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO transactions (date, category, type, amount, user) VALUES (?, ?, ?, ?, ?)",
                (date, category, t_type, amount, user))
    conn.commit()
    conn.close()

def get_all_transactions(user):
    conn = sqlite3.connect("transactions.db")
    cur = conn.cursor()
    cur.execute("SELECT date, category, type, amount FROM transactions WHERE user = ?", (user,))
    rows = cur.fetchall()
    conn.close()
    return rows

def get_summary(user):
    conn = sqlite3.connect("transactions.db")
    cur = conn.cursor()
    cur.execute("SELECT SUM(amount) FROM transactions WHERE type = 'Income' AND user = ?", (user,))
    income = cur.fetchone()[0] or 0
    cur.execute("SELECT SUM(amount) FROM transactions WHERE type = 'Expense' AND user = ?", (user,))
    expense = cur.fetchone()[0] or 0
    conn.close()
    return income, expense, income - expense

def get_categories(user):
    conn = sqlite3.connect("transactions.db")
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT category FROM transactions WHERE user = ?", (user,))
    rows = [row[0] for row in cur.fetchall()]
    conn.close()
    return rows

def get_by_category(category, user):
    conn = sqlite3.connect("transactions.db")
    cur = conn.cursor()
    cur.execute("SELECT date, category, type, amount FROM transactions WHERE category = ? AND user = ?", (category, user))
    rows = cur.fetchall()
    conn.close()
    return rows

def get_expense_by_category(user):
    conn = sqlite3.connect("transactions.db")
    cur = conn.cursor()
    cur.execute("SELECT category, SUM(amount) FROM transactions WHERE type = 'Expense' AND user = ? GROUP BY category", (user,))
    rows = cur.fetchall()
    conn.close()
    return rows
