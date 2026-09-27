# Copyright (c) 2026, Mohammad Ahmad and contributors
# For license information, please see license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestMilaanCase(FrappeTestCase):
	def test_resolved_case_requires_resolution_notes(self):
		case = frappe.get_doc(
			{
				"doctype": "Milaan Case",
				"reason": "Other",
				"status": "Resolved",
			}
		)

		self.assertRaises(frappe.ValidationError, case.insert)

	def test_resolved_case_records_resolution_time(self):
		case = frappe.get_doc(
			{
				"doctype": "Milaan Case",
				"reason": "Other",
				"resolution_notes": "Confirmed the documents were entered in error.",
				"status": "Resolved",
			}
		).insert()

		self.assertIsNotNone(case.resolved_on)
