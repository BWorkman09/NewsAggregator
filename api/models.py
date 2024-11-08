# Define the database models

class User(db.Model):
    __tablename__ = 'User'
    User_ID = db.Column(db.Integer, primary_key=True) 
    Name = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {"User_ID": self.User_ID, "Name": self.Name}


class UserPreference(db.Model):
    __tablename__ = 'User_Preference'
    ID = db.Column(db.Integer, primary_key=True)
    User_ID = db.Column(db.Integer, db.ForeignKey('User_ID'), nullable=False)
    Category_ID = db.Column(db.Integer, db.ForeignKey('Category_ID'), nullable=False)

    def to_dict(self):
        return {"ID": self.id, "User_ID": self.User_ID, "Category_ID": self.Category_ID}


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
    Title = db.Column(db.String(200), nullable=False)
    Content = db.Column(db.Text, nullable=False)
    Category_ID = db.Column(db.Integer, db.ForeignKey('Categories.id'), nullable=False)
    Author = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {"Article_ID": self.Article_ID, "Title": self.Title, "Content": self.Content, "Category_ID": self.Category_ID, "Author": self.Author}