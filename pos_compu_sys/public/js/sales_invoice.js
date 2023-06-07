frappe.ui.form.on('Sales Invoice',{
    refresh(frm){
        if (!frm.doc.__islocal) {
			frappe.call({
				"method": "pos_compu_sys.utils.get_party_balance",
				"args": {
					"doctype": "Sales Invoice",
					"doc": frm.doc.name,
					"debit_to": frm.doc.debit_to,
					"party_type": "Customer",
					"party": frm.doc.customer,
					"company": frm.doc.company
				}
			})
			
		}
		
    }
	



})