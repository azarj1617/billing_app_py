from datetime import timedelta
from flask import Flask
from flask.cli import load_dotenv
from register_blue_print import register_blueprints
from protect_routes import protect_routes
from config import Config
from extensions import db
import os
from flask_jwt_extended import JWTManager
from flask_cors import CORS

def create_app():
    load_dotenv()
    app = Flask(__name__)
    CORS(
    app,
    resources={r"/*": {"origins": ["http://localhost:4200"]}},
    supports_credentials=True,
    allow_headers=["Content-Type", "Authorization"],
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )
    app.config.from_object(Config)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "super-secret-default-key")
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY',"super-jwt-secret-key")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30) # short-lived
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30) # long-lived
    JWTManager(app)
    db.init_app(app)

    # ✅ Register blueprint with prefix
    register_blueprints(app)
    
    # Register global route protection
    protect_routes(app)

    # Debug: list all routes
    print(app.url_map)

    return app

# if __name__ == '__main__':
#     app = create_app()
#     app.run(debug=True)
