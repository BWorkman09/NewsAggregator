from flask import jsonify, request, Blueprint
import api.services as services
from datetime import datetime
import sqlite3
from .models import User, db
from sqlalchemy.exc import IntegrityError
import re

api_bp = Blueprint('api', __name__)

@api_bp.route('/')
def home():
    """
    Just a generic endpoint that we can use to test if the API is running.

    Returns:
        str: A timestamp string indicating the current time, alogn with a message.
    """
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') # Get the current time
    welcome_message = f'Welcome to the User API!  The current time: {current_time}'
    return welcome_message, 200

@api_bp.route('/connection')
def test_connection():
    """
    Test the database connection.

    Returns:
        tuple: A tuple containing a JSON response with a message and an HTTP status code.
    """
    services.get_db_connection()
    return jsonify({'message': 'Successfully connected to the API'}), 200


# ---------------------------------------------------------
# Users 
# ---------------------------------------------------------

@api_bp.route('/users')
def get_users():
    """
    Retrieve a list of users with optional limit and name filter parameters.
   
    Query Parameters:
        limit (int): Maximum number of users to retrieve
        name (str): Filter users by name
        starts_with (bool): If True, filter names starting with the provided value,
                          if False, filter names containing the provided value
   
    Returns:
        tuple: A tuple containing a JSON response with users and an HTTP status code 200.
    """
    # Get query parameters
    limit = request.args.get('limit', default=None, type=int)
    name_filter = request.args.get('name', default=None, type=str)
    starts_with = request.args.get('starts_with', default=True, type=bool)
   
    # Get users based on filters
    if name_filter:
        user_list = services.get_users_by_name(name_filter, starts_with)
    else:
        # Add a default limit if none is provided
        default_limit = 100  # or whatever number makes sense for your application
        user_list = services.get_all_users(limit or default_limit)
   
    # Handle case where user_list is None or contains None values
    if user_list is None:
        user_list = []
    else:
        # Filter out any None values and convert valid users to dict
        user_dict_list = [user.to_dict() for user in user_list if user is not None]
    
    return jsonify(user_dict_list), 200

@api_bp.route('/users', methods=['POST'])
def create_user_route():
    """
    Create a new user via POST request.
    Expects JSON data with 'Name' and 'Email' fields.
    """
    try:
        data = request.get_json()
       
        if not data:
            return jsonify({'error': 'No data provided'}), 400
           
        name = data.get('Name')
        email = data.get('Email')
       
        if not name or not email:
            return jsonify({'error': 'Name and Email are required'}), 400
       
        # Check if user already exists
        existing_user = User.query.filter_by(Email=email).first()
        if existing_user:
            return jsonify({'error': 'Email already exists'}), 409
           
        # Create new user with automatic ID generation
        new_user = User(Name=name, Email=email)
        db.session.add(new_user)
        db.session.flush()  # Flush the session to get the ID
       
        # Get the user data before commit
        user_data = new_user.to_dict()
       
        db.session.commit()
       
        return jsonify({
            'message': 'User created successfully',
            'user': user_data
        }), 201
       
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({
            'error': 'Database integrity error',
            'message': 'Email must be unique'
        }), 409
       
    except Exception as e:
        db.session.rollback()
        print(f"Error creating user: {str(e)}")  # For debugging
        return jsonify({
            'error': 'Failed to create user',
            'message': str(e)
        }), 500

