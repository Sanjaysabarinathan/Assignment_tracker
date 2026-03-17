import sqlite3
import os
import pandas as pd

DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DB_DIR, "assignments.db")

def init_db():
    """Initializes the SQLite database with the assignments table."""
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            deadline DATE NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def get_connection():
    """Returns a database connection."""
    return sqlite3.connect(DB_PATH)

def add_assignment(subject, title, description, deadline):
    """Adds a new assignment to the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO assignments (subject, title, description, deadline)
        VALUES (?, ?, ?, ?)
    ''', (subject, title, description, deadline))
    conn.commit()
    conn.close()

def delete_assignment(assignment_id):
    """Deletes an assignment by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM assignments WHERE id = ?', (assignment_id,))
    conn.commit()
    conn.close()

def get_all_assignments():
    """Returns all assignments as a pandas DataFrame."""
    conn = get_connection()
    query = "SELECT * FROM assignments ORDER BY deadline ASC"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df
