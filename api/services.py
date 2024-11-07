# Service functions, handling business logic, and database operations
import sqlite3
from typing import List
from api.models import User, Category, Article
from pathlib import Path

def get_db_connection():
    """
    Establishes and returns a connection to the SQLite database.

    The connection uses 'data/movie_data.db' as the database file and sets the
    row factory to sqlite3.Row, allowing access to columns by name.

    Returns:
        sqlite3.Connection: A connection object to the SQLite database.
    """
    DATABASE_PATH = Path(__file__).parents[1] / "data"
    connection = sqlite3.connect(DATABASE_PATH / 'News_Aggregator.db')
    connection.row_factory = sqlite3.Row  # This allows you to access columns by name
    return connection

def run_query(query, params=None):
    """
    Run a query on the database and return the results.

    Args:
        query (str): The SQL query to be executed.
        params (tuple, optional): The parameters to be passed to the query. Defaults to None.

    Returns:
        list of dict: A list of dictionaries representing the query results.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    if params is not None:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# ---------------------------------------------------------
# Users
# ---------------------------------------------------------

def convert_rows_to_user_list(users):
    """
    Converts a list of user dictionaries to a list of User objects.

    Args:
        users (list): A list of dictionaries, where each dictionary contains
                      user information with keys 'user_id', 'username', and 'email'.

    Returns:
        list: A list of User objects created from the provided user dictionaries.
    """
    all_users = []
    # If nothing was passed in, return an empty list
    if users is None:
        return all_users
    
    for user in users:
        user_id, name, email, password_hash = user
        user = User(user_id=user_id, name=name, email=email, password_hash=password_hash)
        all_users.append(user)
    
    return all_users


def get_all_users() -> List[User]:
    """
    Retrieve all users from the database.
    This function establishes a connection to the database, executes a query to
    fetch all users, and converts the result into a list of User objects.
    Returns:
        List[User]: A list of User objects representing all users in the database.
    """
    # We need to start by getting the connection to the database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Query the database for all users
    query = "SELECT user_id, name, email, password_hash FROM users"
    cursor.execute(query)
    
    users = cursor.fetchall()
    conn.close()
    
    # Convert this list of users into a list of User objects
    return convert_rows_to_user_list(users)

