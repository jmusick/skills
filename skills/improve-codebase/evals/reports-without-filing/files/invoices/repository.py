import json
import os


class InvoiceRepository:
    """Reads and writes invoices in one JSON file. See docs/adr/0001-json-file-store.md."""

    def __init__(self, path):
        self.path = path

    def _load(self):
        if not os.path.exists(self.path):
            return {}
        with open(self.path, encoding="utf-8") as f:
            return json.load(f)

    def _save(self, data):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def get(self, invoice_id):
        return self._load().get(invoice_id)

    def all(self):
        return list(self._load().values())

    def put(self, invoice):
        data = self._load()
        data[invoice["id"]] = invoice
        self._save(data)

    def delete(self, invoice_id):
        data = self._load()
        data.pop(invoice_id, None)
        self._save(data)
