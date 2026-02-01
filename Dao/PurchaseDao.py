from datetime import datetime
from decimal import Decimal
from operator import and_, or_
import traceback
from flask import jsonify
from models.purchase.purchase_details_model import PurchaseDetails
from models.purchase.purchase_model import PurchaseMaster
from models.response_model import ResponseModel
from extensions import db
from models.stock_ledger import StockLedger
from models.stock_model import StockMaster
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
            update_stock_master(details,p)  
            update_stock_ledger(details,p)                     
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
    
def update_stock_master(details,p):
     # Get existing stock row for item
            stock = StockMaster.query.filter(
                StockMaster.item_id == details.item_id
            ).with_for_update().first()

            if stock:
                # Update existing stock
                stock.current_qty = (stock.current_qty or Decimal('0')) + Decimal(details.purchase_qty)
            else:
                # Create new stock row
                stock = StockMaster(
                    **StockMaster.map_stock_data_to_model(p)
                )      
                stock.current_qty = details.purchase_qty
                db.session.add(stock)  

def update_stock_ledger(details,p):
     
                stock_txn = StockLedger(
                    **StockLedger.map_stock_txn_data_to_model(p)
                )      

                stock_txn.referenceId = details.purchase_id
                stock_txn.txn_type = "PURCHASE"
                stock_txn.qty_in = details.purchase_qty
                stock_txn.rate = details.purchase_price
                db.session.add(stock_txn)  