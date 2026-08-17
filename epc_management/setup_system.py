import frappe

PRINT_HTML = """
<div style="font-family: Arial, sans-serif; padding: 10px;">
    <!-- Header -->
    <div style="text-align: center; border-bottom: 2px solid #000; padding-bottom: 10px; margin-bottom: 15px;">
        <h2 style="margin: 0; text-transform: uppercase;">Measurement Book (MB) Record</h2>
        <p style="margin: 4px 0 0 0; font-size: 13px; color: #555;">Official Interim Measurement & Verification Certificate</p>
    </div>

    <!-- Project & Contractor Metadata -->
    <table style="width: 100%; font-size: 12px; margin-bottom: 15px; border-collapse: collapse;">
        <tr>
            <td style="width: 20%; padding: 4px 0;"><strong>MB Reference:</strong></td>
            <td style="width: 30%; padding: 4px 0;">{{ doc.name }}</td>
            <td style="width: 20%; padding: 4px 0;"><strong>Date of Posting:</strong></td>
            <td style="width: 30%; padding: 4px 0;">{{ frappe.utils.formatdate(doc.posting_date) }}</td>
        </tr>
        <tr>
            <td style="padding: 4px 0;"><strong>Project:</strong></td>
            <td style="padding: 4px 0;">{{ doc.project }}</td>
            <td style="padding: 4px 0;"><strong>Measurement Period:</strong></td>
            <td style="padding: 4px 0;">{{ frappe.utils.formatdate(doc.period_from) or 'N/A' }} to {{ frappe.utils.formatdate(doc.period_to) or 'N/A' }}</td>
        </tr>
        <tr>
            <td style="padding: 4px 0;"><strong>Subcontractor:</strong></td>
            <td style="padding: 4px 0;">{{ doc.subcontractor }}</td>
            <td style="padding: 4px 0;"><strong>Purchase Order:</strong></td>
            <td style="padding: 4px 0;">{{ doc.purchase_order or 'Direct Agreement' }}</td>
        </tr>
    </table>

    <!-- Detailed Measurements Table -->
    <table style="width: 100%; border-collapse: collapse; font-size: 11px; margin-bottom: 15px;" border="1" cellpadding="5">
        <thead>
            <tr style="background-color: #f2f2f2; text-align: center;">
                <th style="width: 5%;">S.No</th>
                <th style="width: 30%;">Item Description & Location</th>
                <th style="width: 8%;">No.</th>
                <th style="width: 9%;">L (m)</th>
                <th style="width: 9%;">W (m)</th>
                <th style="width: 9%;">H (m)</th>
                <th style="width: 9%;">Qty</th>
                <th style="width: 6%;">Unit</th>
                <th style="width: 10%;">Rate</th>
                <th style="width: 14%;">Amount</th>
            </tr>
        </thead>
        <tbody>
            {% for item in doc.measurements %}
            <tr>
                <td style="text-align: center;">{{ loop.index }}</td>
                <td>
                    <strong>{{ item.work_description }}</strong>
                    {% if item.location_reference %}<br><small style="color: #666;">Loc: {{ item.location_reference }}</small>{% endif %}
                </td>
                <td style="text-align: center;">{{ item.numbers or 1 }}</td>
                <td style="text-align: right;">{{ item.length or '-' }}</td>
                <td style="text-align: right;">{{ item.width or '-' }}</td>
                <td style="text-align: right;">{{ item.height or '-' }}</td>
                <td style="text-align: right; font-weight: bold;">{{ frappe.utils.fmt_money(item.quantity, currency='') }}</td>
                <td style="text-align: center;">{{ item.uom or 'Nos' }}</td>
                <td style="text-align: right;">{{ frappe.utils.fmt_money(item.rate, currency=doc.currency) }}</td>
                <td style="text-align: right; font-weight: bold;">{{ frappe.utils.fmt_money(item.amount, currency=doc.currency) }}</td>
            </tr>
            {% endfor %}
            <tr style="background-color: #fafafa; font-weight: bold;">
                <td colspan="9" style="text-align: right; padding-right: 10px;">Total Measured Value:</td>
                <td style="text-align: right;">{{ frappe.utils.fmt_money(doc.total_measured_amount, currency=doc.currency) }}</td>
            </tr>
        </tbody>
    </table>

    <!-- Remarks -->
    {% if doc.remarks %}
    <div style="font-size: 11px; margin-bottom: 30px;">
        <strong>Remarks / Joint Notes:</strong> {{ doc.remarks }}
    </div>
    {% endif %}

    <!-- Signature Blocks -->
    <div style="margin-top: 50px; display: flex; justify-content: space-between; font-size: 11px;">
        <div style="width: 30%; text-align: center; border-top: 1px solid #000; padding-top: 5px;">
            <strong>Measured By</strong><br>
            Site Engineer / Surveyor
        </div>
        <div style="width: 30%; text-align: center; border-top: 1px solid #000; padding-top: 5px;">
            <strong>Accepted By</strong><br>
            Subcontractor Representative
        </div>
        <div style="width: 30%; text-align: center; border-top: 1px solid #000; padding-top: 5px;">
            <strong>Verified & Certified</strong><br>
            Project Manager / QA-QC
        </div>
    </div>
</div>
"""

