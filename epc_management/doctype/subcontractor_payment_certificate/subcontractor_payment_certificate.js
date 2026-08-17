frappe.ui.form.on('Subcontractor Payment Certificate', {
    refresh(frm) {
        // When document is submitted (docstatus === 1), show Create > Purchase Invoice
        if (frm.doc.docstatus === 1) {
            frm.add_custom_button(__('Purchase Invoice'), function() {
                frappe.model.open_mapped_doc({
                    method: 'epc_management.doctype.subcontractor_payment_certificate.subcontractor_payment_certificate.make_purchase_invoice',
                    frm: frm
                });
            }, __('Create'));
            frm.page.set_inner_btn_group_as_primary(__('Create'));
        }
    },

    measurement_book(frm) {
        if (frm.doc.measurement_book) {
            frappe.db.get_doc('Measurement Book', frm.doc.measurement_book).then(mb => {
                frm.set_value('project', mb.project);
                frm.set_value('subcontractor', mb.subcontractor);
                frm.set_value('purchase_order', mb.purchase_order);
                frm.set_value('gross_amount', mb.total_measured_amount || 0);
            });
        }
    }
});