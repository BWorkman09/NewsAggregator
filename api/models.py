# Database models/classes
from datetime import datetime

class User:
    def __init__(self, user_id: int, name: str, email: str, password_hash: str):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password_hash = password_hash

    def __repr__(self):
        return f'<User {self.user_id} - {self.name}>'

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'password_hash': self.password_hash,
        }
    
def create_user_from_dict(data: dict) -> User:
    # create a user object from a dictionary.
    # if user_id is not provided in the dictionary, it will default to none.
    return User(data.get('user_id', None), data['name'], data['email'], data['password_hash'])

    
    
class Category:
    def __init__(self, category_id: int, category: str, description: str):
        self.category_id = category_id
        self.category = category
        self.description = description

    def __repr__(self):
        return f'<Category {self.category_id} - {self.category}>'

    def to_dict(self):
        return {
            'category_id': self.category_id,
            'category': self.category,
            'description': self.description,
        }


class Article:
    def __init__(self, article_id: int, url: str, source: str, title: str, category: str, 
                 category_id: int, content: str, authors: str, date: datetime):
        self.article_id = article_id
        self.url = url
        self.source = source
        self.title = title
        self.category = category
        self.category_id = category_id
        self.content = content
        self.authors = authors
        self.date = date

    def __repr__(self):
        return f'<Article {self.article_id} - {self.title}>'

    def to_dict(self):
        return {
            'article_id': self.article_id,
            'url': self.url,
            'source': self.source,
            'title': self.title,
            'category': self.category,
            'category_id': self.category_id,
            'content': self.content,
            'authors': self.authors,
            'date': self.date.strftime('%Y-%m-%d') if isinstance(self.date, datetime) else self.date,
        }
    
