from frappe.tests.utils import FrappeTestCase

from milaan.services.exception_detection import exceeds_tolerance, has_missing_receipt


class TestExceptionDetection(FrappeTestCase):
	def test_invoice_with_all_receipts_is_not_an_exception(self):
		self.assertFalse(has_missing_receipt([{"purchase_receipt": "PREC-0001"}]))

	def test_invoice_with_a_missing_receipt_is_an_exception(self):
		self.assertTrue(has_missing_receipt([{"purchase_receipt": "PREC-0001"}, {"purchase_receipt": None}]))

	def test_tolerance_allows_small_difference_and_blocks_large_difference(self):
		self.assertFalse(exceeds_tolerance(10.2, 10, 5))
		self.assertTrue(exceeds_tolerance(10.6, 10, 5))
