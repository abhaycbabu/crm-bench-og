frappe.ui.form.on('Lead', {
  before_save: function (frm) {
    const budget = frm.doc.custom_budget_range || 0;
    const group = frm.doc.custom_group_size|| 1;
        console.log('Auto-evaluating status', { budget, group });


    if (budget > 20000 && group >= 2 && frm.doc.custom_expected_travel_date && frm.doc.custom_preferred_destination) {
      frm.set_value('status', 'Converted');
      console.log('Auto-evaluating status', { budget, group });
    }
  }
});
