TAX_RATE_BP = 725  # 7.25%, in basis points


def line_total(line):
    """Price in cents times quantity, less any discount."""
    gross = line["price_cents"] * line["qty"]
    return gross - line.get("discount_cents", 0)


def line_tax(line):
    if line.get("tax_exempt"):
        return 0
    return (line_total(line) * TAX_RATE_BP + 5000) // 10000


def invoice_totals(invoice):
    subtotal = sum(line_total(l) for l in invoice["lines"])
    tax = sum(line_tax(l) for l in invoice["lines"])
    return {"subtotal": subtotal, "tax": tax, "total": subtotal + tax}
