import frappe
from frappe.utils import now

def auto_qualify_lead(doc, method=None):
    if doc.doctype != "Lead":
        return

    # Conditions for auto qualification
    if (
        doc.custom_preferred_destination and
        doc.custom_expected_travel_date and
        doc.custom_budget_range and float(doc.custom_budget_range or 0) >= 20000 and
        doc.custom_group_size and int(doc.custom_group_size or 0) >= 1
    ):
        doc.qualification_status = "Qualified"
        doc.qualified_by = frappe.session.user
        doc.qualified_on = now()
    else:
        doc.qualification_status = "Unqualified"
