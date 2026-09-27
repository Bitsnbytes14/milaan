import frappe


def get_case(case_name):
	case = frappe.get_doc("Milaan Case", case_name)
	if not frappe.has_permission("Milaan Case", "write", case):
		frappe.throw("You do not have permission to update this case.", frappe.PermissionError)
	return case


@frappe.whitelist()
def assign_case(case_name, user):
	case = get_case(case_name)
	case.case_owner = user
	case.save()
	case.add_comment("Info", f"Case assigned to {user}.")
	return case.name


@frappe.whitelist()
def resolve_case(case_name, resolution_notes):
	case = get_case(case_name)
	case.status = "Resolved"
	case.resolution_notes = resolution_notes
	case.save()
	case.add_comment("Info", "Case resolved.")
	return case.name


@frappe.whitelist()
def reopen_case(case_name):
	case = get_case(case_name)
	case.status = "Open"
	case.save()
	case.add_comment("Info", "Case reopened.")
	return case.name
