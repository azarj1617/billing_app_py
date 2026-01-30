from flask import Blueprint, jsonify, request
from Services.CustomerService import get_customers_data, save_customer_serv,search_customers_data
from models.customer_model import Customer
from models.response_model import ResponseModel
# ✅ Create a Blueprint
customer_bp = Blueprint('customer_bp', __name__,url_prefix='/customers')

@customer_bp.route('/get-all-customers', methods=['GET'])
def get_customers():
    status = request.args.get('status', type=int)
    return get_customers_data(status)

@customer_bp.route('/search-customer-data', methods=['GET'])
def search_customer_data():
    searchTerm = request.args.get('searchTerm', type=str)
    status = request.args.get('status', type=int)
    return search_customers_data(searchTerm,status) 

@customer_bp.route('/save-customer',methods=['POST'])
def save_customer():
    data = request.get_json()
    return save_customer_serv(data)