from .totals import TAX_RATE_BP, line_total


def refund_amount(invoice, line_ids):
    """What to refund, tax included, for the given lines."""
    refund = 0
    for line in invoice["lines"]:
        if line["id"] not in line_ids:
            continue
        amount = line_total(line)
        refund += amount
        if not line.get("tax_exempt"):
            refund += (amount * TAX_RATE_BP + 4999) // 10000
    return refund
