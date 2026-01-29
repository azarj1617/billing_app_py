from datetime import datetime
from operator import and_, or_
import traceback
from flask import jsonify
from extensions import db
from models.quote_details_model import QuoteDetails
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
                ).order_by(desc(QuoteMaster.quote_seq_no)).all()
    return jsonify([u.to_quote_dict() for u in quotesList])

def get_quote_by_id_dao(quoteId):
    quote = (
        QuoteMaster.query
        .filter(QuoteMaster.quote_id == quoteId)
        .order_by(desc(QuoteMaster.quote_seq_no))
        .first()
        )
    return jsonify(quote.to_quote_dict() if quote else None)

def get_quote_no_dao():
    latest_quote = (
        QuoteMaster.query
        .filter(func.date(QuoteMaster.quote_date) == datetime.today().replace(hour=0, minute=0, second=0, microsecond=0))
        .order_by(desc(QuoteMaster.quote_seq_no))
        .first()
        )
    return latest_quote

def save_quote_dao(quoteData):
    try: 
        quoteFields = QuoteMaster.map_quote_data_to_model(quoteData)
        quote = QuoteMaster(**quoteFields)
        latest_quote = get_quote_no_dao()
        latestSeqNo = latest_quote.quote_seq_no if latest_quote else 0 
        quoteSeqNo = latestSeqNo+1
        quote.quote_seq_no = quoteSeqNo
        now = datetime.now()
        dateSeq = now.strftime("%Y%m%d")
        latestQuoteNum = "QUO/"+dateSeq+"/"+str(quoteSeqNo)
        quote.quote_no = latestQuoteNum
        dailyQuoteNo = "QUO/"+str(quoteSeqNo)
        quote.daily_seq_no = dailyQuoteNo
        db.session.add(quote)
        db.session.flush()

        for p in quoteData.get("details", []):
            price = QuoteDetails(**QuoteDetails.map_quote_detail_write(p))
            if quoteData.get("priceDetails") and len(quoteData["priceDetails"]) > 0:
                price.price_id = quoteData["priceDetails"][0].get("priceId")
            else:
                price.price_id = None
            quote.details.append(price)
            
            db.session.commit()
            res = ResponseModel(
            status="SUCCESS",
            statusCode=200,
            message= "Quote Data Saved Successfully" 
            )
            return jsonify(res.__dict__), 201
    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        res = ResponseModel(
        status="FAILURE",
        statusCode=200,
        message="OOPS! Something went wrong"
        )
        return jsonify(res.__dict__)