import json
import frappe

def run():
    # 1. Get exact card names
    card1 = frappe.db.get_value("Number Card", {"label": "Total Certified Work (MB)"}, "name") or "Total Certified Work (MB)"
    card2 = frappe.db.get_value("Number Card", {"label": "Certified Subcontractor Payables"}, "name") or "Certified Subcontractor Payables"
    card3 = frappe.db.get_value("Number Card", {"label": "Total DPRs Logged"}, "name") or "Total DPRs Logged"
    card4 = frappe.db.get_value("Number Card", {"label": "Approved QA/QC Inspections"}, "name") or "Approved QA/QC Inspections"

    # 2. Visual layout grid blocks for Frappe v15
    content_blocks = [
        {
            "type": "header",
            "data": {
                "text": "EPC Project KPIs",
                "level": 4,
                "col": 12
            }
        },
        {
            "type": "card",
            "data": {
                "card_name": card1,
                "col": 3
            }
        },
        {
            "type": "card",
            "data": {
                "card_name": card2,
                "col": 3
            }
        },
        {
            "type": "card",
            "data": {
                "card_name": card3,
                "col": 3
            }
        },
        {
            "type": "card",
            "data": {
                "card_name": card4,
                "col": 3
            }
        },
        {
            "type": "header",
            "data": {
                "text": "Site Operations & Contract Billing",
                "level": 4,
                "col": 12
            }
        },
        {
            "type": "shortcut",
            "data": {
                "shortcut_name": "Daily Progress Report",
                "col": 3
            }
        },
        {
            "type": "shortcut",
            "data": {
                "shortcut_name": "Measurement Book",
                "col": 3
            }
        },
        {
            "type": "shortcut",
            "data": {
                "shortcut_name": "Payment Certificate",
                "col": 3
            }
        },
        {
            "type": "shortcut",
            "data": {
                "shortcut_name": "Site Inspection Request",
                "col": 3
            }
        }
    ]

    # 3. Find and update Workspace
    ws_name = "EPC Management"
    if not frappe.db.exists("Workspace", ws_name):
        ws_list = frappe.get_all("Workspace", filters={"title": ["like", "%EPC%"]}, pluck="name")
        if ws_list:
            ws_name = ws_list[0]

    ws = frappe.get_doc("Workspace", ws_name)
    ws.label = "EPC Project Management"
    ws.title = "EPC Project Management"
    ws.public = 1
    ws.icon = "project"
    ws.content = json.dumps(content_blocks)

    # Populate child tables
    ws.number_cards = []
    if card1: ws.append("number_cards", {"number_card_name": card1, "label": "Total Certified Work (MB)"})
    if card2: ws.append("number_cards", {"number_card_name": card2, "label": "Certified Subcontractor Payables"})
    if card3: ws.append("number_cards", {"number_card_name": card3, "label": "Total DPRs Logged"})
    if card4: ws.append("number_cards", {"number_card_name": card4, "label": "Approved QA/QC Inspections"})

    ws.shortcuts = []
    ws.append("shortcuts", {"type": "DocType", "link_to": "Daily Progress Report", "label": "Daily Progress Report"})
    ws.append("shortcuts", {"type": "DocType", "link_to": "Measurement Book", "label": "Measurement Book"})
    ws.append("shortcuts", {"type": "DocType", "link_to": "Subcontractor Payment Certificate", "label": "Payment Certificate"})
    ws.append("shortcuts", {"type": "DocType", "link_to": "Site Inspection Request", "label": "Site Inspection Request"})
    ws.append("shortcuts", {"type": "DocType", "link_to": "Project", "label": "All Projects"})

    ws.save(ignore_permissions=True)
    frappe.db.commit()
    frappe.clear_cache()
    print("SUCCESS: EPC Project Management Workspace layout generated.")