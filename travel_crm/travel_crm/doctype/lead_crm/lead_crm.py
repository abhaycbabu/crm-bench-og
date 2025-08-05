# Copyright (c) 2025, abhay and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class LeadCRM(Document):
    def validate(self):
        restrict_status_change(self)

def restrict_status_change(doc):
    allowed_statuses = ["Qualified", "Quoted", "Converted"]
    current_user = frappe.session.user

    # Skip for administrator
    if current_user == "Administrator":
        return

    # Skip if status is not being changed or is not in the restricted list
    if not doc.has_value_changed("lead_status") or doc.lead_status not in allowed_statuses:
        return

    if doc.assigned_sales_person != current_user:
        frappe.throw("You are not allowed to change the status to this value. Only the assigned sales person can do that.")


@frappe.whitelist()
def get_sales_team_users(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql("""
        SELECT DISTINCT u.name, CONCAT(u.full_name, ' (', u.name, ')')
        FROM `tabUser` u
        JOIN `tabHas Role` hr ON hr.parent = u.name
        WHERE hr.role = 'Sales Team'
        AND u.enabled = 1
        AND (u.name LIKE %(txt)s OR u.full_name LIKE %(txt)s)
        LIMIT 20
    """, {"txt": f"%{txt}%"})

def get_permission_query_conditions(user):
    if user == "Administrator":
        return ""

    return f"""
        `tabLead CRM`.assigned_sales_person = '{user}'

    """

def has_permission(doc, ptype, user):
    if user == "Administrator":
        return True
    return (
        doc.assigned_sales_person == user
    )
