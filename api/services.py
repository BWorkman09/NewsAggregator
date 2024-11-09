from sqlalchemy.exc import SQLAlchemyError
from api.models import db, User, Article, Category, UserPreference
from typing import List, Optional, Dict, Any, Tuple
from pathlib import Path
import sqlite3



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
    Default limit is 250 if not specified.
   
    Args:
        category_name (str, optional): Category name to filter articles
        limit (int): Maximum number of Article objects to retrieve.
   
    Returns:
        List[tuple]: A list of tuples containing Article and Category objects
    """
    query = (
        db.session.query(Article, Category)
        .join(Category, Article.Category_ID == Category.Category_ID)
    )
   
    if category_name is not None:
        query = query.filter(Category.Category == category_name)
   
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
    return UserPreference.query.limit(limit).all()


