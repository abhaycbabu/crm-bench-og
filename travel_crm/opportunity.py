@frappe.whitelist()
def get_lead_destination(lead_name):
    frappe.msgprint(f"Getting destination for Lead: {lead_name}")
    lead = frappe.get_doc("Lead", lead_name)
    return {"destination": lead.custom_preferred_destination}
