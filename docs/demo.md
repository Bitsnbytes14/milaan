# Milaan demo

1. Create a **Milaan Policy** for a company, supplier, or item group and leave
   **Require a Purchase Receipt before payment** enabled.
2. Create and submit a Purchase Invoice for a matching supplier or item group
   without a Purchase Receipt on at least one line.
3. Open **Milaan Case**. Milaan creates one high-severity case, links the
   invoice and Purchase Order, records the amount waiting for resolution, and
   explains the next action.
4. Add the missing receipt or otherwise resolve the issue. Add resolution notes
   and set the case status to **Resolved**. Milaan records the resolution time.

For the daily receipt check, create a submitted Purchase Receipt that has no
submitted Purchase Invoice and is older than the policy's age threshold. Run the
scheduled task or wait for the daily scheduler. Milaan creates an overdue case.
