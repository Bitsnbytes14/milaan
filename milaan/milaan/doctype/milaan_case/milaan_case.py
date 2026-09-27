# Copyright (c) 2026, Mohammad Ahmad and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime


class MilaanCase(Document):
	def validate(self):
		if self.status == "Resolved":
			if not self.resolution_notes:
				frappe.throw("Add resolution notes before resolving this case.")
			if not self.resolved_on:
				self.resolved_on = now_datetime()
		else:
			self.resolved_on = None
