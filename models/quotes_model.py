from datetime import datetime
from extensions import db
from models.customer_model import Customer

class QuoteMaster(db.Model):
    __tablename__ = 'quote_master'  # make sure it matches your MySQL table name

    quote_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("customers.customer_id"),
        nullable=False
    )
    quote_date = db.Column(db.Date)
    total_amount = db.Column(db.String(100))
    quote_no = db.Column(db.String(100))
    quote_seq_no = db.Column(db.Integer)
    daily_seq_no = db.Column(db.String(255))
    details = db.relationship(
        "QuoteDetails",
        backref="item",
        lazy="select",   # good for GET APIs
        cascade="all, delete-orphan"
    )
    customers = db.relationship("Customer", lazy="joined")
    
    def __repr__(self):
        return f"<QuoteMaster {self.name}>"

    def to_quote_dict(self):
        return {
            "quoteId": self.quote_id,
            "customerId": self.customer_id,
            "quoteSeqNo": self.quote_seq_no,
            "quoteDate": datetime.strftime(self.quote_date,"%Y-%m-%d %H:%M:%S"),
            "totalAmount" : self.total_amount,
            "quoteNo" : self.quote_no,
            "dailyQuoteNo" : self.daily_seq_no,
            "details":[a.to_dict() for a in self.details],
            "customer": ([self.customer.to_dict()] if self.customer else None)
        }
    
    def map_client_data_to_model(data):
        return {
            "start_date":data.get("startDate"),
            "end_date": data.get("endDate")
        }

