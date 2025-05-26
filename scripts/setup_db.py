#!/usr/bin/env python3

import sqlite3
import os
import sys

# Add the lib directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from lib.db.connection import get_connection

def setup_database():
    """Create the database tables using the schema file"""
    
    # Read the schema file
    schema_path = os.path.join(os.path.dirname(__file__), '..', 'lib', 'db', 'schema.sql')
    
    try:
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
        
        # Connect to database and execute schema
        conn = get_connection()
        cursor = conn.cursor()
        
        # Execute the schema (split by semicolon to handle multiple statements)
        for statement in schema_sql.split(';'):
            statement = statement.strip()
            if statement:  # Skip empty statements
                cursor.execute(statement)
        
        conn.commit()
        conn.close()
        
        print("Database setup completed successfully!")
        print("Tables created: authors, magazines, articles")
        
    except FileNotFoundError:
        print(f"Error: Schema file not found at {schema_path}")
        sys.exit(1)
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    setup_database()