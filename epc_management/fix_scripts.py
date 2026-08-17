import frappe

MB_JS = """
frappe.ui.form.on('Measurement Book', {
    refresh(frm) {
        if (frm.is_new() && !frm.doc.posting_date) {
            frm.set_value('posting_date', frappe.datetime.get_today());
        }
    }
});

frappe.ui.form.on('Measurement Book Item', {
    numbers(frm, cdt, cdn) { calculate_row(frm, cdt, cdn); },
    length(frm, cdt, cdn) { calculate_row(frm, cdt, cdn); },
    width(frm, cdt, cdn) { calculate_row(frm, cdt, cdn); },
    height(frm, cdt, cdn) { calculate_row(frm, cdt, cdn); },
    rate(frm, cdt, cdn) { calculate_row(frm, cdt, cdn); },
    measurements_remove(frm) { calculate_total(frm); }
});

function calculate_row(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    let num = row.numbers || 1;
    let l = row.length || 1;
    let w = row.width || 1;
    let h = row.height || 1;

    let qty = (row.length || row.width || row.height) ? (num * l * w * h) : (row.quantity || 0);
    frappe.model.set_value(cdt, cdn, 'quantity', qty);

    let amt = qty * (row.rate || 0);
    frappe.model.set_value(cdt, cdn, 'amount', amt);

    calculate_total(frm);
}

function calculate_total(frm) {
    let total = 0;
    (frm.doc.measurements || []).forEach(row => {
        total += (row.amount || 0);
    });
    frm.set_value('total_measured_amount', total);
}
"""

def run():
    # 1. Clean any corrupted Client Scripts from the database
    corrupt_scripts = frappe.db.sql("SELECT name FROM `tabClient Script` WHERE script LIKE '%cat %' OR script LIKE '%EOF%'", as_dict=True)
    for row in corrupt_scripts:
        frappe.delete_doc("Client Script", row.name, ignore_permissions=True)
        print(f"Removed corrupted Client Script: {row.name}")

    # 2. Write clean JavaScript directly to the app codebase
    with open("apps/epc_management/epc_management/doctype/measurement_book/measurement_book.js", "w") as f:
        f.write(MB_JS.strip())

    frappe.db.commit()
    frappe.clear_cache()
    print("SUCCESS: Measurement Book JavaScript cleaned and restored.")

