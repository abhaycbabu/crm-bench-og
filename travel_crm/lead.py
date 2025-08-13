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


# import traceback

# def auto_create_opportunity(doc, method):
#     try:
#         status_changed = False

#         if doc.qualification_status == "Qualified":
#             if doc.status != "Opportunity":
#                 doc.status = "Opportunity"
#                 status_changed = True
#         else:
#             if doc.status != "Lead":
#                 doc.status = "Lead"
#                 status_changed = True

#         if status_changed:
#             doc.save(ignore_permissions=True)

#         # Avoid duplicate opportunity
#         if frappe.db.exists("Opportunity", {"party_name": doc.name}):
#             return

#         # Create Opportunity
#         opportunity = frappe.new_doc("Opportunity")
#         opportunity.opportunity_from = "Lead"
#         opportunity.party_name = doc.name
#         opportunity.enquiry_type = "Sales"
#         opportunity.custom_destination = doc.custom_preferred_destination
#         opportunity.transaction_date = frappe.utils.nowdate()
#         opportunity.expected_closing = doc.custom_expected_travel_date
#         opportunity.company = frappe.defaults.get_user_default("Company")
#         opportunity.save(ignore_permissions=True)
#         frappe.db.commit()

#     except Exception as e:
#         frappe.log_error(title="Auto Create Opportunity Error", message=traceback.format_exc())
#         frappe.throw("Error while auto-creating Opportunity. Check error log.")

