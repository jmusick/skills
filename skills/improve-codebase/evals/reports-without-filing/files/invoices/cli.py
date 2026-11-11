import sys

from .format import format_invoice
from .store import InvoiceStore
from .totals import invoice_totals


def main(argv):
    command, path = argv[1], argv[2]
    store = InvoiceStore(path)
    for invoice in store.all():
        if command == "totals":
            print(invoice["id"], invoice_totals(invoice))
        else:
            print(format_invoice(invoice))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))
    except Exception as e:  # Top level of a nightly cron job: log and exit 1 so cron reports the failure.
        print(f"invoices: {e}", file=sys.stderr)
        sys.exit(1)
