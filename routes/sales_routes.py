from flask import Blueprint, jsonify, request
from Services.SalesService import get_bill_by_date_serv, get_bill_by_id_serv, get_latest_bill_no_serv, save_sales_serv
from models.response_model import ResponseModel
# ✅ Create a Blueprint
sales_bp = Blueprint('sales_bp', __name__,url_prefix='/sales')

@sales_bp.route('/get-bill-by-id', methods=['GET'])
def get_bill_by_id():
    salesId = request.args.get('salesId', type=int)
    return get_bill_by_id_serv(salesId)


@sales_bp.route('/get-bills-by-date', methods=['POST'])
def get_quotes_by_date():
    data = request.get_json()
    return get_bill_by_date_serv(data)

@sales_bp.route('/get-latest-bill-no', methods=['GET'])
def get_latest_bill_no():
    return get_latest_bill_no_serv()


@sales_bp.route('/saveSales', methods=['POST'])
def save_sales_data():
    data = request.get_json()
    return save_sales_serv(data)