from datetime import datetime
from extensions import db

class Item(db.Model):
    __tablename__ = 'item_master'  # make sure it matches your MySQL table name

    item_id = db.Column(db.Integer, primary_key=True)
    ea_code = db.Column(db.String(255), nullable=False)
    item_name = db.Column(db.String(255))
    uom = db.Column(db.String(255))
    status = db.Column(db.Integer)
    item_description = db.Column(db.String(255))
    category = db.Column(db.String(255))
    item_code_old = db.Column(db.String(255))
    hsn_code = db.Column(db.String(50))
    gst = db.Column(db.String(25))
    priceDetails = db.relationship(
        "PriceDetails",
        backref="item",
        lazy="select",   # good for GET APIs
        cascade="all, delete-orphan"
    )
    def __repr__(self):
        return f"<Item {self.name}>"

    def item_to_dict(self):
        return {
            "itemId" : self.item_id,
            "eaCode" : self.ea_code, 
            "itemName" : self.item_name, 
            "uom" : self.uom,
            "status" : self.status,
            "itemDescription" : self.item_description,
            "category" : self.category,
            "itemCodeOld" : self.item_code_old,
            "hsnCode" : self.hsn_code, 
            "gst" : self.gst,
            "priceDetails": [a.price_to_dict() for a in self.priceDetails]
        }
    
    def map_item_data_to_model(data):
        return {
            "item_id":data.get("itemId"),
            "ea_code": data.get("eaCode"),
            "item_name": data.get("itemName"),
            "uom": data.get("uom"),
            "status": data.get("status"),
            "item_description": data.get("itemDescription"),
            "category": data.get("category"),
            "item_code_old": data.get("itemCodeOld"),
            "hsn_code": data.get("hsnCode"),
            "gst": data.get("gst")
        }

    