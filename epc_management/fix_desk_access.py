import frappe

def run():
    # 1. Ensure desk_access is enabled for all custom EPC roles
    epc_roles = ["EPC Site Engineer", "EPC QA-QC Inspector", "EPC Project Manager"]
    for role_name in epc_roles:
        if frappe.db.exists("Role", role_name):
            frappe.db.set_value("Role", role_name, "desk_access", 1)
            print(f"Enabled desk_access for: {role_name}")

    # 2. Assign standard Desk & Project roles to all EPC team members
    users = [
        "site.engineer@cosmoops.com",
        "qaqc.inspector@cosmoops.com",
        "project.manager@cosmoops.com",
        "accounts.officer@cosmoops.com"
    ]

    has_desk_user = frappe.db.exists("Role", "Desk User")

    for user_email in users:
        if frappe.db.exists("User", user_email):
            u_doc = frappe.get_doc("User", user_email)
            u_doc.user_type = "System User"
            
            if has_desk_user and not frappe.db.exists("Has Role", {"parent": user_email, "role": "Desk User"}):
                u_doc.append("roles", {"role": "Desk User"})
            
            # Add Projects User for standard desk navigation
            if not frappe.db.exists("Has Role", {"parent": user_email, "role": "Projects User"}):
                u_doc.append("roles", {"role": "Projects User"})
                
            u_doc.save(ignore_permissions=True)
            print(f"Updated Desk permissions for: {user_email}")

    # 3. Grant Page & Workspace read permissions to EPC roles
    for role_name in epc_roles:
        for dt in ["Page", "Workspace"]:
            if not frappe.db.exists("Custom DocPerm", {"parent": dt, "role": role_name}):
                try:
                    docperm = frappe.new_doc("Custom DocPerm")
                    docperm.parent = dt
                    docperm.parenttype = "DocType"
                    docperm.parentfield = "permissions"
                    docperm.role = role_name
                    docperm.read = 1
                    docperm.insert(ignore_permissions=True)
                except Exception:
                    pass

    frappe.db.commit()
    frappe.clear_cache()
    print("SUCCESS: Desk and Page permissions configured.")