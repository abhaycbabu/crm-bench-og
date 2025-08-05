frappe.listview_settings['Lead CRM'] = {
    add_fields: ["lead_status"],  // Make sure the field is fetched

    get_indicator: function (doc) {
        if (doc.lead_status === "New") {
            return [__("New"), "blue", "lead_status,=,New"];
        } else if (doc.lead_status === "Qualified") {
            return [__("Qualified"), "green", "lead_status,=,Qualified"];
        } else if (doc.lead_status === "Converted") {
            return [__("Converted"), "purple", "lead_status,=,Converted"];
        } else if (doc.lead_status === "Lost") {
            return [__("Lost"), "red", "lead_status,=,Lost"];
        }
    }
};
// frappe.listview_settings['Lead CRM'] = {
//     onload: function(listview) {
//         const user = frappe.session.user;

//         listview.page.add_inner_button('My Qualified Leads', function() {
//             listview.filter_area.add([
//                 ["Lead CRM", "assigned_sales_person", "=", user],
//                 ["Lead CRM", "lead_status", "in", ["Qualified"]]
//             ]);
//         });
//     }
// };
