import sqlite3

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_name TEXT,
        phone TEXT,
        doctor TEXT,
        time TEXT
    )
    """)
    conn.commit()
    conn.close()

def save_appointment(user_name, phone, doctor, time):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO appointments (user_name, phone, doctor, time) VALUES (?, ?, ?, ?)",
                   (user_name, phone, doctor, time))
    conn.commit()
    conn.close()
