from datetime import datetime
from extensions import db

class Customer(db.Model):
    __tablename__ = 'customers'  # make sure it matches your MySQL table name

    customer_id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100))
    created_by = db.Column(db.Date, nullable=False)
    mobile = db.Column(db.String(100))
    address = db.Column(db.String(255))
    city = db.Column(db.String(255))
    state = db.Column(db.String(100))
    status = db.Column(db.Integer)
    price_type = db.Column(db.Integer)
    cus_old_no = db.Column(db.String(100))
    created_by = db.Column(db.Date,default=datetime.now())
    quotes = db.relationship(
        "QuoteMaster",
        backref="customer",
        lazy="select",   # good for GET APIs
        cascade="all, delete-orphan"
    )
    def __repr__(self):
        return f"<Customer {self.name}>"

    def to_dict(self):
        return {
            "customerId": self.customer_id,
            "customerFirstName": self.firstname,
            "customerLastName": self.lastname,
            "mobile" : self.mobile,
            "address" : self.address,
            "city" : self.city,
            "state" : self.state,
            "status" : self.status,
            "priceType" : self.price_type,
            "cusOldNo" : self.cus_old_no,
            "createdAt": self.created_by.strftime("%d-%m-%Y")
        }
    
    def map_client_to_model(data):
        return {
            "customer_id":data.get("customerId"),
            "firstname": data.get("customerFirstName"),
            "lastname": data.get("customerLastName"),
            "mobile": data.get("mobile"),
            "address": data.get("address"),
            "city": data.get("city"),
            "state": data.get("state"),
            "status": data.get("status"),
            "price_type": data.get("priceType"),
            "cus_old_no": data.get("cusOldNo")
        }

