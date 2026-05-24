import sqlite3
from datetime import datetime

# 🔗 Create connection
conn = sqlite3.connect("stock.db", check_same_thread=False)
cur = conn.cursor()

# -------------------------
# CREATE TABLES
# -------------------------

# ✅ USERS TABLE
cur.execute("""
CREATE TABLE IF NOT EXISTS users(
    username TEXT UNIQUE,
    password TEXT
)
""")

# ✅ HISTORY TABLE
cur.execute("""
CREATE TABLE IF NOT EXISTS history(
    username TEXT,
    stock TEXT,
    price REAL,
    prediction REAL,
    confidence REAL,
    date TEXT
)
""")

conn.commit()


# -------------------------
# USER FUNCTIONS
# -------------------------

def create_user(u, p):
    try:
        # 🔍 check if user exists
        cur.execute("SELECT * FROM users WHERE username=?", (u,))
        if cur.fetchone():
            return False   # ❌ already exists

        # ✅ insert user
        cur.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (u, p)
        )
        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False


def check_user(u, p):
    cur.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (u, p)
    )
    return cur.fetchone()


# -------------------------
# STOCK FUNCTIONS
# -------------------------

def save_stock(username, stock, price, prediction, confidence):
    try:
        cur.execute(
            "INSERT INTO history VALUES (?,?,?,?,?,?)",
            (username, stock, price, prediction, confidence, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        conn.commit()
    except Exception as e:
        print("DB SAVE ERROR:", e)


def get_history(username):
    cur.execute(
        "SELECT stock, price, prediction, confidence, date FROM history WHERE username=? ORDER BY date DESC",
        (username,)
    )
    return cur.fetchall()


def clear_history(username):
    cur.execute("DELETE FROM history WHERE username=?", (username,))
    conn.commit()


# -------------------------
# EXTRA (SAFE DEBUG)
# -------------------------

def show_all_history():
    cur.execute("SELECT * FROM history")
    data = cur.fetchall()
    print("ALL HISTORY:", data)


def reset_db():
    cur.execute("DROP TABLE IF EXISTS users")
    cur.execute("DROP TABLE IF EXISTS history")
    conn.commit()
def get_all_users():
    cur.execute("SELECT username FROM users")
    return cur.fetchall()

def get_all_history():
    cur.execute("""
        SELECT username, stock, price, prediction, confidence, date
        FROM history
        ORDER BY date DESC
    """)
    return cur.fetchall()