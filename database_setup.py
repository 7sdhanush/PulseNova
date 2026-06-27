import sqlite3
import os

os.makedirs("database", exist_ok=True)

conn = sqlite3.connect("database/healthcare.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS medicines(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    medicine_name TEXT,
    medicine_time TEXT,
    status TEXT,
    missed_count INTEGER DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS health_history(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    health_score INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS caretaker(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    category TEXT,
    amount REAL,
    description TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS symptoms(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symptom TEXT,
    severity TEXT,
    notes TEXT,
    date TEXT
)
""")

conn.commit()
conn.close()

print("Database Created Successfully")