import sqlite3
import hashlib

DB_NAME = "todo_simple.db"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_tables():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                email TEXT UNIQUE,
                password_hash TEXT
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                title TEXT,
                status TEXT DEFAULT 'pending'
            )
        ''')
        conn.commit()

def register_user(username, email, password):
    try:
        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            c.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                (username, email, hash_password(password))
            )
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False

def check_user(username, password):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT id, password_hash FROM users WHERE username=?", (username,))
        row = c.fetchone()
        if row and row[1] == hash_password(password):
            return row[0]
    return None

def add_task(user_id, title):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO tasks (user_id, title) VALUES (?, ?)", (user_id, title))
        conn.commit()

def get_tasks(user_id):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT id, title, status FROM tasks WHERE user_id=?", (user_id,))
        return c.fetchall()

def mark_task_done(task_id):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("UPDATE tasks SET status='done' WHERE id=?", (task_id,))
        conn.commit()
