from flask import jsonify, request, Blueprint
import api.services as services
from api.models import User, create_user_from_dict
from datetime import datetime



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

