from datetime import datetime
from operator import and_, or_
import traceback
from flask import jsonify
from extensions import db
from models.quotes_model import QuoteMaster
from models.response_model import ResponseModel
from sqlalchemy import func, desc
quotesList = []

def get_all_quotes_dao():
    quotesList = QuoteMaster.query.all() 
    return jsonify([u.to_quote_dict() for u in quotesList])

def get_quotes_by_date_dao(data):
    start_date = data.get("startDate")
    end_date = data.get("endDate")
    quotesList = QuoteMaster.query.filter(
                 QuoteMaster.quote_date >= start_date,
                 QuoteMaster.quote_date <= end_date
                ).all()
    return jsonify([u.to_quote_dict() for u in quotesList])

def get_quote_by_id_dao(quoteId):
    quotesList = QuoteMaster.query.filter(
                 QuoteMaster.quote_id == quoteId
                ).all()
    return jsonify([u.to_quote_dict() for u in quotesList])

def get_quote_no_dao():
    latest_quote = (
        QuoteMaster.query
        .filter(func.date(QuoteMaster.quote_date) == datetime.today().replace(hour=0, minute=0, second=0, microsecond=0))
        .order_by(desc(QuoteMaster.quote_seq_no))
        .first()
        )
    return latest_quote