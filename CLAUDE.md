# QA workflow (orchestrator)
For a requirement or Jira ticket I give you:
1. Delegate to the `test-cases-expert` sub-agent. It follows `skills/test-case-standards.md` and writes `docs/test_cases.csv`.
2. STOP and wait for my approval ("LGTM"/"approved"). Never move on by yourself.
3. After approval, automate the approved cases in `tests/` using existing page objects/clients, run `pytest`, and show results.
Rules: never invent requirements; ask when something is ambiguous; keep tests independent and parametrized.
