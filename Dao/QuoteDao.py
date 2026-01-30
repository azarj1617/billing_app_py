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

def get_next_quote_seq_locked(session):
    # Lock the row with the highest sequence
    last_quote = (
        session.query(QuoteMaster)
        .filter(func.date(QuoteMaster.quote_date) == datetime.today().replace(hour=0, minute=0, second=0, microsecond=0))
        .order_by(QuoteMaster.quote_seq_no.desc())
        .with_for_update()   # 🔒 CRITICAL
        .first()
    )

    if last_quote:
        return last_quote.quote_seq_no + 1
    else:
        return 1

def save_quote_dao(quoteData):
    try: 
       
        db.session.begin()
        
        latest_quote = get_next_quote_seq_locked(db.session)
        
        quoteFields = QuoteMaster.map_quote_data_to_model(quoteData)
        quote = QuoteMaster(**quoteFields)

        # latestSeqNo = latest_quote.quote_seq_no if latest_quote else 0 
        quoteSeqNo = latest_quote
        quote.quote_seq_no = quoteSeqNo
        now = datetime.now()
        dateSeq = now.strftime("%Y%m%d")
        latestQuoteNum = "QUO/"+dateSeq+"/"+str(quoteSeqNo)
        quote.quote_no = latestQuoteNum
        dailyQuoteNo = "QUO/"+str(quoteSeqNo)
        quote.daily_seq_no = dailyQuoteNo
    
        db.session.add(quote)
       
        for p in quoteData.get("details", []):
            price = QuoteDetails(**QuoteDetails.map_quote_detail_write(p))
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
    
def update_quote_dao(quoteId, quoteData):
    try:
        db.session.begin() 
        quote = (
            db.session.query(QuoteMaster)
            .filter(QuoteMaster.quote_id == quoteId)
            .with_for_update()  
            .one_or_none()
        )

        if not quote:
            db.session.rollback()
            return jsonify({
                "status": "FAILURE",
                "message": "Quote not found"
            }), 404

        # Update master fields

        updated_fields = QuoteMaster.map_quote_data_to_model(quoteData)
        SKIP_FIELDS = {"quote_id", "quote_date","quote_no","quote_seq_no","quote_detail_id","daily_seq_no"}
        for key, value in updated_fields.items():
            if key not in SKIP_FIELDS:
                setattr(quote, key, value)

        existing_details = QuoteDetails.query.filter_by(quote_id=quoteId).all()
        existing_map = {d.quote_detail_id: d for d in existing_details}
        incoming_ids = set()

        for p in quoteData.get("details", []):
            detail_id = p.get("quoteDetailId")

            if detail_id and detail_id in existing_map:
                # ✅ UPDATE existing row
                detail = existing_map[detail_id]
                mapped = QuoteDetails.map_quote_detail_write(p)

                for k, v in mapped.items():
                     if k not in SKIP_FIELDS:
                        setattr(detail, k, v)

                incoming_ids.add(detail_id)

            else:
                # ✅ INSERT new row
                new_detail = QuoteDetails(**QuoteDetails.map_quote_detail_write(p))
                new_detail.quote_id = quoteId
                db.session.add(new_detail)
        for delId in quoteData.get("deleteIds", []):
            detail = existing_map.get(delId)
            if detail:
                db.session.delete(detail)
        # 5️⃣ Commit everything
        db.session.commit()

        return jsonify({
            "status": "SUCCESS",
            "message": "Quote updated successfully"
        }), 200

    except Exception:
        db.session.rollback()
        traceback.print_exc()
        return jsonify({
            "status": "FAILURE",
            "message": "OOPS! Something went wrong"
        }), 500