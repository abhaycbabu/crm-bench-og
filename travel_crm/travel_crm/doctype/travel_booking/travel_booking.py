import frappe
from frappe import _
from frappe.utils import nowdate

from frappe.model.document import Document
from frappe.permissions import has_permission


# 
# def date_overlap(start1, end1, start2, end2):
#     return max(start1, start2) <= min(end1, end2)


class TravelBooking(Document):
    def validate(self):

        # if self.get_doc_before_save():
        #     old_status = self.get_doc_before_save().status
        #     if (
        #         old_status != self.status and 
        #         self.status in ["Draft", "Pending", "Completed"] and
        #         not frappe.flags.allow_status_override
        #     ):
        #         frappe.throw(f"You cannot manually change status to '{self.status}'.")    

        filters = {"name": ["!=", self.name]}

        # 1. Hotel conflict
        if self.hotel and self.check_in and self.check_out:
            conflict = frappe.db.get_value("Travel Booking", {
                **filters,
                "hotel": self.hotel,
                "check_in": ["<=", self.check_out],
                "check_out": [">=", self.check_in]
            }, "name")
            if conflict:
                frappe.throw(_("Conflict: Hotel {0} is already booked between {1} and {2}. Conflicting Booking: <a href='/app/travel-booking/{3}'>{3}</a>").format(
                    self.hotel, self.check_in, self.check_out, conflict
                ), title="Booking Conflict")

        # 2. Cab conflict
        if self.cab and self.pickup_date and self.drop_date:
            conflict = frappe.db.get_value("Travel Booking", {
                **filters,
                "cab": self.cab,
                "pickup_date": ["<=", self.drop_date],
                "drop_date": [">=", self.pickup_date]
            }, "name")
            if conflict:
                frappe.throw(_("Conflict: Cab {0} is already booked between {1} and {2}. Conflicting Booking: <a href='/app/travel-booking/{3}'>{3}</a>").format(
                    self.cab, self.pickup_date, self.drop_date, conflict
                ), title="Booking Conflict")

        # 3. Activity conflict
        if self.activities:
            for row in self.activities:
                if row.activity and row.activity_date:
                    # Find other bookings with same activity and same activity_date
                    conflict = frappe.db.sql("""
                        SELECT tb.name
                        FROM `tabTravel Booking` tb
                        JOIN `tabSelected Activity` sa ON sa.parent = tb.name
                        WHERE tb.name != %s
                        AND sa.activity = %s
                        AND sa.activity_date = %s
                        AND tb.docstatus < 2
                        LIMIT 1
                    """, (self.name, row.activity, row.activity_date))

                    if conflict:
                        conflict_name = conflict[0][0]
                        frappe.throw(
                            _("Conflict: Activity {0} is already booked on {1}. Conflicting Booking: <a href='/app/travel-booking/{2}'>{2}</a>").format(
                                row.activity, row.activity_date, conflict_name
                            ),
                            title="Activity Booking Conflict"
                        )


        # 4. Ops Person conflict
        if self.assigned_ops_person and self.travel_date_starting and self.travel_date_ending:
            conflict = frappe.db.get_value("Travel Booking", {
                **filters,
                "assigned_ops_person": self.assigned_ops_person,
                "travel_date_starting": ["<=", self.travel_date_ending],
                "travel_date_ending": [">=", self.travel_date_starting]
            }, "name")
            if conflict:
                frappe.throw(_("Conflict: Ops person {0} is already assigned between {1} and {2}. Conflicting Booking: <a href='/app/travel-booking/{3}'>{3}</a>").format(
                    self.assigned_ops_person, self.travel_date_starting, self.travel_date_ending, conflict
                ), title="Booking Conflict")

def get_permission_query_conditions(user):
    if not user or user == "Administrator":
        return None

    if "Sales Team" in frappe.get_roles(user):
        return None  # Full access

    conditions = []

    if "Ops Team" in frappe.get_roles(user):
        conditions.append(f"`tabTravel Booking`.assigned_ops_person = '{user}'")

    vendor_info = frappe.get_value("Destination Vendor", {"email": user}, ["name", "destination"], as_dict=True)

    if vendor_info:
        conditions.append(f"""(
            `tabTravel Booking`.destination = '{vendor_info.destination}' AND
            (
                `tabTravel Booking`.hotel = '{vendor_info.name}' OR
                `tabTravel Booking`.cab = '{vendor_info.name}'
            )
        )""")
        # Note: We removed `.activities` check here because it's a child table

    return " OR ".join(f"({c})" for c in conditions) if conditions else "0=1"



