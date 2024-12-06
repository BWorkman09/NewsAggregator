from sqlalchemy.exc import SQLAlchemyError
from api.models import db, User, Article, Category, UserPreference
from typing import List, Optional, Dict, Any, Tuple
from pathlib import Path
import sqlite3
import re
from sqlalchemy import func


# ---------------------------------------------------------
# Users Functions
# ---------------------------------------------------------

def get_all_users(limit: int = None) -> List[User]:
    """
    Retrieve users from the database with a specified limit.
    
    Args:
        limit (int): Maximum number of User objects to retrieve.
    
    Returns:
        List[User]: A list of User objects up to the specified limit.
    """
    return User.query.limit(limit).all()

def get_users_by_name(name_filter: str, starts_with: bool = True) -> List[User]:
    if starts_with:
        return User.query.filter(User.Name.like(f'{name_filter}%')).all()
    return User.query.filter(User.Name.like(f'%{name_filter}%')).all()

def create_user(name: str, email: str) -> User:
    """Create a new user with a unique ID in format XX-XXXXXXX"""
    try:
        # Generate unique user ID
        while True:
            user_id = User.generate_user_id()
            if not User.query.get(user_id):
                break
        
        # Create new user with ID
        new_user = User(
            User_ID=user_id,
            Name=name,
            Email=email
        )
        
        db.session.add(new_user)
        db.session.commit()
        return new_user
        
    except Exception as e:
        db.session.rollback()
        raise e


def update_user_name(user_id: str, new_name: str):
    """
    Update a user's name in the database.
    """
    try:
        # Validate user ID format
        if not user_id or not isinstance(user_id, str) or not re.match(r'^\d{2}-\d{7}$', user_id):
            raise ValueError('Invalid user ID format. Must be XX-XXXXXXX')
            
        # Validate new name
        if not new_name or not isinstance(new_name, str):
            raise ValueError('Name is required and must be a string')

        user = User.query.filter_by(User_ID=user_id).first()
        if not user:
            raise ValueError(f'No user found with ID {user_id}')

        user.Name = new_name
        db.session.commit()
        return user.to_dict()
    except Exception as e:
        db.session.rollback()
        raise e


