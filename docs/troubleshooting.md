# Troubleshooting

## No case was created for an invoice

Check that a matching Milaan Policy is enabled and requires a Purchase Receipt.
Supplier rules take precedence over company and item-group rules. Milaan does
not flag invoices when no enabled policy applies.

## The overdue scan did not create a case

The Purchase Receipt must be submitted, older than the policy threshold, and
must not have a submitted Purchase Invoice linked to it.

## A duplicate case exists

Milaan prevents duplicates for the same linked invoice or receipt and reason.
Resolve or reopen the existing case instead of creating a second one.
