# Copyright (c) 2026, Mohammad Ahmad and contributors
# For license information, please see license.txt

import frappe
from frappe.tests.utils import FrappeTestCase

from milaan.api import assign_case, reopen_case, resolve_case, run_overdue_receipt_scan


class TestMilaanApi(FrappeTestCase):
	def new_case(self):
		return frappe.get_doc({"doctype": "Milaan Case", "reason": "Other"}).insert()

	def test_assign_case_updates_owner(self):
		case = self.new_case()
		assign_case(case.name, "test2@example.com")
		self.assertEqual(frappe.db.get_value("Milaan Case", case.name, "case_owner"), "test2@example.com")

	def test_resolve_case_requires_notes(self):
		case = self.new_case()
		self.assertRaises(frappe.ValidationError, resolve_case, case.name, "")

	def test_resolve_then_reopen_case(self):
		case = self.new_case()
		resolve_case(case.name, "Confirmed and closed for this test.")
		self.assertEqual(frappe.db.get_value("Milaan Case", case.name, "status"), "Resolved")
		self.assertIsNotNone(frappe.db.get_value("Milaan Case", case.name, "resolved_on"))

		reopen_case(case.name)
		self.assertEqual(frappe.db.get_value("Milaan Case", case.name, "status"), "Open")
		self.assertIsNone(frappe.db.get_value("Milaan Case", case.name, "resolved_on"))

	def test_case_actions_require_permission(self):
		case = self.new_case()
		with self.set_user("test3@example.com"):
			self.assertRaises(frappe.PermissionError, assign_case, case.name, "test3@example.com")

	def test_overdue_scan_requires_system_manager(self):
		with self.set_user("test3@example.com"):
			self.assertRaises(frappe.PermissionError, run_overdue_receipt_scan)
