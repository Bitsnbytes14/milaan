import frappe
from frappe.utils import add_days, nowdate


def get_policy(company, supplier):
	filters = {"enabled": 1, "receipt_required": 1}
	if supplier:
		policy = frappe.get_all("Milaan Policy", filters={**filters, "supplier": supplier}, pluck="name", limit=1)
		if policy:
			return frappe.get_doc("Milaan Policy", policy[0])
	if company:
		policy = frappe.get_all("Milaan Policy", filters={**filters, "company": company}, pluck="name", limit=1)
		if policy:
			return frappe.get_doc("Milaan Policy", policy[0])
	return None


def has_missing_receipt(items):
	return any(not item.get("purchase_receipt") for item in items)


def create_case(values):
	filters = {"purchase_invoice": values.get("purchase_invoice"), "purchase_receipt": values.get("purchase_receipt"), "reason": values["reason"]}
	if frappe.db.exists("Milaan Case", filters):
		return None
	return frappe.get_doc({"doctype": "Milaan Case", **values}).insert(ignore_permissions=True)


def create_missing_receipt_case(doc, method=None):
	policy = get_policy(doc.company, doc.supplier)
	if not policy or not has_missing_receipt(doc.items):
		return None
	return create_case(
		{
			"purchase_invoice": doc.name,
			"purchase_order": next((item.purchase_order for item in doc.items if item.purchase_order), None),
			"supplier": doc.supplier,
			"case_owner": doc.owner,
			"severity": "High",
			"reason": "Invoice submitted without receipt",
			"blocked_amount": doc.grand_total,
			"next_action": "Confirm the goods or services were received, then create or link the Purchase Receipt.",
		}
	)


def create_overdue_receipt_cases():
	policies = frappe.get_all("Milaan Policy", filters={"enabled": 1}, fields=["name", "company", "supplier", "receipt_age_days"])
	for policy in policies:
		filters = {"docstatus": 1, "company": policy.company} if policy.company else {"docstatus": 1}
		if policy.supplier:
			filters["supplier"] = policy.supplier
		for receipt in frappe.get_all("Purchase Receipt", filters=filters, fields=["name", "supplier", "company", "posting_date", "grand_total", "owner"]):
			if receipt.posting_date > add_days(nowdate(), -policy.receipt_age_days):
				continue
			if has_submitted_invoice_for_receipt(receipt.name):
				continue
			create_case({"purchase_receipt": receipt.name, "supplier": receipt.supplier, "case_owner": receipt.owner, "severity": "Medium", "reason": "Receipt overdue for invoice", "blocked_amount": receipt.grand_total, "next_action": "Confirm whether the supplier invoice is expected, then follow up or close this case."})


def has_submitted_invoice_for_receipt(receipt_name):
	invoice_names = frappe.get_all(
		"Purchase Invoice Item",
		filters={"purchase_receipt": receipt_name},
		pluck="parent",
	)
	return bool(invoice_names and frappe.db.exists("Purchase Invoice", {"name": ["in", invoice_names], "docstatus": 1}))
