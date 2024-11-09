from sqlalchemy.exc import SQLAlchemyError
from api.models import db, User, Article, Category, UserPreference
from typing import List, Optional
from pathlib import Path
import sqlite3



# ---------------------------------------------------------
# Users Functions
# ---------------------------------------------------------

def get_all_users() -> List[User]:
    return User.query.all()

def get_users_by_name(name_filter: str, starts_with: bool = True) -> List[User]:
    if starts_with:
        return User.query.filter(User.Name.like(f'{name_filter}%')).all()
    return User.query.filter(User.Name.like(f'%{name_filter}%')).all()


# ---------------------------------------------------------
# Category Functions
# ---------------------------------------------------------