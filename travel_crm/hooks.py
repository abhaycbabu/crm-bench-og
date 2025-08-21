app_name = "travel_crm"
app_title = "Travel Crm"
app_publisher = "abhay"
app_description = "About crm-erp selfho"
app_email = "abhay517@gmail.com"
app_license = "mit"



# doc_events = {
#     "Travel Booking": {
#         "get_permission_query_conditions": "travel_crm.permissions.travel_booking.get_permission_query_conditions"
#     }
# }

#vendors to only see their own destinations, or
#Salespersons to only see leads/clients assigned to them
permission_query_conditions = {
    "Travel Booking": "travel_crm.travel_crm.doctype.travel_booking.travel_booking.get_permission_query_conditions",
    "Destination Vendor": "travel_crm.travel_crm.doctype.destination_vendor.destination_vendor.get_permission_query_conditions",
    # "Lead CRM": "travel_crm.travel_crm.doctype.lead_crm.lead_crm.get_permission_query_conditions",
    "Lead": "travel_crm.custom_lead.get_permission_query_conditions",
    "Task": "travel_crm.task_permission.get_permission_query_conditions"

}

#“Should this user be allowed to view, edit, or delete this specific document?”
has_permission = {
    "Travel Booking": "travel_crm.travel_crm.doctype.travel_booking.travel_booking.has_permission",
    # "Lead CRM": "travel_crm.travel_crm.doctype.lead_crm.lead_crm.has_permission",
    "Lead": "travel_crm.custom_lead.has_permission",
    "Task": "travel_crm.task_permission.has_permission"


}

#filter color to lead status
doctype_list_js = {
    "Customer": "public/js/customer.js"
}
doctype_js = {
    "Opportunity": "public/js/opportunity.js",
    "Lead": "public/js/lead.js"
}

override_whitelisted_methods = {
    "erpnext.crm.doctype.lead.lead.make_customer": "travel_crm.lead_to_customer.make_customer"
}

# app_include_js = "/assets/travel_crm/js/lead_crm_list.js"

doc_events = {
    "Task": {
        "on_update": "travel_crm.travel_crm.doctype.travel_booking.travel_booking.update_visa_task_progress"
    },
    "Sales Invoice": {
        "on_submit": "travel_crm.travel_crm.doctype.travel_booking.travel_booking.update_travel_booking_status_on_payment"

    },
    "Customer Feedback": {
        "after_insert": "travel_crm.travel_crm.doctype.customer_feedback.customer_feedback.create_follow_up_task"
    },
    "Task": {
        "on_update": "travel_crm.travel_crm.doctype.customer_feedback.customer_feedback.mark_gift_sent"
    },
    "Lead": {
        "validate": "travel_crm.lead.auto_qualify_lead",
        # "on_update": "travel_crm.lead.auto_create_opportunity"
    },
 
    "Quotation": {
        "on_update": "travel_crm.travel_crm.doctype.travel_booking.travel_booking.update_booking_status_from_quotation"
    }


}


fixtures = [
    {
        "doctype": "Custom Field",
        "filters": [
            ["name", "in", [
                "Lead-custom_expected_travel_date",
                "Lead-custom_travel_type",
                "Lead-custom_preferred_destination",
                "Lead-custom_group_size",
                "Lead-custom_budget_range",
                "Lead-custom_visa_required",
                "Lead-custom_visa_type",
                "Lead-custom_lead_source",
                "Lead-custom_preferred_communication",
                "Lead-custom_whatsapp_number",
                "Lead-custom_travel_details",
                "Customer-custom_preferred_destination",
                "Customer-custom_expected_travel_date",
                "Sales Order-custom_travel_booking",
                "Task-custom_ops_remarks",
                "Task-custom_visa_document",
                "Project-custom_travel_booking",
                "Task-custom_assigned_ops_person",
                "Sales Invoice-custom_travel_booking",
                "Quotation-custom_travel_booking",
                "Payment Entry-custom_reference_booking",
                "Opportunity-custom_destination",
                "Opportunity-custom_travel_package",
                "Customer-custom_visa_type",
                "Customer-custom_group_size",
                "Customer-custom_budget_range"
            ]]
        ]
    }
]










# #filter sale team in Lead CRM
# doctype_js = {
#     "Lead CRM": "public/js/lead_crm.js"
# }
# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "travel_crm",
# 		"logo": "/assets/travel_crm/logo.png",
# 		"title": "Travel Crm",
# 		"route": "/travel_crm",
# 		"has_permission": "travel_crm.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/travel_crm/css/travel_crm.css"
# app_include_js = "/assets/travel_crm/js/travel_crm.js"

# include js, css files in header of web template
# web_include_css = "/assets/travel_crm/css/travel_crm.css"
# web_include_js = "/assets/travel_crm/js/travel_crm.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "travel_crm/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "travel_crm/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "travel_crm.utils.jinja_methods",
# 	"filters": "travel_crm.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "travel_crm.install.before_install"
# after_install = "travel_crm.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "travel_crm.uninstall.before_uninstall"
# after_uninstall = "travel_crm.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "travel_crm.utils.before_app_install"
# after_app_install = "travel_crm.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "travel_crm.utils.before_app_uninstall"
# after_app_uninstall = "travel_crm.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "travel_crm.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"travel_crm.tasks.all"
# 	],
# 	"daily": [
# 		"travel_crm.tasks.daily"
# 	],
# 	"hourly": [
# 		"travel_crm.tasks.hourly"
# 	],
# 	"weekly": [
# 		"travel_crm.tasks.weekly"
# 	],
# 	"monthly": [
# 		"travel_crm.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "travel_crm.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "travel_crm.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "travel_crm.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["travel_crm.utils.before_request"]
# after_request = ["travel_crm.utils.after_request"]

# Job Events
# ----------
# before_job = ["travel_crm.utils.before_job"]
# after_job = ["travel_crm.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"travel_crm.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

