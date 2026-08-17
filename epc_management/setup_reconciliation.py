import frappe

def create_child_doctype():
    if not frappe.db.exists("DocType", "Material Reconciliation Item"):
        fields = [
            {"fieldname": "item_code", "fieldtype": "Link", "options": "Item", "label": "Material / Item Code", "in_list_view": 1, "reqd": 1},
            {"fieldname": "item_name", "fieldtype": "Data", "label": "Item Description", "in_list_view": 1, "read_only": 1},
            {"fieldname": "uom", "fieldtype": "Link", "options": "UOM", "label": "Unit", "in_list_view": 1, "read_only": 1},
            {"fieldname": "theoretical_qty", "fieldtype": "Float", "label": "Theoretical Required Qty", "in_list_view": 1},
            {"fieldname": "actual_qty", "fieldtype": "Float", "label": "Actual Issued Qty", "in_list_view": 1},
            {"fieldname": "variance_qty", "fieldtype": "Float", "label": "Variance (Wastage)", "in_list_view": 1, "read_only": 1},
            {"fieldname": "variance_pct", "fieldtype": "Percent", "label": "Wastage %", "in_list_view": 1, "read_only": 1},
            {"fieldname": "unit_rate", "fieldtype": "Currency", "label": "Unit Rate (INR)"},
            {"fieldname": "financial_impact", "fieldtype": "Currency", "label": "Financial Loss / Gain (INR)", "in_list_view": 1, "read_only": 1},
            {"fieldname": "status", "fieldtype": "Select", "options": "Within Tolerance\nExcess Wastage / Pilferage Alert\nUnder-consumption", "label": "Audit Status", "in_list_view": 1, "read_only": 1}
        ]
        
        doc = frappe.new_doc("DocType")
        doc.name = "Material Reconciliation Item"
        doc.module = "EPC Management"
        doc.custom = 0
        doc.istable = 1
        for f in fields:
            doc.append("fields", f)
        doc.insert(ignore_permissions=True)
        print("Created Child DocType: Material Reconciliation Item")

def create_parent_doctype():
    if not frappe.db.exists("DocType", "Material Reconciliation"):
        fields = [
            {"fieldname": "section_details", "fieldtype": "Section Break", "label": "Project & Reconciliation Period"},
            {"fieldname": "project", "fieldtype": "Link", "options": "Project", "label": "Project", "reqd": 1, "in_list_view": 1},
            {"fieldname": "posting_date", "fieldtype": "Date", "label": "Posting Date", "reqd": 1, "in_list_view": 1},
            {"fieldname": "column_break_1", "fieldtype": "Column Break"},
            {"fieldname": "from_date", "fieldtype": "Date", "label": "Period From"},
            {"fieldname": "to_date", "fieldtype": "Date", "label": "Period To"},
            {"fieldname": "allowable_wastage_pct", "fieldtype": "Percent", "label": "Standard Allowable Wastage (%)", "default": "3.0"},
            
            {"fieldname": "section_items", "fieldtype": "Section Break", "label": "Material Consumption & Variance Analysis"},
            {"fieldname": "items", "fieldtype": "Table", "options": "Material Reconciliation Item", "label": "Reconciled Materials"},
            
            {"fieldname": "section_summary", "fieldtype": "Section Break", "label": "Audit Summary & Financial Impact"},
            {"fieldname": "total_financial_loss", "fieldtype": "Currency", "label": "Total Wastage / Loss Value (INR)", "read_only": 1, "in_list_view": 1},
            {"fieldname": "column_break_2", "fieldtype": "Column Break"},
            {"fieldname": "reconciliation_verdict", "fieldtype": "Select", "options": "Pass - Within Allowable Norms\nWarning - Minor Overconsumption\nFailed - Investigation Required", "label": "Overall Audit Verdict", "read_only": 1, "in_list_view": 1},
            {"fieldname": "remarks", "fieldtype": "Small Text", "label": "Auditor Remarks & Corrective Action"}
        ]

        doc = frappe.new_doc("DocType")
        doc.name = "Material Reconciliation"
        doc.module = "EPC Management"
        doc.custom = 0
        doc.is_submittable = 1
        doc.autoname = "MREC-.YYYY.-.#####"
        for f in fields:
            doc.append("fields", f)
        doc.insert(ignore_permissions=True)
        print("Created DocType: Material Reconciliation")

def run():
    create_child_doctype()
    create_parent_doctype()
    
    # Configure Permissions
    roles = ["EPC Project Manager", "EPC Site Engineer", "Stock Manager"]
    for dt in ["Material Reconciliation", "Material Reconciliation Item"]:
        for r in roles:
            if not frappe.db.exists("Custom DocPerm", {"parent": dt, "role": r}):
                docperm = frappe.new_doc("Custom DocPerm")
                docperm.parent = dt
                docperm.parenttype = "DocType"
                docperm.parentfield = "permissions"
                docperm.role = r
                docperm.read = 1
                docperm.write = 1
                docperm.create = 1
                docperm.submit = 1 if r in ["EPC Project Manager", "Stock Manager"] else 0
                docperm.cancel = 1 if r == "EPC Project Manager" else 0
                docperm.amend = 1 if r == "EPC Project Manager" else 0
                docperm.insert(ignore_permissions=True)

    frappe.db.commit()
    print("SUCCESS: Material Reconciliation DocTypes and Permissions created.")