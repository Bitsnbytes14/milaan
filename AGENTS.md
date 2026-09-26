# Milaan development guide

## Product

Milaan is a Frappe and ERPNext app for resolving purchase-to-pay exceptions. It identifies mismatches between Purchase Orders, Purchase Receipts, and Purchase Invoices, then gives each exception a clear owner and an auditable resolution path.

## Initial scope

- Target Frappe Framework and ERPNext v16.
- Begin with one custom DocType: `Milaan Case`.
- Detect two conditions: a submitted Purchase Invoice without a matching Purchase Receipt, and an old Purchase Receipt without a Purchase Invoice.
- Do not alter, submit, cancel, or repost ERPNext financial or stock documents automatically.
- Keep business rules deterministic and configurable; do not add LLM features to the initial release.

## Technical conventions

- Use Frappe's ORM, permissions, document lifecycle hooks, background jobs, and Desk UI patterns.
- Never use raw SQL when Frappe ORM or Query Builder can express the query.
- Check permissions in every whitelisted server method.
- Keep each detection rule independently testable.
- Store linked ERPNext document references, the reason for the case, owner, severity, and resolution notes in `Milaan Case`.
- Add tests with every server-side detection rule or lifecycle hook.

## Product conventions

- Use plain language for finance, purchasing, and warehouse users.
- A case must always answer: what is wrong, which documents are involved, who owns the next action, and how it was resolved.
- Prefer actionable queues and clear exceptions over dashboards that only report a problem.
