

frappe.ui.form.on('Lead CRM', {
    validate: function (frm) {
        const group_size = frm.doc.group_size || 0;
        const budget = frm.doc.budget || 0;
        const visa = frm.doc.visa_type;
        const from = frm.doc.from_date;
        const to = frm.doc.to_date;

        if (
            group_size >= 2 &&
            budget >= 50000 &&
            visa &&
            from &&
            to
        ) {
            frm.set_value("lead_status", "Qualified");
            frappe.msgprint("Lead auto-qualified based on entered info.");
        }
    }
});

// Limit Assigned Sales Person to users with Sales Team role
frappe.ui.form.on('Lead CRM', {
    onload: function (frm) {
        frm.set_query("assigned_sales_person", function () {
            return {
                query: "travel_crm.travel_crm.doctype.lead_crm.lead_crm.get_sales_team_users"
            };
        });
    }
});

//set read-only for assigned_sales_person if not Admin or System Manager
frappe.ui.form.on('Lead CRM', {
    refresh: function(frm) {
        // If current user is not Admin and not System Manager
        if (!frappe.user.has_role('System Manager') && !frappe.user.has_role('Administrator')) {
            frm.set_df_property('assigned_sales_person', 'read_only', 1);
        }
    }
});

// frappe.ui.form.on('Lead CRM', {
//     refresh: function (frm) {
//         // Only show if status is Qualified
//         if (frm.doc.lead_status === "Qualified") {
//             frm.add_custom_button('Create Travel Booking', () => {
//                 frappe.new_doc('Travel Booking', {
//                     customer: frm.doc.name,
//                     destination: frm.doc.destination_interested,
//                 });
//             }, __('Actions'));
//         }
//     }
// });

