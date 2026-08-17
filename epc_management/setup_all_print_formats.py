import frappe

DPR_HTML = """
<div style="font-family: Arial, sans-serif; padding: 10px; font-size: 11px;">
    <!-- Header -->
    <div style="text-align: center; border-bottom: 2px solid #000; padding-bottom: 8px; margin-bottom: 12px;">
        <h2 style="margin: 0; text-transform: uppercase; font-size: 16px;">Daily Progress Report (DPR)</h2>
        <p style="margin: 2px 0 0 0; font-size: 12px; color: #555;">Daily Site Execution, Manpower & Machinery Log</p>
    </div>

    <!-- Metadata Table -->
    <table style="width: 100%; border-collapse: collapse; margin-bottom: 12px;" border="0">
        <tr>
            <td style="width: 18%; padding: 3px 0;"><strong>Report Ref:</strong></td>
            <td style="width: 32%; padding: 3px 0;">{{ doc.name }}</td>
            <td style="width: 18%; padding: 3px 0;"><strong>Report Date:</strong></td>
            <td style="width: 32%; padding: 3px 0;">{{ frappe.utils.formatdate(doc.report_date) }}</td>
        </tr>
        <tr>
            <td style="padding: 3px 0;"><strong>Project:</strong></td>
            <td style="padding: 3px 0;">{{ doc.project }}</td>
            <td style="padding: 3px 0;"><strong>Weather Condition:</strong></td>
            <td style="padding: 3px 0;">{{ doc.weather or 'Normal' }}</td>
        </tr>
        <tr>
            <td style="padding: 3px 0;"><strong>Site Engineer:</strong></td>
            <td style="padding: 3px 0;">{{ doc.site_engineer }}</td>
            <td style="padding: 3px 0;"><strong>Status:</strong></td>
            <td style="padding: 3px 0; text-transform: uppercase; font-weight: bold;">{{ 'Submitted' if doc.docstatus == 1 else 'Draft' }}</td>
        </tr>
    </table>

    <!-- 1. Manpower Log -->
    <h4 style="margin: 8px 0 4px 0; text-transform: uppercase; border-bottom: 1px solid #ccc; padding-bottom: 2px;">1. Site Manpower & Labor Deployment</h4>
    <table style="width: 100%; border-collapse: collapse; margin-bottom: 12px;" border="1" cellpadding="4">
        <thead>
            <tr style="background-color: #f2f2f2; text-align: center;">
                <th style="width: 8%;">S.No</th>
                <th style="width: 42%;">Trade / Skill Designation</th>
                <th style="width: 25%;">Category</th>
                <th style="width: 12%;">Headcount</th>
                <th style="width: 13%;">Overtime (Hrs)</th>
            </tr>
        </thead>
        <tbody>
            {% set total_labor = [0] %}
            {% set total_ot = [0] %}
            {% for item in doc.manpower_details %}
            {% if total_labor.append(total_labor.pop() + (item.count or 0)) %}{% endif %}
            {% if total_ot.append(total_ot.pop() + (item.overtime_hours or 0)) %}{% endif %}
            <tr>
                <td style="text-align: center;">{{ loop.index }}</td>
                <td>{{ item.trade }}</td>
                <td style="text-align: center;">{{ item.category or 'General' }}</td>
                <td style="text-align: right; font-weight: bold;">{{ item.count or 0 }}</td>
                <td style="text-align: right;">{{ item.overtime_hours or 0 }}</td>
            </tr>
            {% endfor %}
            <tr style="background-color: #fafafa; font-weight: bold;">
                <td colspan="3" style="text-align: right;">Total Labor Deployed:</td>
                <td style="text-align: right;">{{ total_labor[0] }}</td>
                <td style="text-align: right;">{{ total_ot[0] }} hrs</td>
            </tr>
        </tbody>
    </table>

    <!-- 2. Equipment Log -->
    <h4 style="margin: 8px 0 4px 0; text-transform: uppercase; border-bottom: 1px solid #ccc; padding-bottom: 2px;">2. Machinery & Heavy Equipment Deployment</h4>
    <table style="width: 100%; border-collapse: collapse; margin-bottom: 12px;" border="1" cellpadding="4">
        <thead>
            <tr style="background-color: #f2f2f2; text-align: center;">
                <th style="width: 8%;">S.No</th>
                <th style="width: 42%;">Equipment / Machinery Name</th>
                <th style="width: 16%;">Working (Hrs)</th>
                <th style="width: 16%;">Idle / Breakdown</th>
                <th style="width: 18%;">Fuel Consumed (L)</th>
            </tr>
        </thead>
        <tbody>
            {% for item in doc.equipment_details %}
            <tr>
                <td style="text-align: center;">{{ loop.index }}</td>
                <td>{{ item.equipment_name }}</td>
                <td style="text-align: right;">{{ item.working_hours or 0 }}</td>
                <td style="text-align: right;">{{ item.breakdown_hours or 0 }}</td>
                <td style="text-align: right; font-weight: bold;">{{ item.fuel_consumed or 0 }} L</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>

    <!-- 3. Work Progress -->
    {% if doc.progress_details %}
    <h4 style="margin: 8px 0 4px 0; text-transform: uppercase; border-bottom: 1px solid #ccc; padding-bottom: 2px;">3. Work Activities & Progress Completed</h4>
    <table style="width: 100%; border-collapse: collapse; margin-bottom: 12px;" border="1" cellpadding="4">
        <thead>
            <tr style="background-color: #f2f2f2; text-align: center;">
                <th style="width: 8%;">S.No</th>
                <th style="width: 62%;">Work Description & Location</th>
                <th style="width: 15%;">Quantity Output</th>
                <th style="width: 15%;">Unit</th>
            </tr>
        </thead>
        <tbody>
            {% for item in doc.progress_details %}
            <tr>
                <td style="text-align: center;">{{ loop.index }}</td>
                <td>{{ item.activity_description or item.task }}</td>
                <td style="text-align: right; font-weight: bold;">{{ item.quantity or 0 }}</td>
                <td style="text-align: center;">{{ item.uom or 'Nos' }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    {% endif %}

    <!-- Remarks -->
    {% if doc.remarks %}
    <div style="margin-bottom: 25px;">
        <strong>Site Notes / Safety Remarks:</strong> {{ doc.remarks }}
    </div>
    {% endif %}

    <!-- Signatures -->
    <div style="margin-top: 40px; display: flex; justify-content: space-between; font-size: 11px;">
        <div style="width: 45%; text-align: center; border-top: 1px solid #000; padding-top: 5px;">
            <strong>Recorded By</strong><br>
            Site Engineer / Section In-Charge
        </div>
        <div style="width: 45%; text-align: center; border-top: 1px solid #000; padding-top: 5px;">
            <strong>Reviewed & Approved</strong><br>
            Project Manager / Resident Engineer
        </div>
    </div>
</div>
"""

