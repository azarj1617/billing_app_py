from routes.user_routes import user_bp
from routes.customer_routes import customer_bp
from routes.item_routes import item_bp
from routes.auth_routes import auth_bp
from routes.quotes_routes import quotes_bp
from routes.stock_routes import stock_bp
from routes.purchase_routes import purchase_bp
def register_blueprints(app):
# ✅ Register blueprint with prefix
    app.register_blueprint(user_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(item_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(quotes_bp)
    app.register_blueprint(stock_bp)
    app.register_blueprint(purchase_bp)