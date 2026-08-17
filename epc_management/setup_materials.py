import frappe

def run():
    company = frappe.db.get_single_value("Global Defaults", "default_company") or "Cosmoops"
    abbr = frappe.db.get_value("Company", company, "abbr") or "C"

    # 1. Create missing Units of Measure (UOM)
    uoms = ["Bag", "Kg", "Litre", "Cum", "Nos"]
    for u in uoms:
        if not frappe.db.exists("UOM", u):
            frappe.get_doc({"doctype": "UOM", "uom_name": u, "must_be_whole_number": 0}).insert(ignore_permissions=True)
            print(f"Created UOM: {u}")

    # 2. Create / Update Construction Stock Items
    materials = [
        ("MAT-CEMENT-53", "OPC 53 Grade Cement", "Bag", 380.0),
        ("MAT-STEEL-16MM", "TMT Reinforcement Rebar 16mm (Fe500D)", "Kg", 65.0),
        ("MAT-DIESEL-HSD", "High Speed Diesel (Fuel)", "Litre", 92.0),
        ("MAT-AGG-20MM", "Coarse Blue Metal Aggregates 20mm", "Cum", 1250.0)
    ]

    for code, name, uom, rate in materials:
        if not frappe.db.exists("Item", code):
            doc = frappe.new_doc("Item")
            doc.item_code = code
            doc.item_name = name
            doc.item_group = "Raw Material"
            doc.stock_uom = uom
            doc.is_stock_item = 1
            doc.valuation_rate = rate
            doc.standard_rate = rate
            doc.insert(ignore_permissions=True)
        else:
            frappe.db.set_value("Item", code, {"is_stock_item": 1, "stock_uom": uom})
        print(f"Verified Stock Item: {code}")

    # 3. Create Site Warehouse if not exists
    site_wh_name = f"Metro Line Site Store - {abbr}"
    if not frappe.db.exists("Warehouse", site_wh_name):
        wh = frappe.new_doc("Warehouse")
        wh.warehouse_name = "Metro Line Site Store"
        wh.company = company
        wh.parent_warehouse = f"All Warehouses - {abbr}"
        wh.insert(ignore_permissions=True)
        print(f"Created Warehouse: {site_wh_name}")

    # 4. Receive 500 units of initial inventory into Central Store
    central_wh = f"Stores - {abbr}"
    try:
        se = frappe.new_doc("Stock Entry")
        se.stock_entry_type = "Material Receipt"
        se.company = company
        se.to_warehouse = central_wh
        for code, name, uom, rate in materials:
            se.append("items", {
                "item_code": code,
                "qty": 500,
                "uom": uom,
                "basic_rate": rate,
                "t_warehouse": central_wh
            })
        se.insert(ignore_permissions=True)
        se.submit()
        print(f"Added 500 units of each material into Central Store ({central_wh})")
    except Exception as e:
        print(f"Stock receipt status: {e}")

    frappe.db.commit()
    frappe.clear_cache()
    print("SUCCESS: Site Inventory Setup Completed Cleanly.")