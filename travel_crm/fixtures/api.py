# def update_visa_task_progress(doc, method):
#     if doc.project:
#         update_visa_progress(doc.project)

# def update_visa_progress(project_name):
#     total = frappe.db.count("Task", {"project": project_name})
#     if total == 0:
#         return

#     completed = frappe.db.count("Task", {
#         "project": project_name,
#         "status": "Completed"
#     })
#     percent = int((completed / total) * 100)

#     project = frappe.get_doc("Project", project_name)
#     if project.travel_booking:
#         booking = frappe.get_doc("Travel Booking", project.travel_booking)
#         booking.visa_progress = percent
#         booking.save(ignore_permissions=True)
