import frappe

SCRIPT_CODE = """
frappe.ui.form.on('Subcontractor Payment Certificate', {
    refresh: function(frm) {
        if (frm.doc.docstatus === 1) {
            frm.add_custom_button(__('Create Purchase Invoice'), function() {
                frappe.model.open_mapped_doc({
                    method: 'epc_management.doctype.subcontractor_payment_certificate.subcontractor_payment_certificate.make_purchase_invoice',
                    frm: frm
                });
            });
            frm.change_custom_button_type(__('Create Purchase Invoice'), null, 'primary');
        }
    }
});
"""

def run():
    frappe.db.delete("Client Script", {"dt": "Subcontractor Payment Certificate"})
    cs = frappe.new_doc("Client Script")
    cs.dt = "Subcontractor Payment Certificate"
    cs.view = "Form"
    cs.enabled = 1
    cs.script = SCRIPT_CODE
    cs.insert(ignore_permissions=True)
    frappe.db.commit()
    frappe.clear_cache()
    print("SUCCESS: 'Create Purchase Invoice' button configured.")
