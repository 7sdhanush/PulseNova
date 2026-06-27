import sqlite3

conn = sqlite3.connect("database/healthcare.db")
cursor = conn.cursor()

try:
    cursor.execute("""
    ALTER TABLE medicines
    ADD COLUMN missed_count INTEGER DEFAULT 0
    """)

    print("Column added successfully")

except Exception as e:
    print("Column may already exist:", e)

conn.commit()
conn.close()