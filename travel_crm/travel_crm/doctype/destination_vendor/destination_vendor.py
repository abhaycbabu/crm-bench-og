# Copyright (c) 2025, abhay and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class DestinationVendor(Document):
    def autoname(self):
        # Custom name format: VendorType - VendorName
        if self.vendor_type and self.vendor_name:
            self.name = f"{self.vendor_type} - {self.vendor_name}"

    def after_insert(self):
        if self.email and not frappe.db.exists("User", self.email):
            user = frappe.new_doc("User")
            user.email = self.email
            user.first_name = self.vendor_name
            user.send_welcome_email = 0
            user.append("roles", {
                "role": "Vendor"
            })  # This ensures proper child doc creation
            user.save(ignore_permissions=True)


def get_permission_query_conditions(user):
    if not user or user == "Administrator":
        return ""

    if "Ops Team" in frappe.get_roles(user):
        return """
            EXISTS (
                SELECT 1 FROM `tabTravel Booking` tb
                WHERE tb.assigned_ops_person = '{user}'
                AND (
                    tb.hotel = `tabDestination Vendor`.name OR
                    tb.cab = `tabDestination Vendor`.name OR
                    EXISTS (
                        SELECT 1 FROM `tabSelected Activity` tba
                        WHERE tba.parent = tb.name
                        AND tba.activity = `tabDestination Vendor`.name
                    )
                )
            )
        """.format(user=user)

    return ""

#filter Travel Booking to show only related bookings.
# @frappe.whitelist()
# def get_vendor_bookings():
#     vendor = frappe.get_value("Destination Vendor", {"email": frappe.session.user}, "name")
#     if not vendor:
#         frappe.throw("You are not assigned to any vendor.")

#     bookings = frappe.get_all("Travel Booking",
#         filters={"assigned_vendor": vendor},
#         fields=["name", "customer", "destination", "status", "date"]
#     )
#     return bookings