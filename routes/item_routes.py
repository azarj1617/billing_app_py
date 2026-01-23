from flask import Blueprint, jsonify, request
from Services.ItemService import get_items_by_id_serv, get_items_serv, insert_item_serv, search_items_serv, update_item_serv

# ✅ Create a Blueprint
item_bp = Blueprint('item_bp', __name__,url_prefix='/items')

@item_bp.route('/get-all-items', methods=['GET'])
def get_items():
    status = request.args.get('status', type=int)
    return get_items_serv(status)

@item_bp.route('/get-item-details', methods=['GET'])
def get_item_by_id():
    itemId = request.args.get('itemId', type=int)
    return get_items_by_id_serv(itemId)


@item_bp.route('/search-items', methods=['GET'])
def search_items():
    searchTerm = request.args.get('searchTerm', type=str)
    status = request.args.get('status', type=int)
    type = request.args.get('type', type=str)
    return search_items_serv(searchTerm,status,type)

@item_bp.route('/insert-item', methods=['POST'])
def insert_item():
    data = request.get_json()
    return insert_item_serv(data)

@item_bp.route('/update-item', methods=['POST'])
def update_item():
    data = request.get_json()
    return update_item_serv(data)