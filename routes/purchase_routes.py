from flask import Blueprint, jsonify, request
from Services.PurchaseService import get_purchase_data_serv, save_purchase_serv
from Services.StockService import get_all_stocks_serv

# ✅ Create a Blueprint
purchase_bp = Blueprint('purchase_bp', __name__,url_prefix='/purchase')

@purchase_bp.route('/get-purchase-data', methods=['GET'])
def get_purchase_data():
    return get_purchase_data_serv()

@purchase_bp.route('/savePurchase', methods=['POST'])
def save_purchase():
    purchaseData = request.get_json()
    return save_purchase_serv(purchaseData)