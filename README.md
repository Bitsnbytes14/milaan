# Milaan

Milaan is a Frappe app for resolving purchasing exceptions before they become payment delays or month-end issues.

It will identify mismatches between Purchase Orders, Purchase Receipts, and Purchase Invoices, then create an owned, auditable exception for the appropriate team.

## Initial release

- Detect a Purchase Invoice submitted without a matching Purchase Receipt.
- Detect a Purchase Receipt that remains uninvoiced after a configurable number of days.
- Create a Milaan Case with the linked documents, owner, reason, severity, and resolution history.
- Provide a desk workspace for Accounts Payable, Purchasing, and Receiving teams.

## Local development

Milaan targets Frappe and ERPNext v16. Start the local Frappe development environment from
`D:\frappe\frappe_docker`, then open the `milaan.localhost` site in the bench container.

The initial application exposes the `Milaan Case` DocType. It records the exception, the
related ERPNext documents, its owner, severity, and resolution notes.

## Product principle

The first version is deterministic. It will use ERPNext document data and configurable rules rather than an LLM.
