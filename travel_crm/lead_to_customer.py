import frappe
from frappe.model.mapper import get_mapped_doc

# Auto fill Customer expected travel date, preferred destination, budget, group size, and visa type
@frappe.whitelist()
def make_customer(source_name, target_doc=None):
    def set_missing_values(source, target):
        target.custom_expected_travel_date = source.custom_expected_travel_date
        target.custom_preferred_destination = source.custom_preferred_destination
        target.custom_budget_range = source.custom_budget_range
        target.custom_group_size = source.custom_group_size
        target.custom_visa_type = source.custom_visa_type

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
