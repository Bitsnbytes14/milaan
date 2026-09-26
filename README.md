# Milaan

Milaan is a Frappe app for resolving purchasing exceptions before they become payment delays or month-end issues.

It will identify mismatches between Purchase Orders, Purchase Receipts, and Purchase Invoices, then create an owned, auditable exception for the appropriate team.

## Initial release

- Detect a Purchase Invoice submitted without a matching Purchase Receipt.
- Detect a Purchase Receipt that remains uninvoiced after a configurable number of days.
- Create a Milaan Case with the linked documents, owner, reason, severity, and resolution history.
- Provide a desk workspace for Accounts Payable, Purchasing, and Receiving teams.

## Local development

This repository will be scaffolded as a Frappe app once the local Docker-based development environment is ready. The app will target Frappe and ERPNext v16.

## Product principle

The first version is deterministic. It will use ERPNext document data and configurable rules rather than an LLM.
