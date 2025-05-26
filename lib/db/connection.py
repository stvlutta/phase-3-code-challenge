import sqlite3
import os

def get_connection():
    # Use test database if running tests
    db_name = 'test_articles.db' if os.environ.get('TESTING') else 'articles.db'
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row  # This enables column access by name
    return conn