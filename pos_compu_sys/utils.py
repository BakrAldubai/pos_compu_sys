from erpnext.accounts.utils import get_balance_on
from frappe.utils import now,flt
import frappe

def get_balance(doc, method=None):
    doc.party_balance_before_transaction = get_balance_on(
        account=doc.debit_to,
        date=doc.posting_date,
        party_type="Customer",
        party=doc.customer,
        company=doc.company
    )
    doc.party_balance_after_transaction = doc.party_balance_before_transaction + doc.outstanding_amount

@frappe.whitelist()
def get_party_balance(doctype,doc,debit_to,party_type,party,company):
    document = frappe.get_doc(doctype,doc)

    party_current_balance = get_balance_on(
        account=debit_to,
        date=now(),
        party_type=party_type,
        party=party,
        company=company
    )
    if document.docstatus == 1:
        if doctype == "Sales Invoice":
            document.db_set("party_current_balnace", party_current_balance, update_modified=False)
            return
        else:
            out = 0
            for i in frappe.get_all("POS Invoice",filters={"customer": party}):
                if i.status not in ["Draft","Return","Consolidated","Cancelled"]:
                    out = out + flt(i.outstanding_amount)

            document.db_set("party_current_balnace",party_current_balance + out , update_modified=False)
        



@frappe.whitelist()
def validate_party_balance(doc, method=None):

    party_current_balance = get_balance_on(
        account=doc.debit_to,
        date=now(),
        party_type="Customer",
        party=doc.customer,
        company=doc.company
    )
    if doc.doctype == "Sales Invoice":
        doc.party_current_balnace = party_current_balance
        return
    else:
        out = 0
        for i in frappe.get_all("POS Invoice",filters={"customer":doc.customer}):
            if i.status not in ["Draft","Return","Consolidated","Cancelled"]:
                out = out + flt(i.outstanding_amount)

        doc.party_current_balnace = party_current_balance + out