SPC_HTML = """
<div style="font-family: Arial, sans-serif; padding: 10px; font-size: 11px;">
    <!-- Header -->
    <div style="text-align: center; border-bottom: 2px solid #000; padding-bottom: 8px; margin-bottom: 15px;">
        <h2 style="margin: 0; text-transform: uppercase; font-size: 16px;">Subcontractor Interim Payment Certificate (IPC)</h2>
        <p style="margin: 2px 0 0 0; font-size: 12px; color: #555;">Official Abstract of Bill & Contractual Payment Authorization</p>
    </div>

    <!-- Contract Details Table -->
    <table style="width: 100%; border-collapse: collapse; margin-bottom: 15px;" border="0">
        <tr>
            <td style="width: 20%; padding: 4px 0;"><strong>Certificate Ref:</strong></td>
            <td style="width: 30%; padding: 4px 0;">{{ doc.name }}</td>
            <td style="width: 20%; padding: 4px 0;"><strong>Posting Date:</strong></td>
            <td style="width: 30%; padding: 4px 0;">{{ frappe.utils.formatdate(doc.posting_date) }}</td>
        </tr>
        <tr>
            <td style="padding: 4px 0;"><strong>Project:</strong></td>
            <td style="padding: 4px 0;">{{ doc.project }}</td>
            <td style="padding: 4px 0;"><strong>Measurement Book:</strong></td>
            <td style="padding: 4px 0;">{{ doc.measurement_book or 'Direct' }}</td>
        </tr>
        <tr>
            <td style="padding: 4px 0;"><strong>Subcontractor:</strong></td>
            <td style="padding: 4px 0;">{{ doc.subcontractor }}</td>
            <td style="padding: 4px 0;"><strong>Purchase Order:</strong></td>
            <td style="padding: 4px 0;">{{ doc.purchase_order or 'N/A' }}</td>
        </tr>
    </table>

    <!-- Financial Abstract Table -->
    <h4 style="margin: 10px 0 6px 0; text-transform: uppercase; border-bottom: 1px solid #ccc; padding-bottom: 2px;">Financial Statement of Certified Work</h4>
    <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px; font-size: 12px;" border="1" cellpadding="6">
        <thead>
            <tr style="background-color: #f2f2f2;">
                <th style="width: 10%; text-align: center;">Item</th>
                <th style="width: 60%;">Description of Financial Valuation</th>
                <th style="width: 30%; text-align: right;">Amount (INR)</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td style="text-align: center;">A</td>
                <td><strong>Gross Certified Value of Work Executed (as per MB)</strong></td>
                <td style="text-align: right; font-weight: bold;">{{ frappe.utils.fmt_money(doc.gross_amount, currency=doc.currency) }}</td>
            </tr>
            <tr>
                <td style="text-align: center;">B</td>
                <td>Less: Statutory Retention Money ({{ doc.retention_percentage or 5.0 }}%)</td>
                <td style="text-align: right; color: #c00;">- {{ frappe.utils.fmt_money(doc.retention_amount, currency=doc.currency) }}</td>
            </tr>
            <tr>
                <td style="text-align: center;">C</td>
                <td>Less: Mobilization / Advance Recovery</td>
                <td style="text-align: right; color: #c00;">- {{ frappe.utils.fmt_money(doc.advance_recovery or 0, currency=doc.currency) }}</td>
            </tr>
            <tr>
                <td style="text-align: center;">D</td>
                <td>Less: Material Issue / Other Contractual Deductions</td>
                <td style="text-align: right; color: #c00;">- {{ frappe.utils.fmt_money(doc.other_deductions or 0, currency=doc.currency) }}</td>
            </tr>
            <tr style="background-color: #f0f7ff; font-size: 13px; font-weight: bold;">
                <td style="text-align: center;">E</td>
                <td><strong>NET CERTIFIED AMOUNT PAYABLE (A - B - C - D)</strong></td>
                <td style="text-align: right; color: #004085; font-size: 14px;">{{ frappe.utils.fmt_money(doc.net_payable_amount, currency=doc.currency) }}</td>
            </tr>
        </tbody>
    </table>

    {% if doc.remarks %}
    <div style="margin-bottom: 30px;">
        <strong>Certificate Notes / Remarks:</strong> {{ doc.remarks }}
    </div>
    {% endif %}

    <!-- Signatures -->
    <div style="margin-top: 50px; display: flex; justify-content: space-between; font-size: 11px;">
        <div style="width: 30%; text-align: center; border-top: 1px solid #000; padding-top: 5px;">
            <strong>Prepared By</strong><br>
            Quantity Surveyor / Billing Eng.
        </div>
        <div style="width: 30%; text-align: center; border-top: 1px solid #000; padding-top: 5px;">
            <strong>Verified By</strong><br>
            Project Manager (Site)
        </div>
        <div style="width: 30%; text-align: center; border-top: 1px solid #000; padding-top: 5px;">
            <strong>Approved for Payment</strong><br>
            Commercial Head / Accounts
        </div>
    </div>
</div>
"""

def register_pf(name, doctype, html):
    if not frappe.db.exists("Print Format", name):
        pf = frappe.new_doc("Print Format")
        pf.name = name
        pf.doc_type = doctype
        pf.module = "EPC Management"
        pf.standard = "No"
        pf.custom_format = 1
        pf.html = html
        pf.insert(ignore_permissions=True)
        print(f"Created Print Format: {name}")
    else:
        frappe.db.set_value("Print Format", name, "html", html)
        print(f"Updated Print Format: {name}")

def run():
    register_pf("Standard DPR Site Diary", "Daily Progress Report", DPR_HTML)
    register_pf("Standard Payment Certificate (IPC)", "Subcontractor Payment Certificate", SPC_HTML)
    frappe.db.commit()
    frappe.clear_cache()
    print("SUCCESS: All EPC Print Formats Registered Successfully.")
