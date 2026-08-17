import frappe
from frappe.model.document import Document

class MaterialReconciliation(Document):
    def validate(self):
        calculate_reconciliation_hook(self)

def calculate_reconciliation_hook(doc, method=None):
    allowable_limit = float(doc.allowable_wastage_pct or 3.0)
    total_loss = 0.0
    has_excess_wastage = False

    for row in doc.get("items", []):
        if row.item_code and not row.item_name:
            row.item_name = frappe.db.get_value("Item", row.item_code, "item_name")
            row.uom = frappe.db.get_value("Item", row.item_code, "stock_uom")
            if not row.unit_rate:
                row.unit_rate = frappe.db.get_value("Item", row.item_code, "valuation_rate") or 0.0

        theo = float(row.theoretical_qty or 0.0)
        actual = float(row.actual_qty or 0.0)
        rate = float(row.unit_rate or 0.0)

        # Variance = Actual - Theoretical
        variance = actual - theo
        row.variance_qty = variance

        # Wastage % = (Variance / Theoretical) * 100
        if theo > 0:
            pct = (variance / theo) * 100.0
        else:
            pct = 0.0 if actual == 0 else 100.0
        row.variance_pct = round(pct, 2)

        # Financial Loss = Max(0, Variance) * Rate
        fin_loss = max(0.0, variance) * rate
        row.financial_impact = fin_loss
        total_loss += fin_loss

        # Status determination
        if row.variance_pct > allowable_limit:
            row.status = "Excess Wastage / Pilferage Alert"
            has_excess_wastage = True
        elif row.variance_pct < -5.0:
            row.status = "Under-consumption"
        else:
            row.status = "Within Tolerance"

    doc.total_financial_loss = total_loss

    if has_excess_wastage:
        doc.reconciliation_verdict = "Failed - Investigation Required"
    elif total_loss > 0:
        doc.reconciliation_verdict = "Warning - Minor Overconsumption"
    else:
        doc.reconciliation_verdict = "Pass - Within Allowable Norms"