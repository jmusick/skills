from .repository import InvoiceRepository


class InvoiceStore:
    """The interface the rest of the app uses for invoices."""

    def __init__(self, path):
        self.repo = InvoiceRepository(path)

    def get(self, invoice_id):
        return self.repo.get(invoice_id)

    def all(self):
        return self.repo.all()

    def put(self, invoice):
        return self.repo.put(invoice)

    def delete(self, invoice_id):
        return self.repo.delete(invoice_id)
