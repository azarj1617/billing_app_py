from operator import and_, or_
import traceback
from flask import jsonify
from models.response_model import ResponseModel
from extensions import db
from models.stock_model import StockMaster
stockList = []

def get_all_stocks_dao():
    stockList = StockMaster.query.all()
    return jsonify([u.stock_to_dict() for u in stockList])
