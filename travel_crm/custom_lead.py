import frappe

#Allow Assigned To users to view leads assigned to them
def get_permission_query_conditions(user):
    if user == "Administrator":
        return None

    # Check both ToDo assignments and _assign field
    return f"""
        (
            EXISTS (
                SELECT 1 FROM `tabToDo`
                WHERE
                    `tabToDo`.reference_type = 'Lead'
                    AND `tabToDo`.reference_name = `tabLead`.name
                    AND `tabToDo`.owner = '{user}'
                    AND `tabToDo`.status != 'Cancelled'
            )
            OR
            JSON_CONTAINS(IFNULL(`tabLead`.`_assign`, '[]'), '\"{user}\"')
        )
    """


def has_permission(doc, user):
    if user == "Administrator":
        return True
    if "Sales Team" in frappe.get_roles(user):
        return True        

    assigned_users = frappe.get_all("ToDo", filters={
        "reference_type": "Lead",
        "reference_name": doc.name,
        "owner": user,
        "status": ("!=", "Cancelled")
    })

    return bool(assigned_users)
