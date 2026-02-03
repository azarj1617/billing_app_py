from datetime import datetime
from operator import and_, or_
import traceback
from flask import jsonify
from extensions import db
from models.response_model import ResponseModel
from models.sales.sales_model import SalesMaster
from sqlalchemy import func, desc
salesList = []

def get_bill_by_id_dao(salesId):
    saleData = (
        SalesMaster.query
        .filter(SalesMaster.sales_id == salesId)
        .order_by(desc(SalesMaster.bill_seq))
        .first()
        )
    return jsonify(saleData.to_sales_dict() if saleData else None)
