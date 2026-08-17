frappe.ui.form.on('Daily Progress Report', {
    refresh(frm) {
        if (frm.is_new() && !frm.doc.report_date) {
            frm.set_value('report_date', frappe.datetime.get_today());
        }
        if (frm.is_new() && !frm.doc.site_engineer) {
            frm.set_value('site_engineer', frappe.session.user);
        }
    },
    project(frm) {
        if (frm.doc.project) {
            // Filter task dropdown to only show tasks belonging to this project
            frm.set_query('task', 'progress_details', () => {
                return {
                    filters: {
                        project: frm.doc.project
                    }
                };
            });
        }
    }
});
