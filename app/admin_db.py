import sqlite3

conn = sqlite3.connect('accounts.db', check_same_thread=False)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

def init_admin():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS admins(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
    )
    ''')
    conn.commit()

def fetch_for_check(username):
    query = 'SELECT * FROM admins WHERE username = ?'
    return cursor.execute(query, (username, )).fetchone()

def add_user(username, password_hash):
    query = 'INSERT INTO admins (username, password) VALUES (?,?)'
    cursor.execute(query, (username, password_hash))
    conn.commit()