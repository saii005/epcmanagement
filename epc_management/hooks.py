app_name = "epc_management"
app_title = "Apex Infra"
app_publisher = "Cosmoops"
app_description = "An ERPNext-Powered Construction & EPC Management Platform"
app_email = "saiguru@cosmoops.com"
app_license = "mit"

# Global JS for PWA Mobile App Support
app_include_js = "/assets/epc_management/js/pwa.js"
web_include_js = "/assets/epc_management/js/pwa.js"

# Link JavaScript to DocTypes
doctype_js = {
    "Subcontractor Payment Certificate": "doctype/subcontractor_payment_certificate/subcontractor_payment_certificate.js",
    "Measurement Book": "doctype/measurement_book/measurement_book.js",
    "Daily Progress Report": "doctype/daily_progress_report/daily_progress_report.js",
    "Site Inspection Request": "doctype/site_inspection_request/site_inspection_request.js",
    "Material Reconciliation": "doctype/material_reconciliation/material_reconciliation.js"
}

# Auto-Calculation Document Hooks
doc_events = {
    "Measurement Book": {
        "validate": "epc_management.doctype.measurement_book.measurement_book.calculate_mb_totals"
    },
    "Subcontractor Payment Certificate": {
        "validate": "epc_management.doctype.subcontractor_payment_certificate.subcontractor_payment_certificate.calculate_spc_totals"
    },
    "Material Reconciliation": {
        "validate": "epc_management.doctype.material_reconciliation.material_reconciliation.calculate_reconciliation_hook"
    }
}