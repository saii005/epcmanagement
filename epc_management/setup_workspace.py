import frappe

def run():
    if not frappe.db.exists("Workspace", "EPC Management"):
        ws = frappe.new_doc("Workspace")
        ws.label = "EPC Management"
        ws.title = "EPC Project Management"
        ws.module = "EPC Management"
        ws.public = 1
        ws.icon = "project"
        ws.append("shortcuts", {"type": "DocType", "link_to": "Daily Progress Report", "label": "Daily Progress Report"})
        ws.append("shortcuts", {"type": "DocType", "link_to": "Measurement Book", "label": "Measurement Book"})
        ws.append("shortcuts", {"type": "DocType", "link_to": "Subcontractor Payment Certificate", "label": "Payment Certificate"})
        ws.append("shortcuts", {"type": "DocType", "link_to": "Site Inspection Request", "label": "Site Inspection Request"})
        ws.append("shortcuts", {"type": "DocType", "link_to": "Project", "label": "All Projects"})
        ws.insert(ignore_permissions=True)
        frappe.db.commit()
        print("SUCCESS: EPC Public Workspace Created!")
    else:
        frappe.db.set_value("Workspace", "EPC Management", "public", 1)
        frappe.db.commit()
        print("SUCCESS: Existing EPC Workspace set to Public!")
