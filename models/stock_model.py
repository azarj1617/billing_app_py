from datetime import datetime
from extensions import db

class StockMaster(db.Model):
    __tablename__ = 'stock_master'  # make sure it matches your MySQL table name

    stock_id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(
        db.Integer,
        db.ForeignKey("item_master.item_id"),
        nullable=False
    )
    current_qty = db.Column(db.Numeric(2,10))
    updated_at = db.Column(db.Date, nullable=False)
    items = db.relationship("Item", lazy="joined")
    def __repr__(self):
        return f"<StockMaster {self.name}>"

    def stock_to_dict(self):
        itemData = self.items.item_to_dict()
        return {
            "stockId" : self.stock_id,
            "itemId" : self.item_id,
            "itemName":itemData.get("itemName"),
            "currentQty" : self.current_qty, 
            "updatedAt" : datetime.strftime(self.updated_at,"%Y-%m-%d %H:%M:%S")
        }
    
    def map_stock_data_to_model(data):
        return {
            "stock_id":data.get("stockId"),
            "item_id":data.get("itemId"),
            "current_qty": data.get("currentQty"),
            "updated_at": data.get("updatedAt")
        }

    