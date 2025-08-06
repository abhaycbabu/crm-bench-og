import frappe
from frappe.model.document import Document


class CustomerFeedback(Document):
    def on_submit(self):
        create_follow_up_task(self, "on_submit")

@frappe.whitelist()
def create_follow_up_task(doc, method):
	booking = frappe.get_doc("Travel Booking", doc.travel_booking)

	# Ensure there's a project to link
	if not booking.project:
		frappe.throw("No project linked to this booking.")

    # Determine priority based on rating
	priority = "High" if doc.rating and int(doc.rating) < 3 else "Medium"

    # Build detailed task description
	task_description = (
		f"Customer: {booking.customer}<br>"
		f"Booking ID: {booking.name}<br>"
		f"Rating: {doc.rating}/5<br>"
		f"Feedback: {doc.feedback or 'No comments provided.'}<br><br>"
		f"<b>Action:</b> Please follow up with the customer and address the issue appropriately."
	)



	task = frappe.get_doc({
		"doctype": "Task",
		"subject": f"Follow-up: {booking.customer}",
		"project": booking.project,
		"status": "Open",
		"priority": priority,
		"description": task_description,
		"reference_type": "Customer Feedback",
		"reference_name": doc.name
	})

    # Optional: assign to Ops team member based on destination
    # assigned_to = frappe.db.get_value("Destination", booking.destination, "ops_team_user")
    # if assigned_to:
    #     task.append("assignments", {
    #         "assigned_to": assigned_to
    #     })

	task.insert(ignore_permissions=True)
	frappe.db.set_value("Customer Feedback", doc.name, "follow_up_task", task.name)
	frappe.msgprint(f"Follow-up Task <b>{task.name}</b> created.")

	# If rating is high, create a gift task
	if int(doc.rating) >= 4:
		gift_task = frappe.get_doc({
			"doctype": "Task",
			"subject": f"Send Gift: {booking.customer} [{doc.name}]",
			"project": booking.project,
			"status": "Open",
			"priority": "Medium",
			"description": (
				f"Customer gave {doc.rating}/5 rating.<br>"
				f"Feedback: {doc.feedback or 'No feedback'}<br>"
				f"Send a thank-you gift or appreciation."
			),
		})
		gift_task.insert(ignore_permissions=True)
		frappe.db.set_value("Customer Feedback", doc.name, "gift_status", "Not Started")
		frappe.msgprint(f"🎁 Gift Task <b>{gift_task.name}</b> created.")


# If the task is related to a gift, mark it as sent when completed
import re

def mark_gift_sent(task_doc, method):
    if task_doc.status == "Completed" and task_doc.subject.startswith("Send Gift"):
        # Try to extract Customer Feedback ID in square brackets
        match = re.search(r'\[(.*?)\]', task_doc.subject)
        if match:
            feedback_id = match.group(1)
            frappe.db.set_value("Customer Feedback", feedback_id, "gift_status", "Gift Sent")
