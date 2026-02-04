from datetime import datetime
from extensions import db

class PurchaseMaster(db.Model):
    __tablename__ = 'purchase_master'  # make sure it matches your MySQL table name

    purchase_id = db.Column(db.Integer, primary_key=True)
    grn_code = db.Column(db.String(25))
    grn_date = db.Column(db.Date, nullable=False)
    cash_discount_percent = db.Column(db.Numeric(2,10))
    cash_discount_amount = db.Column(db.Numeric(2,10))
    net_purchase_amount = db.Column(db.Numeric(2,10))
    purchaseDetails = db.relationship(
        "PurchaseDetails",
        backref="purchase",
        lazy="select", 
        cascade="all, delete-orphan"
    )

    # def __repr__(self):
    #     return f"<PurchaseMaster {self.name}>"

    def purchase_to_dict(self):
        return {
            "purchaseId": self.purchase_id,
            "grnCode": self.grn_code,
            "grnDate": self.grn_date.strftime("%Y-%m-%d") if self.grn_date else None,
            "cashDiscountPercent": float(self.cash_discount_percent) if self.cash_discount_percent is not None else 0.0,
            "cashDiscountAmount": float(self.cash_discount_amount) if self.cash_discount_amount is not None else 0.0,
            "netPurchaseAmount": float(self.net_purchase_amount) if self.net_purchase_amount is not None else 0.0,
            "purchaseDetails": [a.purchase_detail_to_dict() for a in self.purchaseDetails]
        }
    
    def map_purchase_data_to_model(data):
        return {
            "purchase_id": data.get("purchaseId"),
            "grn_code": data.get("grnCode"),
            "grn_date": data.get("grnDate"),
            "cash_discount_percent": data.get("cashDiscountPercent"),
            "cash_discount_amount": data.get("cashDiscountAmount"),
            "net_purchase_amount": data.get("netPurchaseAmount")
        }


    