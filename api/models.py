from flask_sqlalchemy import SQLAlchemy
import random

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    User_ID = db.Column(db.String(10), primary_key=True)  # Changed to String to handle "XX-XXXXXXX" format
    Name = db.Column(db.String(100), nullable=False)
    Email = db.Column(db.String(120), unique=True, nullable=False)
    preferences = db.relationship('UserPreference', backref='user', lazy=True)

    @staticmethod
    def generate_user_id():
        """Generate ID in format: XX-XXXXXXX"""
        prefix = "29"  # Using 29 as per your example
        # Generate a 7-digit number
        num = f"{random.randint(1000000, 9999999):07d}"
        return f"{prefix}-{num}"

    def __init__(self, Name, Email):
        self.User_ID = User.generate_user_id()
        self.Name = Name
        self.Email = Email
   
    def to_dict(self):
        return {
            "User_ID": self.User_ID,
            "Name": self.Name,
            "Email": self.Email
        }
   
class UserPreference(db.Model):
    __tablename__ = 'user_preference'
    
    User_ID = db.Column(db.String, db.ForeignKey('user.User_ID'), primary_key=True)
    Category_ID = db.Column(db.String, db.ForeignKey('category.Category_ID'), primary_key=True)

    def to_dict(self):
        return {
            "User_ID": self.User_ID, 
            "Category_ID": self.Category_ID
        }

   
class Category(db.Model):
    __tablename__ = 'category'  
    Category_ID = db.Column(db.Integer, primary_key=True)
    Category = db.Column(db.String(100), nullable=False)
    Description = db.Column(db.String(100), nullable=False)
    articles = db.relationship('Article', backref='category', lazy=True)  
    
    def to_dict(self):
        return {
            "Category_ID": self.Category_ID,
            "Category": self.Category,
            "Description": self.Description
        }

class Article(db.Model):
    __tablename__ = 'article'
    
    Article_ID = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(200), nullable=False)
    Content = db.Column(db.Text, nullable=False)
    Category_ID = db.Column(db.Integer, db.ForeignKey('category.Category_ID'), nullable=False)
    URL = db.Column(db.String(500), nullable=True)  # New field
    
    def to_dict(self):
        return {
            "Article_ID": self.Article_ID,
            "Title": self.Title,
            "Content": self.Content,
            "Category_ID": self.Category_ID,
            "URL": self.URL
        }
    
    