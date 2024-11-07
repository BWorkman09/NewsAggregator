from flask import jsonify, request, Blueprint
import api.services as services
from api.models import User, create_user_from_dict
from datetime import datetime


api_bp = Blueprint("api", __name__)

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



@api_bp.route("/users", methods=["GET"])
def get_users():
    """
    Retrieve a list of all users or filter users by name.
    If the query string parameter "starts_with" is provided, filter users by name.
    If the query string parameter "contains" is provided, filter users by name containing the string.

    Returns:
        tuple: A tuple containing a JSON response with all users and an HTTP status code 200.
    """
    # Example: /api/users?starts_with=A
    # Example: /api/users?contains=John
    # Example: /api/users
    
    # Get the query string parameter "starts_with" from the request if it's there
    user_name = request.args.get("starts_with")  # Accessing query string parameter
    # If user_name is not provided
    if not user_name:
        # See if the query string parameter "contains" is provided
        contains_user_name = request.args.get("contains")
        if contains_user_name:
            user_list = services.get_users_by_name(contains_user_name, starts_with=False)
        # If neither "starts_with" nor "contains" is provided, get all users
        else:
            user_list = services.get_all_users()
    else:
        # If user_name is provided, filter users by name
        user_list = services.get_users_by_name(user_name)

    # Convert the list of User objects to a list of dictionaries so that we can jsonify it
    user_dict_list = [user.to_dict() for user in user_list]
    return jsonify(user_dict_list), 200

