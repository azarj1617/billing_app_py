from flask import request, jsonify
from flask_jwt_extended import jwt_required

def protect_routes(app):
    # -------------------------
    # Global JWT protection
    # -------------------------
    @app.before_request
    def protected_routes():
        # List of public routes that don't require JWT
        public_routes = ["/auth/login", "/refresh"]

        if request.path in public_routes:
            return  # Skip JWT check

        # Enforce JWT check
        try:
            jwt_required()(lambda: None)()
        except Exception as e:
            return jsonify({"msg": str(e)}), 401