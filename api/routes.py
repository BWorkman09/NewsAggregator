from flask import jsonify, request, Blueprint
import api.services as services
from api.services import update_user_name, update_user_preference, delete_user_preference, get_user_preference_stats
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
    
@api_bp.route('/users/<string:user_id>', methods=['PUT'])
def update_user_route(user_id):
    """
    Update a user's name via PUT request.
    Expects JSON data with 'Name' field.
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'No data provided',
                'message': 'Request body is required'
            }), 400
            
        new_name = data.get('Name')
        if not new_name:
            return jsonify({
                'error': 'Name is required',
                'message': 'Name field must be provided'
            }), 400

        updated_user = update_user_name(user_id, new_name)
        
        return jsonify({
            'message': 'User updated successfully',
            'user': updated_user
        }), 200

    except ValueError as e:
        return jsonify({
            'error': 'Validation error',
            'message': str(e)
        }), 400
    except Exception as e:
        print(f"Error updating user: {str(e)}")  # For debugging
        return jsonify({
            'error': 'Failed to update user',
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
    limit = request.args.get('limit', default=250, type=int)
    
    try:
        article_list = services.get_all_articles(limit)
        
        article_dict_list = []
        for article, category in article_list:
            article_dict = {
                "Title": str(article.Title),
                "Content": str(article.Content),
                "URL": str(article.URL) if article.URL else None,
                "Authors": str(article.Authors) if article.Authors else None,
                "Category": str(category.Category),
                "Description": str(category.Description)
            }
            article_dict_list.append(article_dict)
        
        response = jsonify(article_dict_list)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/articles/by-category-name')
def get_articles_by_category_name():
    category_name = request.args.get('category', default=None, type=str)
    limit = request.args.get('limit', default=250, type=int)
    
    try:
        article_list = services.get_articles_by_category_name(category_name, limit)
        
        article_dict_list = []
        for article, category in article_list:
            article_dict = {
                "Title": str(article.Title),
                "Content": str(article.Content),
                "URL": str(article.URL) if article.URL else None,
                "Authors": str(article.Authors) if article.Authors else None,
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
    limit = request.args.get('limit', default=None, type=int)
    
    user_preferences_with_categories = services.get_all_user_preferences(limit)
    
    user_preferences_dict_list = [
        {
            "User_ID": pref[0].User_ID,
            "Category_ID": pref[0].Category_ID,  # Will return something like "ENL501"
            "Category": pref[1]  # Will return something like "SPORTS"
        }
        for pref in user_preferences_with_categories
    ]
    
    return jsonify(user_preferences_dict_list), 200


@api_bp.route('/user_preferences/<string:user_id>', methods=['PUT'])
def update_user_preference_route(user_id):
    """
    Update a user's preference via PUT request.
    Expects JSON data with 'Category_ID' field.
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'No data provided',
                'message': 'Request body is required'
            }), 400
            
        category_id = data.get('Category_ID')
        if not category_id:
            return jsonify({
                'error': 'Category_ID is required',
                'message': 'Category_ID field must be provided'
            }), 400

        updated_preference = update_user_preference(user_id, category_id)
        
        if updated_preference:
            return jsonify({
                'message': 'User preference updated successfully',
                'preference': updated_preference
            }), 200
        else:
            return jsonify({
                'error': 'Failed to update preference',
                'message': 'Unable to create or update preference'
            }), 500

    except ValueError as e:
        return jsonify({
            'error': 'Validation error',
            'message': str(e)
        }), 400
    except Exception as e:
        print(f"Error updating user preference: {str(e)}")  # For debugging
        return jsonify({
            'error': 'Failed to update user preference',
            'message': str(e)
        }), 500

@api_bp.route('/user_preferences/<string:user_id>/<string:category_id>', methods=['DELETE'])
def delete_user_preference_route(user_id, category_id):
    """
    Delete a specific user preference via DELETE request.
    """
    try:
        # Validate user_id format
        if not user_id or not isinstance(user_id, str) or not re.match(r'^\d{2}-\d{7}$', user_id):
            return jsonify({
                'error': 'Invalid user ID format',
                'message': 'User ID must be in format XX-XXXXXXX'
            }), 400

        # Check if preference was deleted
        if delete_user_preference(user_id, category_id):
            return jsonify({
                'message': 'User preference deleted successfully',
                'user_id': user_id,
                'category_id': category_id
            }), 200
        else:
            return jsonify({
                'error': 'Preference not found',
                'message': f'No preference found for user {user_id} and category {category_id}'
            }), 404

    except ValueError as e:
        return jsonify({
            'error': 'Validation error',
            'message': str(e)
        }), 400
    except Exception as e:
        print(f"Error deleting user preference: {str(e)}")  # For debugging
        return jsonify({
            'error': 'Failed to delete user preference',
            'message': str(e)
        }), 500

@api_bp.route('/user-preferences/stats')
def get_preference_statistics():
    """
    Get statistics about user preferences.
    Returns:
        JSON response with category counts and HTTP status 200
    """
    try:
        stats = services.get_user_preference_stats()
        response = jsonify(stats)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#print("Available functions in services:", [func for func in dir(services) if callable(getattr(services, func)) and not func.startswith("_")])



