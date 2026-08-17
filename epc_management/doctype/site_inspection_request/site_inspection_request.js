frappe.ui.form.on('Site Inspection Request', {
    refresh(frm) {
        if (frm.is_new() && !frm.doc.inspection_date) {
            frm.set_value('inspection_date', frappe.datetime.get_today());
        }
    }
});
