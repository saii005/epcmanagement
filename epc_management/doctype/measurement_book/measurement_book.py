import frappe
from frappe.model.document import Document

class MeasurementBook(Document):
    def validate(self):
        calculate_mb_totals(self)

def calculate_mb_totals(doc, method=None):
    total = 0.0
    for item in doc.get("measurements", []):
        d = item.as_dict()
        
        # 1. Read values flexibly across all possible field names
        num = float(d.get("numbers") or d.get("no_of_units") or d.get("units") or 1.0)
        l = float(d.get("length") or d.get("length_m") or 0.0)
        w = float(d.get("width") or d.get("width__breadth_m") or d.get("breadth") or 0.0)
        h = float(d.get("height") or d.get("height__depth_m") or d.get("depth") or 0.0)

        # 2. Compute Quantity (L x W x H x No.)
        if l or w or h:
            l_val = l if l else 1.0
            w_val = w if w else 1.0
            h_val = h if h else 1.0
            qty = num * l_val * w_val * h_val
        else:
            qty = float(d.get("total_quantity") or d.get("quantity") or 0.0)

        # 3. Read Rate
        rate = float(d.get("unit_rate") or d.get("rate") or 0.0)
        amount = qty * rate
        total += amount

        # 4. Set both field variations on the row
        if "total_quantity" in d: item.total_quantity = qty
        if "quantity" in d: item.quantity = qty

        if "total_amount" in d: item.total_amount = amount
        if "amount" in d: item.amount = amount

    # 5. Set Total on Header
    p_dict = doc.as_dict()
    if "total_measured_amount" in p_dict: doc.total_measured_amount = total
    if "total_amount" in p_dict: doc.total_amount = total
    if "total_measured_value" in p_dict: doc.total_measured_value = total