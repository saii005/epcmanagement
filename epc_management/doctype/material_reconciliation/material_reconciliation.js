frappe.ui.form.on('Material Reconciliation', {
    refresh(frm) {
        if (frm.is_new() && !frm.doc.posting_date) {
            frm.set_value('posting_date', frappe.datetime.get_today());
        }
    }
});

frappe.ui.form.on('Material Reconciliation Item', {
    theoretical_qty(frm, cdt, cdn) { calculate_reconciliation_row(frm, cdt, cdn); },
    actual_qty(frm, cdt, cdn) { calculate_reconciliation_row(frm, cdt, cdn); },
    unit_rate(frm, cdt, cdn) { calculate_reconciliation_row(frm, cdt, cdn); }
});

function calculate_reconciliation_row(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    let theo = flt(row.theoretical_qty);
    let actual = flt(row.actual_qty);
    let rate = flt(row.unit_rate);
    let limit = flt(frm.doc.allowable_wastage_pct || 3.0);

    let variance = actual - theo;
    frappe.model.set_value(cdt, cdn, 'variance_qty', variance);

    let pct = theo > 0 ? ((variance / theo) * 100.0) : (actual > 0 ? 100.0 : 0.0);
    frappe.model.set_value(cdt, cdn, 'variance_pct', pct);

    let loss = Math.max(0.0, variance) * rate;
    frappe.model.set_value(cdt, cdn, 'financial_impact', loss);

    let status = "Within Tolerance";
    if (pct > limit) {
        status = "Excess Wastage / Pilferage Alert";
    } else if (pct < -5.0) {
        status = "Under-consumption";
    }
    frappe.model.set_value(cdt, cdn, 'status', status);
}