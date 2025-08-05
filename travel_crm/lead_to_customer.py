import frappe
from frappe.model.mapper import get_mapped_doc

#auto fill customer expected travel date and preferred destination
@frappe.whitelist()
def make_customer(source_name, target_doc=None):
    def set_missing_values(source, target):
        target.custom_expected_travel_date = source.custom_expected_travel_date
        target.custom_preferred_destination = source.custom_preferred_destination

    return get_mapped_doc(
        "Lead",
        source_name,
        {
            "Lead": {
                "doctype": "Customer",
                "field_map": {
                    "lead_name": "customer_name",
                    "company_name": "customer_name"
                },
            }
        },
        target_doc,
        set_missing_values
    )
