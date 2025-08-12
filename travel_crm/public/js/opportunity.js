frappe.ui.form.on('Opportunity', {
    lead: function (frm) {
        if (frm.doc.lead) {
            frappe.call({
                method: 'travel_crm.opportunity.get_lead_destination',
                args: { lead_name: frm.doc.lead },
                callback: function (r) {
                    if (r.message && r.message.destination) {
                        frm.set_value('custom_destination', r.message.destination);
                    }
                }
            });
        }
    },

    custom_destination: function(frm) {
        frm.set_query('custom_travel_package', () => {
            return {
                filters: {
                    destination: frm.doc.custom_destination
                }
            };
        });
    }
});
