# SDET Test Automation Framework (Python)

One framework testing four layers — **API, UI, Database, ETL** — plus BDD, CI/CD and an AI-assisted test-design workflow.

## Run
```bash
python -m venv .venv && .venv/Scripts/activate   # source .venv/bin/activate on Linux/Mac
pip install -r requirements.txt && playwright install chromium
pytest -m smoke -n auto     # fast gate
pytest -n auto              # everything, parallel; report in reports/report.html
pytest -m etl               # one layer
```

## Layers
| Layer | Tooling | Where |
|---|---|---|
| API | pytest + requests (`ApiClient`), parametrized, negative + schema + latency checks | `tests/api`, `src/api_client.py` |
| UI | Playwright + Page Object Model | `tests/ui`, `pages/` |
| Database | SQL constraints, PK/CHECK, aggregations (SQLite; same SQL for Postgres/Oracle) | `tests/db` |
| ETL | pandas source→target checks: count, schema, nulls, duplicates, checksum, row-level diff; defect-detection tests | `tests/etl`, `src/etl_checks.py` |
| BDD | pytest-bdd, Gherkin | `features/`, `tests/bdd` |
| CI/CD | GitHub Actions (smoke gate → regression → report artifact), Jenkinsfile | `.github/workflows`, `Jenkinsfile` |
| AI workflow | `CLAUDE.md` orchestrator + sub-agent + skill file, human approval gate | `CLAUDE.md`, `.claude/`, `skills/` |
| Defects / Agile | Test-case CSV, bug template, traceability | `docs/` |

## Traceability
| Requirement | Test cases | Automated in |
|---|---|---|
| REQ-1 Login | TC-01..03 | `tests/ui/test_login.py`, `features/login.feature` |
| REQ-2 Users API | TC-04..05 | `tests/api/test_users_api.py` |
| REQ-3 Trade load | TC-06..07 | `tests/etl`, `tests/db` |

## Design decisions
- Markers let CI run a fast smoke gate before the long suite.
- Page Objects / API client isolate change: one fix, not many.
- ETL checks are plain functions returning problems, reused across datasets.
- Public demo targets (JSONPlaceholder, SauceDemo) keep it runnable by anyone.
