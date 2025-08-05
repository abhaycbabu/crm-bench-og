# import frappe

# def get_permission_query_conditions(user):
#     if user == "Administrator":
#         return None

#     return f"""
#         EXISTS (
#             SELECT 1 FROM `tabToDo`
#             WHERE
#                 `tabToDo`.reference_type = 'Task'
#                 AND `tabToDo`.reference_name = `tabTask`.name
#                 AND `tabToDo`.owner = '{user}'
#                 AND `tabToDo`.status != 'Cancelled'
#         )
#         AND EXISTS (
#             SELECT 1 FROM `tabProject`, `tabTravel Booking`
#             WHERE
#                 `tabProject`.name = `tabTask`.project
#                 AND `tabTravel Booking`.project = `tabProject`.name
#                 AND (
#                     JSON_CONTAINS(IFNULL(`tabTravel Booking`.`_assign`, '[]'), '\"{user}\"')
#                     OR EXISTS (
#                         SELECT 1 FROM `tabToDo` AS booking_todo
#                         WHERE
#                             booking_todo.reference_type = 'Travel Booking'
#                             AND booking_todo.reference_name = `tabTravel Booking`.name
#                             AND booking_todo.owner = '{user}'
#                             AND booking_todo.status != 'Cancelled'
#                     )
#                 )
#         )
#     """

# def has_permission(doc, user):
#     if user == "Administrator":
#         return True

#     # First check if task is assigned
#     is_assigned = frappe.get_all("ToDo", filters={
#         "reference_type": "Task",
#         "reference_name": doc.name,
#         "owner": user,
#         "status": ("!=", "Cancelled")
#     })

#     if not is_assigned:
#         return False

#     # Then check if parent travel booking is assigned
#     if doc.project:
#         project = frappe.db.get_value("Project", doc.project, "name")
#         travel_booking = frappe.get_value("Travel Booking", {"project": project}, "name")

#         if travel_booking:
#             # check assign or ToDo in travel booking
#             is_booking_assigned = frappe.get_all("ToDo", filters={
#                 "reference_type": "Travel Booking",
#                 "reference_name": travel_booking,
#                 "owner": user,
#                 "status": ("!=", "Cancelled")
#             }) or f'"{user}"' in (frappe.db.get_value("Travel Booking", travel_booking, "_assign") or "[]")

#             return bool(is_booking_assigned)

#     return False


import frappe

def get_permission_query_conditions(user):
    if not user or user == "Administrator":
        return None

    roles = frappe.get_roles(user)
    if "Sales Team" in roles:
        return f"`tabTask`.owner = '{user}'"
    if "Ops Team" in roles:
        return f"`tabTask`.custom_assigned_ops_person = '{user}'"

    # Other users have no access
    return "0=1"

def has_permission(doc, ptype=None, user=None):
    if not user or user == "Administrator":
        return True

    roles = frappe.get_roles(user)

    # Sales Team: full access (optional, remove if not needed)
    if "Sales Team" in roles:
        return True

    # Ops Team: Only access if assigned through customer_assigned_ops_person
    if "Ops Team" in roles:
        if doc.custom_assigned_ops_person == user:
            return True if ptype in ("read", "write", "submit", "cancel", "delete", "print", "report") else False

    # No access for others
    return False