def delete_user(user_id: str):
    """
    Delete a user from the database.
    """
    try:
        user = User.query.filter_by(User_ID=user_id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False
    except Exception as e:
        db.session.rollback()
        raise e

# ---------------------------------------------------------
# Category Functions
# ---------------------------------------------------------

def get_all_categories(limit: int = None) -> List[Category]:
    """
    Retrieve categories from the database with a specified limit.
    
    Args:
        limit (int): Maximum number of Category objects to retrieve.

    Returns:
        List[Category]: A list of Category objects up to the specified limit.
    """
    # Apply limit if specified, otherwise retrieve all categories
    return Category.query.limit(limit).all() if limit else Category.query.all()


# ---------------------------------------------------------
# Article Functions
# ---------------------------------------------------------

def get_all_articles(limit: int = 250) -> List[tuple]:
    """
    Retrieve articles with their associated category details up to the specified limit.
    
    Args:
        limit (int): Maximum number of articles to retrieve.
    
    Returns:
        List[tuple]: A list of tuples containing Article and Category objects
    """
    return (
        db.session.query(Article, Category)
        .join(Category, Article.Category_ID == Category.Category_ID)
        .limit(limit)
        .all()
    )

def get_articles_by_category_name(category_name: Optional[str] = None, limit: int = 250) -> List[tuple]:
    """
    Retrieve articles with their associated category details, filtered by category name.
    Supports case-insensitive and partial word matching.
    Default limit is 250 if not specified.
   
    Args:
        category_name (str, optional): Category name to filter articles (case-insensitive, partial match)
        limit (int): Maximum number of Article objects to retrieve.
   
    Returns:
        List[tuple]: A list of tuples containing Article and Category objects
    """
    query = (
        db.session.query(Article, Category)
        .join(Category, Article.Category_ID == Category.Category_ID)
    )
   
    if category_name is not None:
        query = query.filter(Category.Category.ilike(f'%{category_name}%'))
   
    return query.limit(limit).all()

# ---------------------------------------------------------
# User Preference Functions
# ---------------------------------------------------------

def get_all_user_preferences(limit: int = None, name: str = None) -> List[dict]:
    """
    Retrieve consolidated user preferences from the database with optional filters.
   
    Args:
        limit (int): Maximum number of users to retrieve preferences for.
        name (str): Filter users by name (case-insensitive partial match)
    Returns:
        List[dict]: A list of dictionaries containing user information and their preferences.
    """
    # First, get the filtered user IDs if name is provided
    user_query = db.session.query(User.User_ID)
    if name:
        user_query = user_query.filter(User.Name.ilike(f'%{name}%'))
    if limit:
        user_query = user_query.limit(limit)
    filtered_user_ids = user_query.all()
    
    # If name filter is applied and no users found, return empty list
    if name and not filtered_user_ids:
        return []
    
    # Get preferences for filtered users
    query = db.session.query(
        UserPreference,
        Category.Category,
        User.Name
    ).join(
        Category,
        UserPreference.Category_ID == Category.Category_ID
    ).join(
        User,
        UserPreference.User_ID == User.User_ID
    )
    
    if filtered_user_ids:
        user_ids = [uid[0] for uid in filtered_user_ids]
        query = query.filter(UserPreference.User_ID.in_(user_ids))

    results = query.all()
    
    # Group preferences by user
    user_preferences = {}
    for pref, category, user_name in results:
        if pref.User_ID not in user_preferences:
            user_preferences[pref.User_ID] = {
                "User_ID": pref.User_ID,
                "Name": user_name,
                "Preferences": []
            }
        
        user_preferences[pref.User_ID]["Preferences"].append({
            "Category_ID": pref.Category_ID,
            "Category": category
        })
    
    return list(user_preferences.values())


def update_user_preferences(user_id: str, category_names: List[str]) -> List[dict]:
    """
    Update a user's preferences in the database using category names.
    
    Args:
        user_id (str): The user's ID in format XX-XXXXXXX
        category_names (List[str]): List of category names to set as user's preferences
        
    Returns:
        List[dict]: List of updated user preferences with category information
    """
    # Validate user ID format
    if not user_id or not isinstance(user_id, str) or not re.match(r'^\d{2}-\d{7}$', user_id):
        raise ValueError('Invalid user ID format. Must be XX-XXXXXXX')
    
    # Check if user exists
    user = User.query.filter_by(User_ID=user_id).first()
    if not user:
        raise ValueError(f'No user found with ID {user_id}')
    
    # Normalize input category names
    normalized_names = [name.upper().strip() for name in category_names]
    
    # Get categories by names, using uppercase comparison
    existing_categories = Category.query.filter(
        Category.Category.in_(normalized_names)
    ).all()
    
    if len(existing_categories) != len(category_names):
        found_names = {cat.Category for cat in existing_categories}
        invalid_names = set(normalized_names) - found_names
        raise ValueError(f'Invalid category names: {", ".join(invalid_names)}')
    
    try:
        # Remove existing preferences
        UserPreference.query.filter_by(User_ID=user_id).delete()
        
        # Create new preferences using category IDs from found categories
        new_preferences = [
            UserPreference(User_ID=user_id, Category_ID=cat.Category_ID)
            for cat in existing_categories
        ]
        db.session.bulk_save_objects(new_preferences)
        
        # Commit the transaction
        db.session.commit()
        
        # Get updated preferences with category information
        results = db.session.query(
            UserPreference,
            Category.Category
        ).join(
            Category,
            UserPreference.Category_ID == Category.Category_ID
        ).filter(
            UserPreference.User_ID == user_id
        ).all()
        
        if results:
            return [{
                "User_ID": pref.User_ID,
                "Category_ID": pref.Category_ID,
                "Category": category
            } for pref, category in results]
        return []
            
    except Exception as e:
        db.session.rollback()
        raise e
    
    
def delete_user_preference(user_id: str, category_id: str):
    """
    Delete a specific user preference from the database.
    
    Args:
        user_id (str): The user's ID in format XX-XXXXXXX
        category_id (str): Category ID to remove from user's preferences
    
    Returns:
        bool: True if preference was deleted, False if not found
    """
    try:
        # Validate user ID format
        if not user_id or not isinstance(user_id, str) or not re.match(r'^\d{2}-\d{7}$', user_id):
            raise ValueError('Invalid user ID format. Must be XX-XXXXXXX')
        
        preference = UserPreference.query.filter_by(
            User_ID=user_id,
            Category_ID=category_id
        ).first()
        
        if preference:
            db.session.delete(preference)
            db.session.commit()
            return True
        return False
        
    except Exception as e:
        db.session.rollback()
        raise e    

def get_user_preference_stats() -> List[Dict]:
    """
    Get count of users for each preference category.
    Returns:
        List[Dict]: List of categories with their user counts
    """
    stats = (
        db.session.query(
            Category.Category_ID,
            Category.Category,
            func.count(UserPreference.User_ID).label('user_count')
        )
        .join(UserPreference, Category.Category_ID == UserPreference.Category_ID)
        .group_by(Category.Category_ID, Category.Category)
        .all()
    )
    
    return [
        {
            "Category_ID": stat[0],
            "Category": stat[1],
            "User_Count": stat[2]
        }
        for stat in stats
    ]