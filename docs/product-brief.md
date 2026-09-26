# Milaan product brief

## Problem

A supplier invoice may arrive before the receiving team records a Purchase Receipt. A Purchase Receipt may also stay uninvoiced long enough to create an old GRNI balance. Existing reports reveal these situations, but they do not give the exception a clear owner, a resolution workflow, or an audit trail.

## User promise

Milaan turns unresolved purchase-to-pay mismatches into assigned cases that teams can resolve before a supplier payment is delayed or finance reaches month end.

## First workflow

1. A Purchase Invoice is submitted.
2. Milaan checks the invoice items against linked Purchase Orders and Purchase Receipts.
3. If a required receipt is missing or a configured variance is found, it creates a Milaan Case.
4. The case is assigned according to its cause: receiving, purchasing, or accounts payable.
5. The assignee links the missing document or records an approved resolution.
6. Milaan retains the evidence and resolution timeline.

## Non-goals for v1

- Replacing ERPNext's accounting and stock valuation logic.
- Automatically changing or submitting ERPNext financial documents.
- OCR or AI invoice extraction.
- Carrier, bank, or third-party integrations.
