from operator import and_, or_
import traceback
from flask import jsonify
from models.customer_model import Customer
from extensions import db
from models.response_model import ResponseModel

customerList = []

def get_all_customers(status):
    customerList = Customer.query.filter(Customer.status==status).all()
    return jsonify([u.to_dict() for u in customerList])

def search_customer_data(searchTerm,status):
    customerList = Customer.query.filter(and_(Customer.status==status,or_(
                                             Customer.firstname.ilike(f"%{searchTerm}%"),
                                             Customer.lastname.ilike(f"%{searchTerm}%")))) 
    return jsonify([u.to_dict() for u in customerList])

def save_customer_data(data):
    try: 
        customer = Customer(**Customer.map_client_to_model(data))         
        db.session.merge(customer)
        db.session.commit()
        mes = "Updated" if(data.get("customerId")) else "Saved" 
        res = ResponseModel(
        status="SUCCESS",
        statusCode=200,
        message= f"Customer Data {mes} Successfully" 
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
    