import frappe

def set_travel_booking_in_quotation(doc, method):
    if not doc.travel_booking and doc.party_name:
        booking_name = frappe.db.get_value("Travel Booking", {"customer": doc.party_name}, "name")
        if booking_name:
            doc.travel_booking = booking_name

def copy_booking_from_quotation(doc, method):
    if doc.quotation and not doc.travel_booking:
        travel_booking = frappe.db.get_value("Quotation", doc.quotation, "travel_booking")
        if travel_booking:
            doc.travel_booking = travel_booking

def copy_booking_from_sales_order(doc, method):
    if doc.sales_order and not doc.travel_booking:
        travel_booking = frappe.db.get_value("Sales Order", doc.sales_order, "travel_booking")
        if travel_booking:
            doc.travel_booking = travel_booking

@frappe.whitelist()
def update_travel_booking_status_on_payment(doc, method):
    if doc.travel_booking:
        travel_booking = frappe.get_doc("Travel Booking", doc.travel_booking)
        if travel_booking.status != "Completed":
            travel_booking.status = "Completed"
            travel_booking.save()