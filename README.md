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

## Installation

Milaan requires ERPNext v16. From a Frappe bench:

```bash
bench get-app https://github.com/Bitsnbytes14/milaan.git --branch main
bench --site your-site install-app milaan
```

## Run locally

After installing Milaan into a development bench, run the migration and start
Frappe:

```bash
cd frappe-bench
bench --site your-site migrate
bench start
```

Open `http://localhost:8000`, sign in as an Administrator, and open the
**Milaan** workspace from Desk.

For the Docker development environment used in this repository:

```powershell
cd D:\frappe\frappe_docker
docker compose -f .devcontainer/docker-compose.yml up -d
docker compose -f .devcontainer/docker-compose.yml exec -w /workspace/development/frappe-bench frappe bench --site milaan.localhost migrate
docker compose -f .devcontainer/docker-compose.yml exec -w /workspace/development/frappe-bench frappe bench start
```

The final command keeps the server running in that terminal. In a devcontainer,
port 8000 is forwarded automatically; otherwise expose port 8000 in Docker.

Create at least one **Milaan Policy** before submitting invoices. A policy can
match a supplier, company, or item group. The most specific matching policy is
used. Use the Milaan workspace to review cases and policies.

## Operations

- Submit a Purchase Invoice without a required Purchase Receipt to create an
  exception case automatically.
- Use **Run overdue receipt scan** as a System Manager when you need an
  immediate check; the same scan runs daily.
- Resolve cases with notes so the audit timeline explains the outcome.

See [the demo guide](docs/demo.md) for a complete walkthrough.

## Product principle

The first version is deterministic. It will use ERPNext document data and configurable rules rather than an LLM.