def has_permission(doc, ptype=None, user=None):
    if not user or user == "Administrator":
        return True

    roles = frappe.get_roles(user)

    if "Sales Team" in roles:
        return True

    if "Ops Team" in roles:
        if doc.assigned_ops_person == user:
            return True

    # Destination Vendor logic
    vendor = frappe.get_value("Destination Vendor", {"email": user}, "name")
    vendor_destination = frappe.get_value("Destination Vendor", {"email": user}, "destination")

    if not vendor or not vendor_destination:
        return False

    if (
        doc.destination == vendor_destination and (
            doc.hotel == vendor or
            doc.cab == vendor or
            vendor in [a.vendor for a in doc.activities]
        )
    ):
        return True

    return False



#Allow "Sales Team" to Send Vendor Options        
@frappe.whitelist()
def send_vendor_options(docname):
    if "Sales Team" not in frappe.get_roles():
        frappe.throw("Not permitted")

    booking = frappe.get_doc("Travel Booking", docname)

    # Step 1: Fetch vendor options by destination
    vendors = frappe.get_all("Destination Vendor", 
        filters={
            "destination": booking.destination,
            # "status": "Active"
        },
        fields=["vendor_name", "vendor_type", "contact_person", "phone", "email", "base_price"]
    )

    # Step 2: Compose the email content
    vendor_table = ""
    for v in vendors:
        vendor_table += f"""
        <tr>
            <td>{v.vendor_name}</td>
            <td>{v.vendor_type}</td>
            <td>{v.contact_person}</td>
            <td>{v.phone}</td>
            # <td>{v.email}</td>
            <td>{v.base_price}</td>
        </tr>
        """

    html = f"""
    <h3>Recommended Vendors for Your Trip</h3>
    <p>Here are some options based on your destination: <b>{booking.destination}</b></p>
    <table border=1 cellpadding=5 cellspacing=0>
        <thead>
            <tr>
                <th>Name</th>
                <th>Type</th>
                <th>Contact</th>
                <th>Phone</th>
                <th>Email</th>
                <th>Base Price</th>
            </tr>
        </thead>
        <tbody>
            {vendor_table}
        </tbody>
    </table>
    """

    # Step 3: Send email to customer
    customer = frappe.get_doc("Customer", booking.customer)
    # frappe.sendmail(
    #     recipients = [customer.email_id],
    #     subject=f"Vendor Options for Your Trip to {booking.destination}",
    #     message=html
    # )
    frappe.msgprint("Email content preview:<br><br>" + html)
    frappe.msgprint("Vendor options sent successfully.")


