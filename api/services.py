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

def create_user(name: str, email: str):
    """
    Create a new user in the database.
    """
    new_user = User(Name=name, Email=email)
    try:
        db.session.add(new_user)
        db.session.commit()
        db.session.refresh(new_user)
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

def get_all_articles(limit: int = 250) -> List[Article]:
    """
    Retrieve articles from the database with a specified limit.
    Default limit is 250 if not specified.
   
    Args:
        limit (int): Maximum number of Article objects to retrieve.
   
    Returns:
        List[Article]: A list of Article objects up to the specified limit.
    """
    return Article.query.limit(limit).all()

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

def get_all_user_preferences(limit: int = None) -> List[UserPreference]:
    """
    Retrieve user preferences from the database with a specified limit.
    
    Args:
        limit (int): Maximum number of UserPreference objects to retrieve.
    Returns:
        List[UserPreference]: A list of UserPreference objects up to the specified limit.
    """
    query = db.session.query(
        UserPreference, 
        Category.Category  # Using the Category column directly
    ).join(
        Category,
        UserPreference.Category_ID == Category.Category_ID
    )
    
    if limit:
        query = query.limit(limit)
    
    return query.all()


def update_user_preference(user_id: str, category_id: str):
    """
    Update a user's preference in the database.
    
    Args:
        user_id (str): The user's ID in format XX-XXXXXXX
        category_id (str): Category ID to add as user's preference
        
    Returns:
        dict: Updated user preference with category information
    """
    try:
        # Validate user ID format
        if not user_id or not isinstance(user_id, str) or not re.match(r'^\d{2}-\d{7}$', user_id):
            raise ValueError('Invalid user ID format. Must be XX-XXXXXXX')
        
        # Check if user exists
        user = User.query.filter_by(User_ID=user_id).first()
        if not user:
            raise ValueError(f'No user found with ID {user_id}')
        
        # Check if category exists
        category = Category.query.filter_by(Category_ID=category_id).first()
        if not category:
            raise ValueError(f'Invalid category ID: {category_id}')
        
        # Create new preference (will replace if exists due to primary key constraint)
        preference = UserPreference(User_ID=user_id, Category_ID=category_id)
        db.session.merge(preference)
        db.session.commit()
        
        # Get updated preference with category information
        result = db.session.query(
            UserPreference, 
            Category.Category
        ).join(
            Category,
            UserPreference.Category_ID == Category.Category_ID
        ).filter(
            UserPreference.User_ID == user_id,
            UserPreference.Category_ID == category_id
        ).first()
        
        if result:
            return {
                "User_ID": result[0].User_ID,
                "Category_ID": result[0].Category_ID,
                "Category": result[1]
            }
        return None
        
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