def setup_print_format():
    if not frappe.db.exists("Print Format", "Standard Measurement Book"):
        pf = frappe.new_doc("Print Format")
        pf.name = "Standard Measurement Book"
        pf.doc_type = "Measurement Book"
        pf.module = "EPC Management"
        pf.standard = "No"
        pf.custom_format = 1
        pf.html = PRINT_HTML
        pf.insert(ignore_permissions=True)
        print("1. Standard Measurement Book Print Format: Created")
    else:
        frappe.db.set_value("Print Format", "Standard Measurement Book", "html", PRINT_HTML)
        print("1. Standard Measurement Book Print Format: Updated")

def setup_roles_and_permissions():
    roles = ["EPC Site Engineer", "EPC Project Manager", "EPC QA-QC Inspector"]
    for role_name in roles:
        if not frappe.db.exists("Role", role_name):
            frappe.get_doc({"doctype": "Role", "role_name": role_name, "desk_access": 1}).insert(ignore_permissions=True)
    print("2. EPC Roles: Verified & Active")

    perm_matrix = [
        ("Daily Progress Report", "EPC Site Engineer", 1, 1, 1, 1, 0, 0),
        ("Daily Progress Report", "EPC Project Manager", 1, 1, 1, 1, 1, 1),
        ("Measurement Book", "EPC Site Engineer", 1, 1, 1, 0, 0, 0),
        ("Measurement Book", "EPC Project Manager", 1, 1, 1, 1, 1, 1),
        ("Subcontractor Payment Certificate", "EPC Project Manager", 1, 1, 1, 1, 0, 1),
        ("Subcontractor Payment Certificate", "Accounts User", 1, 0, 0, 0, 0, 0),
        ("Site Inspection Request", "EPC Site Engineer", 1, 1, 1, 0, 0, 0),
        ("Site Inspection Request", "EPC QA-QC Inspector", 1, 1, 0, 1, 0, 1),
        ("Site Inspection Request", "EPC Project Manager", 1, 1, 1, 1, 1, 1),
    ]

    for doctype, role, r, w, c, s, ca, a in perm_matrix:
        if frappe.db.exists("DocType", doctype):
            if not frappe.db.exists("Custom DocPerm", {"parent": doctype, "role": role}):
                docperm = frappe.new_doc("Custom DocPerm")
                docperm.parent = doctype
                docperm.parenttype = "DocType"
                docperm.parentfield = "permissions"
                docperm.role = role
                docperm.read = r
                docperm.write = w
                docperm.create = c
                docperm.submit = s
                docperm.cancel = ca
                docperm.amend = a
                docperm.insert(ignore_permissions=True)
    print("3. Custom Permissions Matrix: Configured")

def run():
    setup_print_format()
    setup_roles_and_permissions()
    frappe.db.commit()
    print("--- EPC System Configuration Completed Successfully ---")
