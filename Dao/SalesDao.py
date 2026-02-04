from datetime import datetime
from operator import and_, or_
import traceback
from flask import jsonify
from Dao.PurchaseDao import update_stock_ledger, update_stock_master
from extensions import db
from models.response_model import ResponseModel
from models.sales.sales_details_model import SalesDetails
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

def get_bill_by_date_dao(data):
    start_date = data.get("startDate")
    end_date = data.get("endDate")
    salesList = SalesMaster.query.filter(
                 SalesMaster.bill_date >= start_date,
                 SalesMaster.bill_date <= end_date
                ).order_by(desc(SalesMaster.bill_seq)).all()
    return jsonify([u.to_sales_dict() for u in salesList])

def get_latest_bill_no_dao():
    latest_bill_no  = (
                         SalesMaster.query
                        .order_by(desc(SalesMaster.bill_seq))
                        .first()
                      )
    return latest_bill_no

def save_sales_dao(salesData):
    try: 
       
        db.session.begin()
        
        latest_bill_data = get_latest_bill_no_dao()
        latest_bill_seq = latest_bill_data.bill_seq
        salesFields = SalesMaster.map_sales_data_to_model(salesData)
        sales = SalesMaster(**salesFields)

        latestBillNum = "A/"+str(latest_bill_seq+1)
        sales.bill_seq = latest_bill_seq+1
        sales.bill_number = latestBillNum
    
        db.session.add(sales)
        db.session.flush()

        for p in salesData.get("details", []):
            sale_data = SalesDetails(**SalesDetails.map_sales_detail_write(p))
            sale_data.sales_id = sales.sales_id
            update_stock_master(sale_data,p,"SALE")  
            update_stock_ledger(sale_data,p,"SALE")                     
            sales.details.append(sale_data)
            
        db.session.commit()
        res = ResponseModel(
        status="SUCCESS",
        statusCode=200,
        message= "Sales Data Saved Successfully" 
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

def update_sales_dao(salesId,salesData):
    try:
        db.session.begin() 
        sales = (
            db.session.query(SalesMaster)
            .filter(SalesMaster.sales_id == salesId)
            .with_for_update()  
            .one_or_none()
        )

        if not sales:
            db.session.rollback()
            return jsonify({
                "status": "FAILURE",
                "message": "Quote not found"
            }), 404

        # Update master fields

        updated_fields = SalesMaster.map_sales_data_to_model(salesData)
        SKIP_FIELDS = {"sales_id", "bill_date","bill_number","bill_seq","sales_detail_id"}
        for key, value in updated_fields.items():
            if key not in SKIP_FIELDS:
                setattr(sales, key, value)

        existing_details = SalesDetails.query.filter_by(sales_id=salesId).all()
        existing_map = {d.sales_detail_id: d for d in existing_details}
        incoming_ids = set()

        for p in salesData.get("details", []):
            detail_id = p.get("salesDetailId")

            if detail_id and detail_id in existing_map:
                # ✅ UPDATE existing row
                detail = existing_map[detail_id]
                mapped = SalesDetails.map_sales_detail_write(p)

                for k, v in mapped.items():
                     if k not in SKIP_FIELDS:
                        setattr(detail, k, v)

                incoming_ids.add(detail_id)

            else:
                # ✅ INSERT new row
                new_detail = SalesDetails(**SalesDetails.map_sales_detail_write(p))
                new_detail.sales_id = salesId
                db.session.add(new_detail)
        for delId in salesData.get("deleteIds", []):
            detail = existing_map.get(delId)
            if detail:
                db.session.delete(detail)
        # 5️⃣ Commit everything
        db.session.commit()

        return jsonify({
            "status": "SUCCESS",
            "message": "Sales data updated successfully"
        }), 200

    except Exception:
        db.session.rollback()
        traceback.print_exc()
        return jsonify({
            "status": "FAILURE",
            "message": "OOPS! Something went wrong"
        }), 500