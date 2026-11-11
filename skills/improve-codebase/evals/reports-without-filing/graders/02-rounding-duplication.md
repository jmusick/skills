---
type: llm
focus: trace
weight: 1
---

The report has a finding that the tax rounding is written out separately in invoices/totals.py, invoices/format.py, and invoices/refunds.py, citing path:line for at least two of them. Full credit only if it also notices that refunds.py rounds differently (4999 instead of 5000).
