import frappe
from frappe.utils import add_days, getdate, nowdate


def get_policy(company, supplier, items=()):
	item_codes = [item.get("item_code") for item in items if item.get("item_code")]
	item_groups = set()
	if item_codes:
		item_groups = set(frappe.get_all("Item", filters={"name": ["in", item_codes]}, pluck="item_group"))

	best_policy = None
	best_score = -1
	for policy in frappe.get_all(
		"Milaan Policy",
		filters={"enabled": 1, "receipt_required": 1},
		fields=["name", "company", "supplier", "item_group"],
	):
		if policy.supplier and policy.supplier != supplier:
			continue
		if policy.company and policy.company != company:
			continue
		if policy.item_group and policy.item_group not in item_groups:
			continue
		score = bool(policy.supplier) * 4 + bool(policy.company) * 2 + bool(policy.item_group)
		if score > best_score:
			best_policy = policy.name
			best_score = score

	return frappe.get_doc("Milaan Policy", best_policy) if best_policy else None


def has_missing_receipt(items):
	return any(not item.get("purchase_receipt") for item in items)


def create_case(values):
	filters = {"purchase_invoice": values.get("purchase_invoice"), "purchase_receipt": values.get("purchase_receipt"), "reason": values["reason"]}
	if frappe.db.exists("Milaan Case", filters):
		return None
	return frappe.get_doc({"doctype": "Milaan Case", **values}).insert(ignore_permissions=True)


def create_missing_receipt_case(doc, method=None):
	policy = get_policy(doc.company, doc.supplier, doc.items)
	if not policy:
		return None
	purchase_order = next((item.purchase_order for item in doc.items if item.purchase_order), None)
	purchase_receipt = next((item.purchase_receipt for item in doc.items if item.purchase_receipt), None)
	case = None
	if has_missing_receipt(doc.items):
		case = create_case(
		{
			"purchase_invoice": doc.name,
			"purchase_order": purchase_order,
			"supplier": doc.supplier,
			"case_owner": doc.owner,
			"severity": "High",
			"reason": "Invoice submitted without receipt",
			"blocked_amount": doc.grand_total,
			"next_action": "Confirm the goods or services were received, then create or link the Purchase Receipt.",
		}
	)
	for reason, message in find_tolerance_exceptions(doc.items, policy):
		case = create_case({"purchase_invoice": doc.name, "purchase_order": purchase_order, "purchase_receipt": purchase_receipt, "supplier": doc.supplier, "case_owner": doc.owner, "severity": "High", "reason": reason, "blocked_amount": doc.grand_total, "next_action": message}) or case
	return case


def exceeds_tolerance(actual, expected, tolerance_percent):
	if not expected:
		return False
	return actual > expected * (1 + (tolerance_percent or 0) / 100)


def find_tolerance_exceptions(items, policy):
	exceptions = []
	for item in items:
		if exceeds_tolerance(item.get("qty") or 0, item.get("received_qty") or 0, policy.quantity_tolerance_percent):
			exceptions.append(("Quantity mismatch", "Review the invoiced quantity against the quantity received."))
		if item.get("po_detail"):
			po_rate = frappe.db.get_value("Purchase Order Item", item.po_detail, "rate")
			if exceeds_tolerance(item.get("rate") or 0, po_rate or 0, policy.rate_tolerance_percent):
				exceptions.append(("Amount mismatch", "Review the invoice rate against the agreed Purchase Order rate."))
	return exceptions


def create_overdue_receipt_cases():
	policies = frappe.get_all("Milaan Policy", filters={"enabled": 1}, fields=["name", "company", "supplier", "receipt_age_days"])
	for policy in policies:
		filters = {"docstatus": 1, "company": policy.company} if policy.company else {"docstatus": 1}
		if policy.supplier:
			filters["supplier"] = policy.supplier
		for receipt in frappe.get_all("Purchase Receipt", filters=filters, fields=["name", "supplier", "company", "posting_date", "grand_total", "owner"]):
			if getdate(receipt.posting_date) > add_days(getdate(nowdate()), -policy.receipt_age_days):
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
