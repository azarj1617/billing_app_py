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
    item_id =  db.Column(
        db.Integer,
        db.ForeignKey("item_master.item_id"),
        nullable=False
    )
    quantity = db.Column(db.Numeric(10, 2))
    mrp = db.Column(db.Numeric(10, 2))
    selling_price = db.Column(db.Numeric(10, 2))
    save_value = db.Column(db.Numeric(10, 2))
    whole_sale_price = db.Column(db.Numeric(10, 2))
    hsn_code = db.Column(db.String(25))
    sales_amount = db.Column(db.Numeric(10, 2),default=0.00)
    discount_percentage = db.Column(db.Numeric(10, 2),default=0)
    discount_amount = db.Column(db.Numeric(10, 2),default=0.00)
    taxable_amount = db.Column(db.Numeric(10, 2),default=0.00)
    gst = db.Column(db.Numeric(10, 2),default=0.00)
    cgst = db.Column(db.Numeric(10, 2),default=0.00)
    sgst = db.Column(db.Numeric(10, 2),default=0.00)
    cgst_amount = db.Column(db.Numeric(10, 2),default=0.00)
    sgst_amount = db.Column(db.Numeric(10, 2),default=0.00)
    igst = db.Column(db.Numeric(10, 2),default=0.00)
    igst_amount = db.Column(db.Numeric(10, 2),default=0.00)
    net_sales_amount = db.Column(db.Numeric(10, 2),default=0.00)
    price_id = db.Column(db.Integer)
    items = db.relationship("Item", lazy="joined")
    def __repr__(self):
        return f"<QuoteDetails {self.name}>"

    def to_dict(self):
        itemData = self.items.item_to_dict()
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
            "itemName":itemData.get("itemName"),
            "itemDescription":itemData.get("itemDescription"),
            "uom":itemData.get("uom"),
            "hsnCode":itemData.get("hsnCode"),
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
    
    def map_quote_detail_to_model(data):
        return {
            "price_id": data.get("priceId"),
            "quote_id": data.get("quoteId"),
            "quote_detail_id": data.get("quoteDetailId"),
            "item_id": data.get("itemId"),
            "quantity": data.get("quantity"),
            "mrp": data.get("mrp"),
            "selling_price": data.get("sellingPrice"),
            "save_value": data.get("saveValue"),
            "whole_sale_price": data.get("wholeSalePrice"),

            "item_name": data.get("itemName"),
            "item_description": data.get("itemDescription"),
            "uom": data.get("uom"),
            "hsn_code": data.get("hsnCode"),

            "sales_amount": data.get("salesAmount"),
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
            "net_sales_amount": data.get("netSalesAmount")
        }

    def map_quote_detail_write(data):
        return {
            "price_id": data.get("priceId"),
            "quote_id": data.get("quoteId"),
            "quote_detail_id": data.get("quoteDetailId"),
            "item_id": data.get("itemId"),
            "quantity": data.get("quantity"),
            "mrp": data.get("mrp"),
            "selling_price": data.get("sellingPrice"),
            "save_value": data.get("saveValue"),
            "whole_sale_price": data.get("wholeSalePrice"),
            "hsn_code": data.get("hsnCode"),
            "sales_amount": data.get("salesAmount"),
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
            "net_sales_amount": data.get("netSalesAmount")
        }