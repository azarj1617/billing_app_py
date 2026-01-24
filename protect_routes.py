from flask import request, jsonify
from flask_jwt_extended import jwt_required

def protect_routes(app):
    # -------------------------
    # Global JWT protection
    # -------------------------
    @app.before_request
    def protected_routes():
        # ✅ MUST allow preflight
        if request.method == "OPTIONS":
            return "", 200


        # ✅ Allow auth routes (VERY IMPORTANT)
        if "/auth/" in request.path:
            return None # Skip JWT check
       
        # Enforce JWT check
        try:
            jwt_required()(lambda: None)()
        except Exception as e:
            return jsonify({"msg": str(e)}), 401