from datetime import datetime
from extensions import db

class PurchaseDetails(db.Model):
    __tablename__ = 'purchase_details'  # make sure it matches your MySQL table name

    purchase_detail_id = db.Column(db.Integer, primary_key=True)
    purchase_id = db.Column(
        db.Integer,
        db.ForeignKey("purchase_master.purchase_id"),
        nullable=False
    )
    item_id = db.Column(db.Integer, nullable=False)

    hsn_code = db.Column(db.String(20))
    mrp = db.Column(db.Numeric(2,10))
    uom = db.Column(db.String(10))

    purchase_price = db.Column(db.Numeric(2,10))
    purchase_qty = db.Column(db.Numeric(2,10))
    purchase_amount = db.Column(db.Numeric(2,10))

    discount_percentage = db.Column(db.Numeric(2,10))
    discount_amount = db.Column(db.Numeric(2,10))

    taxable_amount = db.Column(db.Numeric(2,10))

    gst = db.Column(db.Numeric(2,10))
    cgst = db.Column(db.Numeric(2,10))
    sgst = db.Column(db.Numeric(2,10))

    cgst_amount = db.Column(db.Numeric(2,10))
    sgst_amount = db.Column(db.Numeric(2,10))

    igst = db.Column(db.Numeric(2,10))
    igst_amount = db.Column(db.Numeric(2,10))

    net_purchase_amount = db.Column(db.Numeric(2,10))
    
    def __repr__(self):
        return f"<PurchaseDetails {self.name}>"

    def purchase_detail_to_dict(self):
        return {
        "purchaseDetailId": self.purchase_detail_id,
        "purchaseId": self.purchase_id,
        "itemId": self.item_id,
        "hsnCode": self.hsn_code,
        "mrp": self.mrp if self.mrp is not None else 0.0,
        "uom": self.uom,
        "purchasePrice": self.purchase_price if self.purchase_price is not None else 0.0,
        "purchaseQty": self.purchase_qty if self.purchase_qty is not None else 0.0,
        "purchaseAmount": self.purchase_amount if self.purchase_amount is not None else 0.0,
        "discountPercentage": self.discount_percentage if self.discount_percentage is not None else 0.0,
        "discountAmount": self.discount_amount if self.discount_amount is not None else 0.0,
        "taxableAmount": self.taxable_amount if self.taxable_amount is not None else 0.0,
        "gst": self.gst if self.gst is not None else 0.0,
        "cgst": self.cgst if self.cgst is not None else 0.0,
        "sgst": self.sgst if self.sgst is not None else 0.0,
        "cgstAmount": self.cgst_amount if self.cgst_amount is not None else 0.0,
        "sgstAmount": self.sgst_amount if self.sgst_amount is not None else 0.0,
        "igst": self.igst if self.igst is not None else 0.0,
        "igstAmount": self.igst_amount if self.igst_amount is not None else 0.0,
        "netPurchaseAmount": self.net_purchase_amount if self.net_purchase_amount is not None else 0.0
    }

    
    def map_purchase_detail_data_to_model(data):
        return {
        "purchase_detail_id": data.get("purchaseDetailId"),
        "purchase_id": data.get("purchaseId"),
        "item_id": data.get("itemId"),
        "hsn_code": data.get("hsnCode"),
        "mrp": data.get("mrp"),
        "uom": data.get("uom"),
        "purchase_price": data.get("purchasePrice"),
        "purchase_qty": data.get("purchaseQty"),
        "purchase_amount": data.get("purchaseAmount"),
        "discount_percentage": data.get("discountPercentage"),
        "discount_amount": data.get("discountAmount"),
        "taxable_amount": data.get("taxableAmount"),
        "gst": data.get("gst"),
        "cgst": data.get("cgst"),
        "sgst": data.get("sgst"),
        "cgst_amount": data.get("cgstAmount"),
        "sgst_amount": data.get("sgstAmount"),
        "igst": data.get("igst"),
        "igst_amount": data.get("igstAmount"),
        "net_purchase_amount": data.get("netPurchaseAmount")
    }



    