#filter assigned_Ops_team in travel booking
@frappe.whitelist()
def get_ops_team_users(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql("""
        SELECT DISTINCT u.name, u.full_name
        FROM `tabUser` u
        JOIN `tabHas Role` hr ON hr.parent = u.name
        WHERE hr.role = 'Ops Team'
        AND u.enabled = 1
        AND (u.name LIKE %(txt)s OR u.full_name LIKE %(txt)s)
        LIMIT 20
    """, {"txt": f"%{txt}%"})

# Create Ops Project from Travel Booking
@frappe.whitelist()
def create_visa_project_with_tasks(booking_name):
    booking = frappe.get_doc("Travel Booking", booking_name)
    visa_type = booking.visa_type

    # Create the Visa Project
    project = frappe.get_doc({
        "doctype": "Project",
        "project_name": f"{visa_type} Visa - {booking.customer}",
        "custom_travel_booking": booking.name,
        "expected_start_date": booking.travel_date_starting,
        "expected_end_date": booking.travel_date_ending,
        "project_type": "Visa",
        "customer": booking.customer,
        "status": "Open"
    })
    project.insert()

    # Fetch tasks for this visa type
    visa_type_doc = frappe.get_doc("Visa Type", visa_type)
    for row in visa_type_doc.tasks_template:
        frappe.get_doc({
            "doctype": "Task",
            "subject": row.task_title,
            "project": project.name,
            "status": "Open"
        }).insert()
    
    booking.reload()    
    booking.project = project.name
    booking.save(ignore_permissions=True)
    return project.name

#test visa percentage
def update_visa_task_progress(doc, method): 
    if doc.project:
        update_visa_progress(doc.project)

def update_visa_progress(project_name):
    total = frappe.db.count("Task", {"project": project_name})
    if total == 0:
        return

    completed = frappe.db.count("Task", {
        "project": project_name,
        "status": "Completed"
    })
    percent = int((completed / total) * 100)

    project = frappe.get_doc("Project", project_name)
    if project.custom_travel_booking:
        booking = frappe.get_doc("Travel Booking", project.custom_travel_booking)
        booking.visa_progress = percent
        booking.save(ignore_permissions=True)

# Create Quotation from Travel Booking
@frappe.whitelist()
def create_quotation_from_booking(booking_name):
    booking = frappe.get_doc("Travel Booking", booking_name)

    quotation = frappe.new_doc("Quotation")
    quotation.party_name = booking.customer  # assuming this is set
    quotation.quotation_to = "Customer"
    quotation.custom_travel_booking = booking.name  # if you added this custom field

    def get_vendor_price(vendor_name):
        vendor = frappe.get_value("Destination Vendor", {"vendor_name": vendor_name}, "base_price")
        return vendor if vendor else 0

    # Add Hotel
    if booking.hotel:
        quotation.append("items", {
            "item_code": "TRAVEL-PKG-001",
            "item_name": booking.hotel,
            "description": f"Hotel stay at {booking.destination} by {booking.hotel}",
            "qty": 1,
            "rate": get_vendor_price(booking.hotel)
        })

    # Add Cab
    if booking.cab:
        quotation.append("items", {
            "item_code": "TRAVEL-PKG-001",
            "item_name": booking.cab,
            "description": f"Cab service at {booking.destination} by {booking.cab}",
            "qty": 1,
            "rate": get_vendor_price(booking.cab)
        })

    # Add Activities
    for activity in booking.activities:
        quotation.append("items", {
            "item_code": "TRAVEL-PKG-001",
            "item_name": activity.activity,
            "description": f"Activities at {booking.destination} by {activity.activity}",
            "qty": 1,
            "rate": activity.price
        })
    quotation.set_missing_values()
    quotation.calculate_taxes_and_totals()
    quotation.insert()
    return quotation.name


# Get Package Details
@frappe.whitelist()
def get_package_details(package):
    doc = frappe.get_doc("Travel Package", package)

    return {
        "base_price": doc.base_price,
        "package_items": [
            {
                "service_type": row.service_type,
                "vendor": row.vendor,
                "description": row.description,
                "rate_per_person": row.rate_per_person,
                "base_price": row.base_price
            }
            for row in doc.package_items
        ]
    }




#FETCH TRAVEL BOOKING: QUOTATION TO SLAESORDER TO SALES INVOICE
#no need until maually create sales order and sales invoice
def copy_booking_from_quotation(doc, method): #sales order
    if doc.quotation and not doc.travel_booking:
        travel_booking = frappe.db.get_value("Quotation", doc.quotation, "travel_booking")
        if travel_booking:
            doc.travel_booking = travel_booking

def copy_booking_from_sales_order(doc, method): #sales invoice
    if doc.sales_order and not doc.travel_booking:
        travel_booking = frappe.db.get_value("Sales Order", doc.sales_order, "travel_booking")
        if travel_booking:
            doc.travel_booking = travel_booking

#set status to completed on sales invoice submit
@frappe.whitelist()
def update_travel_booking_status_on_payment(doc, method):
    if doc.custom_travel_booking:
        travel_booking = frappe.get_doc("Travel Booking", doc.custom_travel_booking)
        if travel_booking.status != "Completed":
            travel_booking.status = "Completed"
            travel_booking.save()

#set advance payment on travel booking
@frappe.whitelist()
def create_advance_payment(customer, amount, reference_booking=None):
    from erpnext.accounts.party import get_party_account
    from frappe.utils import nowdate

    amount = float(amount)  # Ensure amount is numeric

    company = frappe.defaults.get_user_default("Company")
    party_account = get_party_account("Customer", customer, company)

    pe = frappe.new_doc("Payment Entry")
    pe.payment_type = "Receive"
    pe.party_type = "Customer"
    pe.party = customer
    pe.posting_date = nowdate()
    pe.paid_amount = amount
    pe.received_amount = amount
    pe.mode_of_payment = "Cash"
    pe.party_account = party_account
    pe.paid_to = frappe.db.get_value("Account", {"account_type": "Cash", "is_group": 0, "company": company}, "name")
    pe.custom_reference_booking = reference_booking  # optional custom field for traceability

    pe.set_missing_values()
    pe.set_exchange_rate()
    pe.insert()
    return pe.name

