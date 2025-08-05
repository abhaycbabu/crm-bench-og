// frappe.ui.form.on('Travel Package', {
//   setup(frm) {
//     // Set vendor filter for hotel
//     frm.set_query('hotel', () => ({
//       filters: {
//         vendor_type: 'Hotel',
//         destination: frm.doc.destination
//       }
//     }));

//     // Set vendor filter for cab
//     frm.set_query('cab', () => ({
//       filters: {
//         vendor_type: 'Cab',
//         destination: frm.doc.destination
//       }
//     }));

//     // Set vendor filter for activities table
//     frm.fields_dict.activities.grid.get_field('activity').get_query = function(doc) {
//       return {
//         filters: {
//           vendor_type: 'Activities',
//           destination: doc.destination
//         }
//       };
//     };
//   },

//   // Recalculate total when saving
//   validate: function(frm) {
//     update_package_total(frm);
//   }
// });

// frappe.ui.form.on('Travel Package Item', {
//   // When service_type is selected, restrict vendor list
//   service_type: function(frm, cdt, cdn) {
//     const row = locals[cdt][cdn];
//     frappe.meta.get_docfield("Travel Package Item", "vendor", frm.doc.name).get_query = function() {
//       return {
//         filters: {
//           service_type: row.service_type,
//           destination: frm.doc.destination
//         }
//       };
//     };
//   },

//   // When vendor is selected, fetch its base_price_per_person
//   vendor: function(frm, cdt, cdn) {
//     const row = locals[cdt][cdn];
//     if (row.vendor) {
//       frappe.call({
//         method: 'frappe.client.get_value',
//         args: {
//           doctype: 'Destination Vendor',
//           filters: { name: row.vendor },
//           fieldname: 'base_price'
//         },
//         callback: function(r) {
//           if (r.message) {
//             frappe.model.set_value(cdt, cdn, 'rate_per_person', r.message.base_price_per_person);
//             update_package_total(frm);
//           }
//         }
//       });
//     }
//   },

//   // Trigger recalc on rate change
//   rate_per_person: function(frm) {
//     update_package_total(frm);
//   },

//   // Trigger recalc on item removal
//   package_items_remove: function(frm) {
//     update_package_total(frm);
//   }
// });

// // Helper to update base_price_per_person in Travel Package
// function update_package_total(frm) {
//   let total = 0;
//   (frm.doc.package_items || []).forEach(item => {
//     total += flt(item.rate_per_person || 0);
//   });
//   frm.set_value('base_price_per_person', total);
// }
