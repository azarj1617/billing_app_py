from flask import Flask
from register_blue_print import register_blueprints
from config import Config
from extensions import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # ✅ Register blueprint with prefix
    register_blueprints(app)
    # Debug: list all routes
    print(app.url_map)

    return app

# if __name__ == '__main__':
#     app = create_app()
#     app.run(debug=True)
