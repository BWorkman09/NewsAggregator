from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'  # Fixed: double underscores
    User_ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    preferences = db.relationship('UserPreference', backref='user', lazy=True)
   
    def to_dict(self):
        return {
            "User_ID": self.User_ID,
            "Name": self.Name
        }
   
class UserPreference(db.Model):
    __tablename__ = 'user_preference'  # Fixed: convention is lowercase with underscore
    ID = db.Column(db.Integer, primary_key=True)
    User_ID = db.Column(db.Integer, db.ForeignKey('user.User_ID'), nullable=False)  # Fixed: reference to correct table and column
    Category_ID = db.Column(db.Integer, db.ForeignKey('category.Category_ID'), nullable=False)  # Fixed: reference to correct table
    
    def to_dict(self):
        return {
            "ID": self.ID,  # Fixed: using correct attribute name
            "User_ID": self.User_ID, 
            "Category_ID": self.Category_ID
        }
   
class Category(db.Model):
    __tablename__ = 'category'  # Fixed: lowercase convention
    Category_ID = db.Column(db.Integer, primary_key=True)
    Category = db.Column(db.String(100), nullable=False)
    Description = db.Column(db.String(100), nullable=False)
    articles = db.relationship('Article', backref='category', lazy=True)  # Added relationship
    
    def to_dict(self):
        return {
            "Category_ID": self.Category_ID,
            "Category": self.Category,
            "Description": self.Description
        }

class Article(db.Model):
    __tablename__ = 'article'  # Fixed: lowercase convention
    Article_ID = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(200), nullable=False)
    Content = db.Column(db.Text, nullable=False)
    Category_ID = db.Column(db.Integer, db.ForeignKey('category.Category_ID'), nullable=False)  # Fixed: reference to correct table
    Author = db.Column(db.String(100), nullable=False)
    
    def to_dict(self):
        return {
            "Article_ID": self.Article_ID,
            "Title": self.Title,
            "Content": self.Content,
            "Category_ID": self.Category_ID,
            "Author": self.Author
        }