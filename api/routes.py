from flask import jsonify, request, Blueprint
import api.services as services
from datetime import datetime


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


@api_bp.route('/users')
def get_users():
    """
    Retrieve a list of all users.
    Returns:
        tuple: A tuple containing a JSON response with all users and an HTTP status code 200.
    """
    # Example: /api/all-users
    
    # Get all users from the service
    user_list = services.get_all_users()
    
    # Convert the list of User objects to a list of dictionaries so that we can jsonify it
    user_dict_list = [user.to_dict() for user in user_list]
    return (jsonify(user_dict_list), 200)