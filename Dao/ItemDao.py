from operator import and_, or_
import traceback
from flask import jsonify
from models.item_model import Item
from models.price_details_model import PriceDetails
from models.response_model import ResponseModel
from extensions import db
itemList = []

def get_all_items(status):
    itemList = Item.query.filter(Item.status==status) 
    return jsonify([u.item_to_dict() for u in itemList])

def get_items_by_id_dao(itemId):
    itemList = Item.query.filter(Item.item_id == itemId)
    return jsonify([u.item_to_dict() for u in itemList][0])

def search_items_dao(searchTerm,status,type):
    if type=='eaCode':
        itemList = Item.query.filter(and_(Item.status==status,Item.ea_code == searchTerm))
        return jsonify([u.item_to_dict() for u in itemList])
    else:
        itemList = Item.query.filter(and_(Item.status==status,Item.item_name.ilike(f"%{searchTerm}%")))
        return jsonify([u.item_to_dict() for u in itemList])
    
def insert_item_dao(itemData):
    try: 
        item_fields = Item.map_item_data_to_model(itemData)       
        
        ea_code = item_fields.get("ea_code")
        existing_item = Item.query.filter_by(ea_code=ea_code).first()
       
        if existing_item:
            res = ResponseModel(
            status="FAILURE",
            statusCode=200,
            message="EA Code already exists"
            )
            return jsonify(res.__dict__), 201
        
        item = Item(**item_fields)
        db.session.add(item)
        db.session.flush()

        for p in itemData.get("priceDetails", []):
            price = PriceDetails(**PriceDetails.map_price_details(p))
            item.priceDetails.append(price)
        
        db.session.commit()
        res = ResponseModel(
        status="SUCCESS",
        statusCode=200,
        message= "Item Data Saved Successfully" 
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
    
def update_item_dao(itemData):
    try: 
        item_fields = Item.map_item_data_to_model(itemData)       
        
        item_id = item_fields.get("item_id")
        item = Item.query.get(item_id)

        for key, value in item_fields.items():
            if key != "item_id" and hasattr(item, key):
                setattr(item, key, value)
                
        sync_price_details(item, itemData.get("priceDetails", []))
        db.session.commit()

        
        db.session.commit()
        res = ResponseModel(
        status="SUCCESS",
        statusCode=200,
        message= "Item Data Updated Successfully" 
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
    
def sync_price_details(item, price_list):
    existing_prices = {p.price_id: p for p in item.priceDetails}

    incoming_ids = set()

    for p in price_list:
        price_id = p.get("priceId")

        if price_id and price_id in existing_prices:
            # 🔹 UPDATE
            price = existing_prices[price_id]
            for key, value in PriceDetails.map_price_details(p).items():
                setattr(price, key, value)

            incoming_ids.add(price_id)

        else:
            # 🔹 INSERT
            price = PriceDetails(**PriceDetails.map_price_details(p))
            item.priceDetails.append(price)

    # 🔹 DELETE removed prices
    for price_id, price in existing_prices.items():
        if price_id not in incoming_ids:
            db.session.delete(price)
