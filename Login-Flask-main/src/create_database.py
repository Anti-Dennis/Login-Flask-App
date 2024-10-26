import sqlite3
import contextlib
from pathlib import Path


def create_connection(db_file: str) -> None:
    """ Create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to database {db_file}")
    except sqlite3.Error as e:
        print(f"Error creating connection to {db_file}: {e}")
    finally:
        if conn:
            conn.close()


def create_table(db_file: str) -> None:
    """ Create a table for users in the database if it doesn't exist """
    query = '''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            email TEXT
        );
    ''' 

    try:
        with contextlib.closing(sqlite3.connect(db_file)) as conn:
            with conn:
                conn.execute(query)
            print(f"Table 'users' created or already exists in {db_file}")
    except sqlite3.Error as e:
        print(f"Error creating table in {db_file}: {e}")


def insert_user(db_file: str, username: str, password: str, email: str) -> None:
    """ Insert a new user into the users table """
    query = '''
        INSERT INTO users(username, password, email)
        VALUES (:username, :password, :email)
    '''
    params = {'username': username, 'password': password, 'email': email}

    try:
        with contextlib.closing(sqlite3.connect(db_file)) as conn:
            with conn:
                conn.execute(query, params)
        print(f"User {username} inserted successfully.")
    except sqlite3.IntegrityError as e:
        print(f"Integrity error: {e} - The username '{username}' might already exist.")
    except sqlite3.Error as e:
        print(f"Database insert error for user {username}: {e}")


def setup_database(name: str) -> None:
    """ Set up the database by checking if it exists, and creating the table if necessary """
    if Path(name).exists():
        print(f"Database '{name}' already exists, no need to create.")
        return

    create_connection(name)  # Establish initial connection
    create_table(name)  # Create 'users' table
    print('\033[91m', f'Creating new example database "{name}"', '\033[0m')

