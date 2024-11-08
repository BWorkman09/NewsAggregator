import bcrypt
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
from datetime import date
import os
import random

# Initialize the Flask app
app = Flask(__name__)

# Database configuration
DATABASE_PATH = Path(__file__).parents[1] / "data" / "News_Aggregator.db"
DATABASE_URI = f"sqlite:///{DATABASE_PATH}"
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the database connection
db = SQLAlchemy(app)

# Define the database models

class User(db.Model):
    __tablename__ = 'User'
    User_ID = db.Column(db.String(100), primary_key=True) 
    Name = db.Column(db.String(100), nullable=False)
    Email = db.Column(db.String(100), nullable=False)
    Password_hash = db.Column(db.String(60), nullable=False)

    def to_dict(self):
        return {"User_ID": self.User_ID, "Name": self.Name, "Email": self.Email}


class User_Preference(db.Model):
    __tablename__ = 'User_Preference'
    User_ID = db.Column(db.String, db.ForeignKey('User.User_ID'), primary_key=True, nullable=False)
    Category_ID = db.Column(db.Integer, db.ForeignKey('Category.Category_ID'), primary_key=True, nullable=False)

    def to_dict(self):
        return {
            "User_ID": self.User_ID,
            "Category_ID": self.Category_ID
        }

class Category(db.Model):
    __tablename__ = 'Category'
    Category_ID = db.Column(db.Integer, primary_key=True)
    Category = db.Column(db.String(100), nullable=False)
    Description = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {"Category_ID": self.Category_ID, "Category": self.Category, "Description": self.Description}


class Article(db.Model):
    __tablename__ = 'Article'
    Article_ID = db.Column(db.Integer, primary_key=True)
    URL = db.Column(db.String(200), nullable= False)
    Source_ID = db.Column(db.String(100), nullable=False)
    Title = db.Column(db.String(200), nullable=False)
    Category = db.Column(db.String(100), nullable=False)
    Category_ID = db.Column(db.Integer, db.ForeignKey('Category.Category_ID'), nullable=False)
    Content = db.Column(db.Text, nullable=False)
    Authors = db.Column(db.String(100), nullable=False)
    Date = db.Column(db.Date, nullable=False, default=date.today)

    def to_dict(self):
        """
        Convert the Article object to a dictionary for easy JSON serialization.
        """
        return {
            "Article_ID": self.Article_ID,
            "URL": self.URL,
            "Source_ID": self.Source_ID,
            "Title": self.Title,
            "Category": self.Category,
            "Category_ID": self.Category_ID,
            "Content": self.Content,
            "Authors": self.Authors,
            "Date": self.Date.isoformat()  # Convert date to ISO 8601 string format
        }
# Create tables
with app.app_context():
    db.create_all()