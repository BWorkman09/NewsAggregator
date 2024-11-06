# Service functions, handling business logic, and database operations
import sqlite3
from typing import List
from api.models import User, Category, Article
from pathlib import Path


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

