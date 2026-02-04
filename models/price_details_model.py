from datetime import datetime
from extensions import db
class PriceDetails(db.Model):
    __tablename__ = 'item_master_price_history'  # make sure it matches your MySQL table name
    price_id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(
        db.Integer,
        db.ForeignKey("item_master.item_id"),
        nullable=False
    )
    mrp = db.Column(db.Numeric(10, 2))
    selling_price = db.Column(db.Numeric(10, 2))
    save_value = db.Column(db.Numeric(10, 2))
    whole_sale_price = db.Column(db.Numeric(10, 2))
    cost_price = db.Column(db.Numeric(10, 2))
    updated_at = db.Column(db.Date,default=datetime.now())
      
    def __repr__(self):
        return f"<PriceDetails {self.name}>"

    def price_to_dict(self):
        return {
            "priceId" : self.price_id,
            "itemId" : self.item_id,
            "mrp" : self.mrp, 
            "sellingPrice" : self.selling_price, 
            "saveValue" : self.save_value,
            "wholeSalePrice" : self.whole_sale_price,
            "costPrice" : self.cost_price,
        }
    
    def map_price_details(data):
        return {
            "price_id": data.get("priceId"),
            "item_id": data.get("itemId"),
            "mrp":data.get("mrp"),
            "selling_price":data.get("sellingPrice"),
            "save_value":data.get("saveValue"),
            "whole_sale_price":data.get("wholeSalePrice"),
            "cost_price":data.get("costPrice")
        }

