from flask import Blueprint, jsonify, request
from Services.QuoteService import get_all_quotes_serv, get_quotes_by_date_serv, get_quote_by_id_serv
from models.response_model import ResponseModel
# ✅ Create a Blueprint
quotes_bp = Blueprint('quotes_bp', __name__,url_prefix='/quotes')

@quotes_bp.route('/get-quotes', methods=['GET'])
def get_all_quotes():
    return get_all_quotes_serv()

@quotes_bp.route('/getQuotesByDate', methods=['GET'])
def get_quotes_by_date():
    data = request.get_json()
    return get_quotes_by_date_serv(data)

@quotes_bp.route('/getQuoteById', methods=['GET'])
def get_quotes_by_id():
    quoteId = request.args.get('quoteId', type=int)
    return get_quote_by_id_serv(quoteId)