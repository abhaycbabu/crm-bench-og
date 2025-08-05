frappe.ui.form.on('Customer', {
    refresh: function(frm) {
        // Add custom button to create Travel Booking
        frm.add_custom_button(__('Book Travel Ticket'), function() {
            frappe.new_doc('Travel Booking', {
                customer: frm.doc.name,
                destination: frm.doc.custom_preferred_destination,  // Use custom field for destination
                travel_date_starting: frm.doc.custom_expected_travel_date  // Use custom field for expected travel date
            });
        }, __('Actions'));  // Optional: group under 'Actions'
    }
});
