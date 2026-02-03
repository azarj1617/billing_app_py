from flask import Blueprint, jsonify, request
from Services.SalesService import get_bill_by_id_serv
from models.response_model import ResponseModel
# ✅ Create a Blueprint
sales_bp = Blueprint('sales_bp', __name__,url_prefix='/sales')

@sales_bp.route('/get-bill-by-id', methods=['GET'])
def get_bill_by_id():
    salesId = request.args.get('salesId', type=int)
    return get_bill_by_id_serv(salesId)


# @quotes_bp.route('/getQuotesByDate', methods=['POST'])
# def get_quotes_by_date():
#     data = request.get_json()
#     return get_quotes_by_date_serv(data)

# @quotes_bp.route('/getQuoteById', methods=['GET'])
# def get_quotes_by_id():
#     quoteId = request.args.get('quoteId', type=int)
#     return get_quote_by_id_serv(quoteId)

# @quotes_bp.route('/get-quote-number', methods=['GET'])
# def get_quote_no():
#     resp = dict(quoteNo=get_quote_no_serv())
#     return jsonify(resp)

# @quotes_bp.route('/saveQuote', methods=['POST'])
# def save_quote():
#     data = request.get_json()
#     return save_quote_serv(data)

