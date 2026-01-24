import hashlib
from flask import Blueprint
from Services.UserService import get_users_data
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token,create_refresh_token,jwt_required,get_jwt_identity
from werkzeug.security import check_password_hash
from models.user_model import User
from models.response_model import ResponseModel

# ✅ Create a Blueprint
auth_bp = Blueprint('auth_bp', __name__,url_prefix='/auth')

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    
    auth_fields = User.auth_data_map(data)
   
    username = auth_fields.get("user_name")
    password = auth_fields.get("user_password")

    if not username or not password:
        return jsonify({"msg": "Username and password required"}), 400

    user = User.query.filter_by(user_name=username).first()
    hashed_input = hashlib.sha256(password.encode()).hexdigest()
   
    if not user or not user.user_password == hashed_input:
        res = ResponseModel(
        status="FAILURE",
        statusCode=200,
        message="Invalid credentials")
        return jsonify(res.__dict__), 201 

    if not user.user_status ==1:
        res = ResponseModel(
        status="FAILURE",
        statusCode=200,
        message="User is inactive")
        return jsonify(res.__dict__), 201

    # ✅ Create JWT (store user id inside token)
    access_token = create_access_token(identity=user.user_id)
    refresh_token = create_refresh_token(identity=user.user_id)
    res = ResponseModel(
        status="SUCCESS",
        statusCode=200,
        message="Login successfully",
        data={
        "accessToken": access_token,
        "refreshToken":refresh_token
        })
    return jsonify(res.__dict__), 201

@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity() # from refresh token
    new_access_token = create_access_token(identity=user_id)
    return jsonify(access_token=new_access_token), 200
