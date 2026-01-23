from flask import Blueprint
from Services.UserService import get_users_data

# ✅ Create a Blueprint
user_bp = Blueprint('user_bp', __name__,url_prefix='/users')


@user_bp.route('/get-all-users', methods=['GET'])
def get_users():
    return get_users_data()

@user_bp.route('/test', methods=['GET'])
def get_users1():
    return "Test"
    