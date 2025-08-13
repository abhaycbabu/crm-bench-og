frappe.ui.form.on('Travel Booking', {

  onload(frm) {
    // Set ops user filter
    frm.set_query('assigned_ops_person', function () {
      return {
        query: 'travel_crm.travel_crm.doctype.travel_booking.travel_booking.get_ops_team_users'
      };
    });
  },
  customer: function (frm) {
    if (frm.doc.customer) {
      frappe.db.get_value('Customer', frm.doc.customer,
        ['custom_group_size', 'custom_visa_type']) // ✅ fetch both fields
        .then(r => {
          if (r.message) {
            if (r.message.custom_group_size) {
              frm.set_value('person_count', r.message.custom_group_size);
            }
            if (r.message.custom_visa_type) {
              frm.set_value('visa_type', r.message.custom_visa_type);
            }
          }
        });
    }
  },

  refresh(frm) {

    frm.set_df_property('status', 'read_only', frm.doc.status === 'Completed');

    // Sales team button
    if (frappe.user.has_role("Sales Team") && !frm.is_new()) {
      frm.add_custom_button("Send Hotel/Cab Options", function () {
        frappe.call({
          method: "travel_crm.travel_crm.doctype.travel_booking.travel_booking.send_vendor_options",
          args: { docname: frm.doc.name },
          callback: function (r) {
            if (!r.exc) {
              frappe.msgprint("Options sent to customer successfully!");
              frappe.flags.allow_status_override = true;
              frm.set_value("status", "Pending");
              frm.save();
            }
          }
        });
      }, 'Actions');
    }

    // Ensure customer is always readonly once set
    if (frm.doc.customer) {
      frm.set_df_property("customer", "read_only", 1);
    }

    if (frappe.session.user === 'Administrator' || frappe.user.has_role("Sales Team")) {
      // Create Sales Order button
      if (!frm.doc.__islocal && frm.doc.status == "Confirmed") {
        frm.add_custom_button("Create Quotation", () => {
          frappe.call({
            method: "travel_crm.travel_crm.doctype.travel_booking.travel_booking.create_quotation_from_booking",
            args: {
              booking_name: frm.doc.name
            },
            callback(r) {
              if (r.message) {
                frappe.set_route("Form", "Quotation", r.message);
              }
            }
          });
        }, 'Create');
      }

      // Create Ops Project button
      if (!frm.doc.project && !frm.is_new()) {
        frm.add_custom_button("Create Ops Project", function () {
          frappe.call({
            method: "travel_crm.travel_crm.doctype.travel_booking.travel_booking.create_visa_project_with_tasks",
            args: { booking_name: frm.doc.name },
            callback(r) {
              if (r.message) {
                frappe.msgprint("Project Created: " + r.message);
                frm.reload_doc();
              }
            }
          });
        }, 'Create');
      }

      // Create Advance Payment button
      if (frm.doc.status === 'Confirmed') {
        frm.add_custom_button('Make Advance Payment', () => {
          const advance_percent = 30;
          const advance_amount = frm.doc.package_total * (advance_percent / 100);
          frappe.call({
            method: 'travel_crm.travel_crm.doctype.travel_booking.travel_booking.create_advance_payment',
            args: {
              customer: frm.doc.customer,
              amount: advance_amount,
              reference_booking: frm.doc.name
            },
            callback(r) {
              if (r.message) {
                frappe.set_route('Form', 'Payment Entry', r.message);
              }
            }
          });
        }, 'Actions');
      }

      // Send Feedback Link button
      if (frm.doc.status === 'Completed') {
        frm.add_custom_button('Send Feedback Link', () => {
          let base_url = window.location.origin;
          let link = `${base_url}/customer-feedback/new?customer=${frm.doc.customer}&travel_booking=${frm.doc.name}`;
          frappe.msgprint(__('Feedback Link: <br><a href="{0}" target="_blank">{0}</a>', [link]));
        }, 'Actions');

        // Fetch submitted feedback (if any)
        frappe.call({
          method: "frappe.client.get_list",
          args: {
            doctype: "Customer Feedback",
            filters: {
              travel_booking: frm.doc.name
            },
            fields: ["name", "customer", "feedback", "creation"]
          },
          callback: function (r) {
            if (r.message && r.message.length) {
              let feedback = r.message[0];
              frm.dashboard.add_comment(__('Feedback received from {0} on {1}: {2}', [
                feedback.customer,
                frappe.datetime.str_to_user(feedback.creation),
                feedback.feedback || "No comments"
              ]));
            }
          }
        });
      }
    }
  },

  //setup filter for travel packgae based on destination
  setup(frm) {
    frm.set_query('package', function () {
      return {
        filters: {
          destination: frm.doc.destination
        }
      };
    });
  },
  // Clear existing package if destination changed
  destination(frm) {
    frm.set_value('package', null);
    frm.set_value('package_total', null);
    frm.set_value('hotel', null);
    frm.set_value('cab', null);
    frm.clear_table('activities', null);
    frm.refresh_field('activities', null);
    frm.set_value('check_in', null);
    frm.set_value('check_out', null);
    frm.set_value('pickup_date', null);
    frm.set_value('drop_date', null);

  },
  // Handle package selection and fetch details
  package: function (frm) {
    if (frm.doc.use_package && frm.doc.package) {
      frappe.call({
        method: 'frappe.client.get',
        args: {
          doctype: 'Travel Package',
          name: frm.doc.package
        },
        callback: function (r) {
          if (r.message) {
            const pkg = r.message;

            // Set base_price_per_person and calculate package_total
            const base_price = pkg.base_price_per_person || 0;
            frm.set_value('package_total', (frm.doc.person_count || 1) * base_price);

            // Reset values first
            frm.set_value('hotel', '');
            frm.set_value('cab', '');
            frm.clear_table('activities');

            // Process package_items
            (pkg.package_items || []).forEach(item => {
              if (item.service_type === 'Hotel') {
                frm.set_value('hotel', item.vendor);
              } else if (item.service_type === 'Cab') {
                frm.set_value('cab', item.vendor);
              } else if (item.service_type === 'Activities') {
                let row = frm.add_child('activities');
                row.activity = item.vendor;  // adjust based on fieldnames in Selected Activity
                row.description = item.description;
              }
            });

            frm.refresh_field('activities');
          }
        }
      });
    }
  },

  use_package: function (frm) {
    if (frm.doc.use_package && frm.doc.package) {
      toggle_package_fields(frm);
      frm.trigger('package');  // auto trigger logic
    }
  },

  person_count: function (frm) {
    if (frm.doc.use_package && frm.doc.package) {
      frappe.db.get_value('Travel Package', frm.doc.package, 'base_price_per_person', (r) => {
        if (r && r.base_price_per_person) {
          frm.set_value('package_total', (frm.doc.person_count || 1) * r.base_price_per_person);
        }
      });
    }
  },

  use_package(frm) {
    toggle_package_fields(frm);
  },

  // travel_package(frm) {
  //   calculate_package_total(frm);
  // },

  // person_count(frm) {
  //   calculate_package_total(frm);
  // }

});




// Function to toggle package-related fields based on use_package checkbox
function toggle_package_fields(frm) {
  const readonly = frm.doc.use_package ? 1 : 0;

  frm.set_df_property('hotel', 'read_only', readonly);
  frm.set_df_property('cab', 'read_only', readonly);

  const grid = frm.get_field('activities').grid;
  grid.update_docfield_property('activity', 'read_only', readonly);

  // Optional: loop through existing rows and apply readonly flag
  // grid.grid_rows.forEach(row => {
  //   row.toggle_editable('activity', !readonly);
  //   row.toggle_editable('price', !readonly);
  // });

  // Disable add/remove buttons
  // grid.wrapper.find('.grid-add-row, .grid-remove-rows').toggle(!readonly);
  // grid.wrapper.find('.grid-row .grid-delete-row').toggle(!readonly);
  // grid.wrapper.find('.grid-row .grid-remove-rows').toggle(!readonly);

  frm.refresh_field('activities');
}
