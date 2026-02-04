from flask import Blueprint, jsonify, request
from Services.StockService import get_all_stocks_serv

# ✅ Create a Blueprint
stock_bp = Blueprint('stock_bp', __name__,url_prefix='/stocks')

@stock_bp.route('/get-all-stock', methods=['GET'])
def get_all_stocks():
    return get_all_stocks_serv()
