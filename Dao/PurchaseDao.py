from datetime import datetime
from operator import and_, or_
import traceback
from flask import jsonify
from models.purchase.purchase_details_model import PurchaseDetails
from models.purchase.purchase_model import PurchaseMaster
from models.response_model import ResponseModel
from extensions import db
from sqlalchemy import func, desc
purchaseEntries = []

def get_purchase_data_dao():
    purchaseEntries = PurchaseMaster.query.all()
    return jsonify([u.purchase_to_dict() for u in purchaseEntries])

def get_next_purchase_seq_locked(session):
    last_purchase_id = (
        session.query(PurchaseMaster)
        .order_by(PurchaseMaster.purchase_id.desc())
        .with_for_update()  
        .first()
    )
    print(last_purchase_id.purchase_id)
    if last_purchase_id:
        return last_purchase_id.purchase_id + 1
    else:
        return 1
    
def save_purchase_dao(purchaseData):
    try:  
        db.session.begin()
        
        latest_purchase_id = get_next_purchase_seq_locked(db.session)
        
        purchaseFields = PurchaseMaster.map_purchase_data_to_model(purchaseData)
        latestGRN = "GRN-"+datetime.now().strftime("%Y")+"-"+str(latest_purchase_id)
        purchase = PurchaseMaster(**purchaseFields)
        purchase.grn_code = latestGRN
        db.session.add(purchase)
        
        for p in purchaseData.get("purchaseDetails", []):
            details = PurchaseDetails(**PurchaseDetails.map_purchase_detail_data_to_model(p))
            purchase.purchaseDetails.append(details)
        
        db.session.commit()
        res = ResponseModel(
        status="SUCCESS",
        statusCode=200,
        message= "Purchase Data Saved Successfully" 
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