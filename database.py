import sqlite3

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    year TEXT,
    department TEXT,
    email TEXT,
    password TEXT,
    phone TEXT
)
""")

conn.commit()
conn.close()

print("Database & table created")