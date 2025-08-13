import frappe

def set_destination_from_lead(doc, method):
    """Set custom_destination in Opportunity from Lead"""
    if doc.opportunity_from == "Lead" and doc.party_name:
        lead_destination = frappe.db.get_value("Lead", doc.party_name, "custom_preferred_destination")
        if lead_destination:
            doc.custom_destination = lead_destination
