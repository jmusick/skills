import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from invoices.totals import invoice_totals  # noqa: E402


class Totals(unittest.TestCase):
    def test_tax_rounds_half_up_per_line(self):
        invoice = {"lines": [{"price_cents": 1000, "qty": 1}, {"price_cents": 200, "qty": 3, "discount_cents": 100}]}
        self.assertEqual(invoice_totals(invoice), {"subtotal": 1500, "tax": 109, "total": 1609})

    def test_exempt_lines_have_no_tax(self):
        invoice = {"lines": [{"price_cents": 1000, "qty": 2, "tax_exempt": True}]}
        self.assertEqual(invoice_totals(invoice)["tax"], 0)


if __name__ == "__main__":
    unittest.main()
