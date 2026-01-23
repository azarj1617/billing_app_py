from routes.user_routes import user_bp
from routes.customer_routes import customer_bp
from routes.item_routes import item_bp

def register_blueprints(app):
# ✅ Register blueprint with prefix
    app.register_blueprint(user_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(item_bp)