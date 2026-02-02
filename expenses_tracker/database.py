import sqlite3

DB_NAME = "expenses.db"

# ---------------- CREATE DATABASE ---------------- #
def create_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            category TEXT,
            description TEXT,
            amount REAL,
            payment_mode TEXT
        )
    """)

    conn.commit()
    conn.close()


# ---------------- ADD EXPENSE ---------------- #
def add_expense(date, category, description, amount, payment_mode):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO expenses 
        (date, category, description, amount, payment_mode)
        VALUES (?, ?, ?, ?, ?)
    """, (date, category, description, amount, payment_mode))

    conn.commit()
    conn.close()


# ---------------- FETCH ALL EXPENSES ---------------- #
def get_expenses():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
    data = cursor.fetchall()

    conn.close()
    return data
