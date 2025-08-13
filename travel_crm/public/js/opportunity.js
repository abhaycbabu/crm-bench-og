frappe.ui.form.on('Opportunity', {
    refresh: function(frm) {
        console.log("✅ Opportunity JS loaded");

        // Run logic if loaded from Lead and party_name is set
        if (frm.doc.opportunity_from === "Lead" && frm.doc.party_name) {
            frappe.db.get_value('Lead', frm.doc.party_name, 'custom_preferred_destination')
                .then(r => {
                    if (r.message && r.message.custom_preferred_destination) {
                        frm.set_value('custom_destination', r.message.custom_preferred_destination);
                    } else {
                        frm.set_value('custom_destination', '');
                    }
                });
        }
    },

    party_name: function(frm) {
        console.log("party_name event triggered");

        if (frm.doc.opportunity_from === "Lead" && frm.doc.party_name) {
            frappe.db.get_value('Lead', frm.doc.party_name, 'custom_preferred_destination')
                .then(r => {
                    if (r.message && r.message.custom_preferred_destination) {
                        frm.set_value('custom_destination', r.message.custom_preferred_destination);
                    } else {
                        frm.set_value('custom_destination', '');
                    }
                });
        } else {
            frm.set_value('custom_destination', '');
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
