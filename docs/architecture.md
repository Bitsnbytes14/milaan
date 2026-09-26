# Architecture

## Application boundary

Milaan extends ERPNext; it does not replace its buying, stock, or accounting logic. It reads the Purchase Order, Purchase Receipt, and Purchase Invoice documents that ERPNext already owns and creates a separate case whenever configured matching rules find an exception.

## Initial DocTypes

### Milaan Settings

Single settings record for the first release.

- Days before an uninvoiced Purchase Receipt becomes a case.
- Default users or roles responsible for receiving, purchasing, and accounts payable exceptions.
- Thresholds that determine case severity.

### Milaan Case

The central, auditable record for one unresolved purchase-to-pay exception.

- `case_type`: missing receipt, old uninvoiced receipt, quantity variance, or price variance.
- `status`: open, awaiting action, resolved, or dismissed.
- `severity`: low, medium, high, or critical.
- Links to the relevant Purchase Order, Purchase Receipt, and Purchase Invoice.
- `assigned_to`, `resolution_note`, `resolved_by`, and `resolved_on`.
- A plain-language `summary` that says what needs attention.

## Detection design

Each detection rule will live in a dedicated Python module and return normalized case data. A shared service will create or update a Milaan Case idempotently, preventing duplicate cases when a document is saved again or a scheduled scan runs.

The initial triggers will be:

1. A Purchase Invoice is submitted without the required matching receipt.
2. A Purchase Receipt remains uninvoiced beyond the configured age threshold.

## Safety boundaries

- Detection may create or update Milaan records only.
- It must not submit, cancel, amend, repost, or mutate ERPNext financial or stock documents.
- Every future whitelisted method must verify the caller's permissions.
- Background scans must be safe to run repeatedly.
