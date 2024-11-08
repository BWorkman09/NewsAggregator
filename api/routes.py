import bcrypt
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import os
import random

# Define API endpoints
 GET /api/users - Get a list of users
@app.route('/api/users', methods=['GET'])
def get_users():
    limit = request.args.get('limit', 10)
    users = User.query.limit(limit).all()
    return jsonify([user.to_dict() for user in users]), 200

# GET/ api/users/<int:user_id>' - Get the user name
@app.route('/api/users/<string:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = User.query.get(user_id)
    
    if user:
        return jsonify(user.to_dict()), 200
    else:
        return jsonify({'message': 'User not found'}), 404

# GET/ api/users/name/<string:name>
@app.route('/api/users/name/<string:name>', methods=['GET'])
def get_users_by_name(name):
    users = User.query.filter(User.Name.ilike(f"%{name}%")).all() 
    
    if users:
        return jsonify([user.to_dict() for user in users]), 200
    else:
        return jsonify({'message': 'No users found with that name'}), 404


# POST /api/users - Add a new user
@app.route('/api/users', methods=['POST'])
def generate_user_id():
    prefixes = ["12", "34", "56", "78", "90"]
    prefix = random.choice(prefixes)
    suffix = str(random.randint(1000000, 9999999))
    return f"{prefix}-{suffix}"

def create_user():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    # Check if all required fields are present
    if not name or not email or not password:
        return jsonify({"error": "Name, Email, and Password are required"}), 400

    # Hash the password
    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    # Generate the custom User_ID
    user_id = generate_user_id()

    # Create a new User instance
    new_user = User(User_ID=user_id, Name=name, Email=email, Password_hash=password_hash)
    
    # Add to the session and commit to the database
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully", "User_ID": user_id}), 201

    # Add to the database
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "User creation failed", "details": str(e)}), 500


# DELETE /api/users/<string:user_id> - Delete a user
@app.route('/api/users/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error deleting user", "details": str(e)}), 500


# GET /api/articles - Get a list of articles
@app.route('/api/articles', methods=['GET'])
def get_articles():
    limit = request.args.get('limit',10)
    articles = Article.query.limit(limit).all()
    return jsonify([article.to_dict() for article in articles]), 200

# POST /api/articles - Add a new article
@app.route('/api/articles', methods=['POST'])
def add_article():
    data = request.json

    # Validate input data
    required_fields = ['URL', 'Source_ID', 'Title', 'Category', 'Content', 'Authors', 'Date']
    for field in required_fields:
        if field not in data:
            return {"error": f"Missing field: {field}"}, 400
    category_name = data['Category']
    category = Category.query.filter_by(Category=category_name).first()
    if not category:
        return {"error": "Invalid Category name"}, 400

    # Generate the next Article_ID, starting from 209627
    last_article = Article.query.order_by(Article.Article_ID.desc()).first()
    next_article_id = 209627 if not last_article else last_article.Article_ID + 1

    # Create a new Article object
    new_article = Article(
        Article_ID=next_article_id,
        URL=data['URL'],
        Source_ID=data['Source_ID'],
        Title=data['Title'],
        Category=category_name,
        Category_ID=category.Category_ID,
        Content=data['Content'],
        Authors=data['Authors'],
        Date=data['Date']  # Date should be in YYYY-MM-DD format
    )

    # Add and commit the new article to the database
    db.session.add(new_article)
    db.session.commit()

    return jsonify(new_article.to_dict()), 201

# GET /api/category - Get all categories
@app.route('/api/category', methods=['GET'])
def get_category():
    limit = request.args.get('limit',20)
    categories = Category.query.limit(limit).all()
    return jsonify([category.to_dict() for category in categories]), 200

# GET /api/user/<user_id>/preference - Fetch user preferences based on User_ID
@app.route('/api/user/<user_id>/preference', methods=['GET'])
def get_user_preferences(user_id):
    preferences = User_Preference.query.filter_by(User_ID=user_id).all()
    if not preferences:
        return jsonify({"error": "No preferences found for the given User ID"}), 404

    preferences_list = [preference.to_dict() for preference in preferences]
    return jsonify(preferences_list), 200
