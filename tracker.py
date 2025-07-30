import sqlite3

DB_NAME = "transactions.db"

def connect_db():
    conn = sqlite3.connect(DB_NAME)
    return conn

def init_db():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            category TEXT,
            type TEXT,
            amount REAL
        )
    """)
    conn.commit()
    conn.close()

def add_transaction(date, category, t_type, amount):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO transactions (date, category, type, amount) VALUES (?, ?, ?, ?)", (date, category, t_type, amount))
    conn.commit()
    conn.close()

def get_all_transactions():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions")
    data = cursor.fetchall()
    conn.close()
    return data

def delete_all_transactions():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions")
    conn.commit()
    conn.close()

def update_transaction(txn_id, date, category, t_type, amount):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE transactions
        SET date = ?, category = ?, type = ?, amount = ?
        WHERE id = ?
    """, (date, category, t_type, amount, txn_id))
    conn.commit()
    conn.close()

def get_by_month(month, year):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM transactions
        WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?
    """, (f"{int(month):02d}", str(year)))
    data = cursor.fetchall()
    conn.close()
    return data

# Call init_db() once at start
init_db()
