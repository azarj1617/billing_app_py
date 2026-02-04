from datetime import datetime
from extensions import db
from models.customer_model import Customer

class SalesMaster(db.Model):
    __tablename__ = 'sales_master'  # make sure it matches your MySQL table name

    sales_id = db.Column(db.Integer, primary_key=True)
    bill_number = db.Column(db.String(25))
    customer_id =  customer_id = db.Column(
        db.Integer,
        db.ForeignKey("customers.customer_id"),
        nullable=False
    )
    customer_type = db.Column(db.Integer)
    bill_date = db.Column(db.Date)
    discount_percent = db.Column(db.Numeric(10,2),default=0.00)
    discount_amount = db.Column(db.Numeric(10,2),default=0.00)
    net_sales_amount = db.Column(db.Numeric(10,2))
    bill_seq = db.Column(db.Integer)
    
    details = db.relationship(
        "SalesDetails",
        backref="item",
        lazy="select",   # good for GET APIs
        cascade="all, delete-orphan"
    )
    customers = db.relationship("Customer", lazy="joined",viewonly=True)
    
    # def __repr__(self):
    #     return f"<QuoteMaster {self.name}>"

    def to_sales_dict(self):
        return {
            "salesId": self.sales_id,
            "billNumber": self.bill_number,
            "customerId": self.customer_id,
            "customerType": self.customer_type,
            "billDate": datetime.strftime(self.bill_date,"%Y-%m-%d %H:%M:%S"),
            "discountPercent": self.discount_percent,
            "discountAmount": self.discount_amount,
            "netSalesAmount": self.net_sales_amount,
            "billSeq": self.bill_seq,
            "details":[a.to_dict() for a in self.details],
            "customer": ([self.customers.to_dict()] if self.customers else [])
        }   
    
    def map_client_data_to_model(data):
        return {
            "start_date":data.get("startDate"),
            "end_date": data.get("endDate")
        }
    
    def map_sales_data_to_model(data):
        return {
            "sales_id": data.get("salesId"),
            "bill_number": data.get("billNumber"),
            "customer_id": data.get("customerId"),
            "customer_type": data.get("customerType"),
            "bill_date": data.get("billDate"),
            "discount_percent": data.get("discountPercent"),
            "discount_amount": data.get("discountAmount"),
            "net_sales_amount": data.get("netSalesAmount"),
            "bill_seq": data.get("billSeq")
        }


