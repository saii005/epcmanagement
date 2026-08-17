import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class SubcontractorPaymentCertificate(Document):
    def validate(self):
        calculate_spc_totals(self)

def calculate_spc_totals(doc, method=None):
    if doc.measurement_book and not doc.gross_amount:
        mb = frappe.get_doc("Measurement Book", doc.measurement_book)
        doc.project = mb.project
        doc.subcontractor = mb.subcontractor
        doc.purchase_order = mb.purchase_order
        doc.gross_amount = mb.total_measured_amount or 0.0

    gross = float(doc.gross_amount or 0.0)
    ret_pct = float(doc.retention_percentage or 5.0)
    doc.retention_percentage = ret_pct
    doc.retention_amount = gross * (ret_pct / 100.0)
    
    adv = float(doc.advance_recovery or 0.0)
    ded = float(doc.other_deductions or 0.0)
    doc.net_payable_amount = gross - doc.retention_amount - adv - ded

@frappe.whitelist()
def make_purchase_invoice(source_name, target_doc=None):
    doc = frappe.get_doc("Subcontractor Payment Certificate", source_name)
    
    def set_missing_values(source, target):
        target.supplier = source.subcontractor
        target.project = source.project
        target.bill_no = source.name
        target.bill_date = source.posting_date
        
        # Auto-fetch company's default expense account
        expense_acc = frappe.db.get_value("Company", target.company, "default_expense_account") or \
                      frappe.db.get_value("Account", {"company": target.company, "account_type": "Direct Expense", "is_group": 0}, "name") or \
                      frappe.db.get_value("Account", {"company": target.company, "root_type": "Expense", "is_group": 0}, "name")
        
        target.append("items", {
            "item_name": f"Subcontractor Certified Works - {source.name}",
            "description": f"Payment against Measurement Book: {source.measurement_book or 'N/A'}",
            "qty": 1,
            "uom": "Nos",
            "rate": source.net_payable_amount,
            "amount": source.net_payable_amount,
            "expense_account": expense_acc,
            "project": source.project
        })

    return get_mapped_doc(
        "Subcontractor Payment Certificate",
        source_name,
        {
            "Subcontractor Payment Certificate": {
                "doctype": "Purchase Invoice",
                "field_map": {
                    "subcontractor": "supplier",
                    "project": "project",
                    "posting_date": "posting_date"
                }
            }
        },
        target_doc,
        set_missing_values
    )