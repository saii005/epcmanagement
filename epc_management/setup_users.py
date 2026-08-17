import frappe
from frappe.utils.password import update_password

def run():
    project_name = frappe.db.get_value("Project", {"project_name": ["like", "%Metro Line%"]}, "name") or "PROJ-0001"

    users = [
        {
            "email": "site.engineer@cosmoops.com",
            "first_name": "Ravi",
            "last_name": "Kumar",
            "roles": ["EPC Site Engineer", "Stock User"],
            "restricted_project": project_name
        },
        {
            "email": "qaqc.inspector@cosmoops.com",
            "first_name": "Ananya",
            "last_name": "Sharma",
            "roles": ["EPC QA-QC Inspector"],
            "restricted_project": project_name
        },
        {
            "email": "project.manager@cosmoops.com",
            "first_name": "Suresh",
            "last_name": "Menon",
            "roles": ["EPC Project Manager", "Projects User", "Stock Manager"],
            "restricted_project": None
        },
        {
            "email": "accounts.officer@cosmoops.com",
            "first_name": "Priya",
            "last_name": "Nair",
            "roles": ["Accounts User", "Accounts Manager"],
            "restricted_project": None
        }
    ]

    for u in users:
        # 1. Create / Update User as System User
        if not frappe.db.exists("User", u["email"]):
            user_doc = frappe.new_doc("User")
            user_doc.email = u["email"]
            user_doc.first_name = u["first_name"]
            user_doc.last_name = u["last_name"]
            user_doc.user_type = "System User"
            user_doc.send_welcome_email = 0
            user_doc.insert(ignore_permissions=True)
        else:
            user_doc = frappe.get_doc("User", u["email"])
            user_doc.user_type = "System User"
            user_doc.enabled = 1

        # 2. Assign Roles
        for role in u["roles"]:
            if not frappe.db.exists("Has Role", {"parent": u["email"], "role": role}):
                user_doc.append("roles", {"role": role})
        user_doc.save(ignore_permissions=True)

        # 3. Encrypt and set password in Auth table
        update_password(u["email"], "Password123")
        print(f"Password set for: {u['email']}")

        # 4. Set Site-Level User Permissions
        if u["restricted_project"]:
            if not frappe.db.exists("User Permission", {"user": u["email"], "allow": "Project", "for_value": u["restricted_project"]}):
                up = frappe.new_doc("User Permission")
                up.user = u["email"]
                up.allow = "Project"
                up.for_value = u["restricted_project"]
                up.insert(ignore_permissions=True)

    frappe.db.commit()
    frappe.clear_cache()
    print("SUCCESS: All user passwords and site permissions are active.")