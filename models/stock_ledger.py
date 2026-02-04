from datetime import date, datetime
from extensions import db

class StockLedger(db.Model):
    __tablename__ = 'stock_ledger'  # make sure it matches your MySQL table name

    txn_id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer)
    txn_type = db.Column(db.String(30))
    txn_date = db.Column(db.Date,default=date.today)
    qty_in = db.Column(db.Numeric(2,10),default=0.00)
    qty_out = db.Column(db.Numeric(2,10),default=0.00)
    rate = db.Column(db.Numeric(2,10))
    reference_id = db.Column(db.Integer)

    def __repr__(self):
        return f"<StockLedger {self.name}>"

    def txn_to_dict(self):
        return {
            "txnId": self.txn_id,
            "itemId": self.item_id,
            "txnType": self.txn_type,
            "txnDate": self.txn_date.strftime("%Y-%m-%d") if self.txn_date else None,
            "qtyIn": self.qty_in if self.qty_in is not None else 0,
            "qtyOut": self.qty_out if self.qty_out is not None else 0,
            "rate": self.rate if self.rate is not None else 0,
            "referenceId": self.reference_id
        }
    
    def map_stock_txn_data_to_model(data):
        return {
            "item_id": data.get("itemId"),
            "txn_type": data.get("txnType"),
            # "txn_date":data.get("txn_date"),
            "qty_in":data.get("qtyIn", 0),
            "qty_in":data.get("qtyOut", 0),
            "rate":data.get("rate", 0),
            "reference_id": data.get("referenceId"),
        }

    