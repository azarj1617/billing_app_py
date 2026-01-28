from datetime import datetime
from extensions import db

class QuoteDetails(db.Model):
    __tablename__ = 'quote_details'  # make sure it matches your MySQL table name

    quote_detail_id = db.Column(db.Integer, primary_key=True)
    quote_id = db.Column(
        db.Integer,
        db.ForeignKey("quote_master.quote_id"),
        nullable=False
    )
    item_id = db.Column(db.Integer)
    quantity = db.Column(db.Numeric(10, 2))
    mrp = db.Column(db.Numeric(10, 2))
    selling_price = db.Column(db.Numeric(10, 2))
    save_value = db.Column(db.Numeric(10, 2))
    whole_sale_price = db.Column(db.Numeric(10, 2))
    hsn_code = db.Column(db.String(25))
    sales_amount = db.Column(db.Numeric(10, 2))
    discount_percentage = db.Column(db.Numeric(10, 2))
    discount_amount = db.Column(db.Numeric(10, 2))
    taxable_amount = db.Column(db.Numeric(10, 2))
    gst = db.Column(db.Numeric(10, 2))
    cgst = db.Column(db.Numeric(10, 2))
    sgst = db.Column(db.Numeric(10, 2))
    cgst_amount = db.Column(db.Numeric(10, 2))
    sgst_amount = db.Column(db.Numeric(10, 2))
    igst = db.Column(db.Numeric(10, 2))
    igst_amount = db.Column(db.Numeric(10, 2))
    net_sales_amount = db.Column(db.Numeric(10, 2))
    price_id = db.Column(db.Integer)

    def __repr__(self):
        return f"<QuoteDetails {self.name}>"

    def to_dict(self):
        return {
            "priceId": self.price_id,
            "quoteId": self.quote_id,
            "quoteDetailId": self.quote_detail_id,
            "itemId":self.item_id,
            "quantity":self.quantity,
            "mrp":self.mrp,
            "sellingPrice":self.selling_price,
            "saveValue":self.save_value,
            "wholeSalePrice":self.whole_sale_price,
            "itemName":self.item_id,
            "itemDescription":self.item_id,
            "uom":self.item_id,
            "hsnCode":"",
            "salesAmount":self.sales_amount,
            "discountPercentage":self.discount_percentage,
            "discountAmount":self.discount_amount,
            "taxableAmount":self.taxable_amount,
            "gst":self.gst,
            "cgst":self.cgst,
            "sgst":self.sgst,
            "cgstAmount":self.cgst_amount,
            "sgstAmount":self.sgst_amount,
            "igst":self.igst,
            "igstAmount":self.igst_amount,
            "netSalesAmount":self.net_sales_amount
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

