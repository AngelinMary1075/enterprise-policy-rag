# src/database.py
import sqlite3
import os

DB_PATH = "data/enterprise.db"

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Establish policy governance metadata table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS policy_metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT UNIQUE,
            department TEXT,
            effective_date TEXT,
            owner TEXT
        )
    ''')
    
    # Mock data seeds matching potential policy files
    policies = [
        ('wfh_policy.pdf', 'Human Resources', '2026-01-01', 'HR Director'),
        ('it_security_policy.pdf', 'Information Technology', '2025-06-15', 'CISO')
    ]
    try:
        cursor.executemany('''
            INSERT OR IGNORE INTO policy_metadata (filename, department, effective_date, owner)
            VALUES (?, ?, ?, ?)
        ''', policies)
        conn.commit()
    except sqlite3.Error:
        pass
    finally:
        conn.close()

def get_metadata(filename):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT department, effective_date, owner FROM policy_metadata WHERE filename = ?", (filename,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"department": row[0], "effective_date": row[1], "owner": row[2]}
    return {"department": "General Compliance", "effective_date": "N/A", "owner": "Corporate Legal"}

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")