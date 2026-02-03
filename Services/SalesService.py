from flask import jsonify
from Dao.SalesDao import get_bill_by_date_dao, get_bill_by_id_dao, get_latest_bill_no_dao, save_sales_dao, update_sales_dao


def get_bill_by_id_serv(salesId):
    return get_bill_by_id_dao(salesId)

def get_bill_by_date_serv(data):
    return get_bill_by_date_dao(data)

def get_latest_bill_no_serv():
    latest_bill_data = get_latest_bill_no_dao()
    return jsonify(dict(latestBillNo=("A/"+str(latest_bill_data.bill_seq))))

def save_sales_serv(data):
    salesId = data.get("salesId")
    if data.get("salesId"):
        return update_sales_dao(salesId,data)
    else:
        return save_sales_dao(data)