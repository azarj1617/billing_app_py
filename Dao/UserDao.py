from flask import jsonify
from models.user_model import User
from extensions import db

users = []

def get_all_users():
    users = User.query.all()  # fetch all users from MySQL
    return jsonify([u.to_dict() for u in users])