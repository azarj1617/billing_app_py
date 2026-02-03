from datetime import datetime
from extensions import db

class SalesDetails(db.Model):
    __tablename__ = 'sales_details'  # make sure it matches your MySQL table name

    sales_detail_id = db.Column(db.Integer, primary_key=True)
    sales_id = db.Column(
        db.Integer,
        db.ForeignKey("sales_master.sales_id"),
        nullable=False
    )
    item_id =  db.Column(
        db.Integer,
        db.ForeignKey("item_master.item_id"),
        nullable=False
    )
    hsn_code = db.Column(db.String(25))
    mrp = db.Column(db.Numeric(10, 2))
    uom = db.Column(db.String(20))
    selling_price = db.Column(db.Numeric(10, 2))
    sales_qty = db.Column(db.Numeric(10, 2))  
    sales_amount = db.Column(db.Numeric(10, 2),default=0.00)
    discount_percentage = db.Column(db.Numeric(10, 2),default=0.00)
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
        return f"<SalesDetails {self.name}>"

    def to_dict(self):
        itemData = self.items.item_to_dict()
        return {
            "priceId": self.price_id,
            "salesId": self.sales_id,
            "salesDetailId": self.sales_detail_id,
            "itemId":self.item_id,
            "salesQty":self.sales_qty,
            "mrp":self.mrp,
            "sellingPrice":self.selling_price,
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
    
    def map_sales_detail_to_read(data):
        return {
            "price_id": data.get("priceId"),
            "sales_id": data.get("salesId"),
            "sales_detail_id": data.get("salesDetailId"),
            "item_id": data.get("itemId"),
            "sales_qty": data.get("salesQty"),
            "mrp": data.get("mrp"),
            "selling_price": data.get("sellingPrice"),
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

    def map_sales_detail_write(data):
        return {
            "price_id": data.get("priceId"),
            "sales_id": data.get("salesId"),
            "sales_detail_id": data.get("salesDetailId"),
            "item_id": data.get("itemId"),
            "sales_qty": data.get("salesQty"),
            "mrp": data.get("mrp"),
            "selling_price": data.get("sellingPrice"),
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