@api_bp.route('/users/<string:user_id>', methods=['DELETE'])
def delete_user_route(user_id):
    """
    Delete a user via DELETE request.
    Expects user_id in format XX-XXXXXXX
    """
    try:
        # Validate user_id format
        if not user_id or not isinstance(user_id, str) or not re.match(r'^\d{2}-\d{7}$', user_id):
            return jsonify({
                'error': 'Invalid user ID format',
                'message': 'User ID must be in format XX-XXXXXXX'
            }), 400

        # Check if user exists
        user = User.query.filter_by(User_ID=user_id).first()
        if not user:
            return jsonify({
                'error': 'User not found',
                'message': f'No user found with ID {user_id}'
            }), 404

        # Delete user and their preferences (will cascade if set up in model)
        db.session.delete(user)
        db.session.commit()

        return jsonify({
            'message': 'User deleted successfully',
            'user_id': user_id
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error deleting user: {str(e)}")  # For debugging
        return jsonify({
            'error': 'Failed to delete user',
            'message': str(e)
        }), 500
    

# ---------------------------------------------------------
# Category 
# ---------------------------------------------------------

@api_bp.route('/categories')
def get_categories():
    """
    Retrieve a list of categories with an optional limit parameter.
    
    Returns:
        tuple: A tuple containing a JSON response with categories and an HTTP status code 200.
    """
    # Get the 'limit' parameter from the URL if provided, otherwise None for all records
    limit = request.args.get('limit', default=None, type=int)
    
    # Get categories from the service with the specified limit
    category_list = services.get_all_categories(limit)
    
    # Convert the list of Category objects to a list of dictionaries for JSON serialization
    category_dict_list = [category.to_dict() for category in category_list]
    return jsonify(category_dict_list), 200
    


# ---------------------------------------------------------
# Article
# ---------------------------------------------------------
@api_bp.route('/articles')
def get_articles():
    """
    Retrieve a list of articles with an optional limit parameter.
   
    Query Parameters:
        limit (int): Maximum number of articles to retrieve
   
    Returns:
        tuple: A tuple containing a JSON response with articles and an HTTP status code 200.
    """
    # Get the 'limit' parameter from the URL if provided, otherwise use default limit
    limit = request.args.get('limit', default=250, type=int)
   
    try:
        # Get articles from the service with the specified limit
        article_list = services.get_all_articles(limit)
       
        # Convert the list of Article objects to a list of dictionaries
        article_dict_list = []
        for article in article_list:
            article_dict = {
                "Article_ID": article.Article_ID,
                "Title": str(article.Title),
                "Content": str(article.Content),
                "Category_ID": article.Category_ID,
                "URL": str(article.URL) if article.URL else None
            }
            article_dict_list.append(article_dict)
       
        response = jsonify(article_dict_list)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 200
       
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@api_bp.route('/articles/by-category-name')
def get_articles_by_category_name():
    """
    Retrieve a list of articles filtered by category name.
    
    Query Parameters:
        category (str): Name of the category to filter by
        limit (int): Maximum number of articles to retrieve (default: 250)
    
    Returns:
        tuple: A tuple containing a JSON response with filtered articles and an HTTP status code 200.
    """
    category_name = request.args.get('category', default=None, type=str)
    limit = request.args.get('limit', default=250, type=int)
    
    try:
        # Get articles from service
        article_list = services.get_articles_by_category_name(category_name, limit)
        
        # Convert the results to a list of dictionaries
        article_dict_list = []
        for article, category in article_list:
            article_dict = {
                "Article_ID": article.Article_ID,
                "Title": str(article.Title),
                "Content": str(article.Content),
                "Category_ID": article.Category_ID,
                "URL": str(article.URL) if article.URL else None,
                "Category": str(category.Category),
                "Description": str(category.Description)
            }
            article_dict_list.append(article_dict)
        
        response = jsonify(article_dict_list)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/articles', methods=['POST'])
def create_article():
    """
    Create a new article.
    
    Request Body:
        {
            "title": "Article Title",
            "content": "Article Content",
            "category_id": 1,
            "url": "https://example.com/article" (optional)
        }
    
    Returns:
        tuple: A tuple containing a JSON response with the created article and HTTP status code 201.
    """
    data = request.get_json()

# ---------------------------------------------------------
# User Preference
# ---------------------------------------------------------
@api_bp.route('/user_preferences')
def get_user_preferences():
   """
   Retrieve a list of user preferences with optional limit parameter.
   Returns:
       tuple: A tuple containing a JSON response with user preferences and an HTTP status code 200.
   """
   # Get the 'limit' parameter from the URL if provided, otherwise None for all records
   limit = request.args.get('limit', default=None, type=int)
  
   # Get user preferences from service
   user_preferences_list = services.get_all_user_preferences(limit)
  
   # Convert the list of UserPreference objects to dictionaries
   user_preferences_dict_list = [preference.to_dict() for preference in user_preferences_list]
   return jsonify(user_preferences_dict_list), 200



#print("Available functions in services:", [func for func in dir(services) if callable(getattr(services, func)) and not func.startswith("_")])



