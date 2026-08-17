frappe.ui.form.on('Measurement Book', {
    refresh(frm) {
        if (frm.is_new() && !frm.doc.posting_date) {
            frm.set_value('posting_date', frappe.datetime.get_today());
        }

        // Filter Purchase Orders by selected Subcontractor & Project
        frm.set_query('purchase_order', () => {
            let filters = { docstatus: 1 }; // Only submitted Purchase Orders
            if (frm.doc.subcontractor) filters['supplier'] = frm.doc.subcontractor;
            if (frm.doc.project) filters['project'] = frm.doc.project;
            return { filters: filters };
        });
    },

    subcontractor(frm) {
        frm.set_value('purchase_order', '');
    },

    // When Purchase Order is selected, offer to auto-populate items and rates
    purchase_order(frm) {
        if (frm.doc.purchase_order) {
            frappe.db.get_doc('Purchase Order', frm.doc.purchase_order).then(po => {
                // If measurements table is empty, auto-populate contracted items
                if (!frm.doc.measurements || frm.doc.measurements.length === 0) {
                    (po.items || []).forEach(po_item => {
                        let row = frm.add_child('measurements');
                        row.work_description = po_item.item_name || po_item.item_code;
                        row.uom = po_item.uom || 'Nos';
                        row.unit_rate = po_item.rate || 0;
                        row.rate = po_item.rate || 0;
                        row.numbers = 1;
                    });
                    frm.refresh_field('measurements');
                    frappe.show_alert({
                        message: __('Auto-populated {0} contracted item(s) from Work Order', [po.items.length]),
                        indicator: 'green'
                    });
                }
            });
        }
    }
});

frappe.ui.form.on('Measurement Book Item', {
    numbers(frm, cdt, cdn) { calculate_row(frm, cdt, cdn); },
    length(frm, cdt, cdn) { calculate_row(frm, cdt, cdn); },
    width(frm, cdt, cdn) { calculate_row(frm, cdt, cdn); },
    height(frm, cdt, cdn) { calculate_row(frm, cdt, cdn); },
    unit_rate(frm, cdt, cdn) { calculate_row(frm, cdt, cdn); },
    rate(frm, cdt, cdn) { calculate_row(frm, cdt, cdn); },
    measurements_remove(frm) { calculate_total(frm); }
});

function calculate_row(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    let num = row.numbers || 1;
    let l = row.length || 0;
    let w = row.width || 0;
    let h = row.height || 0;

    let qty = (l || w || h) ? (num * (l || 1) * (w || 1) * (h || 1)) : (row.total_quantity || row.quantity || 0);
    
    frappe.model.set_value(cdt, cdn, 'total_quantity', qty);
    frappe.model.set_value(cdt, cdn, 'quantity', qty);

    let rate = row.unit_rate || row.rate || 0;
    let amt = qty * rate;

    frappe.model.set_value(cdt, cdn, 'total_amount', amt);
    frappe.model.set_value(cdt, cdn, 'amount', amt);

    calculate_total(frm);
}

function calculate_total(frm) {
    let total = 0;
    (frm.doc.measurements || []).forEach(row => {
        total += (row.total_amount || row.amount || 0);
    });
    frm.set_value('total_measured_amount', total);
}