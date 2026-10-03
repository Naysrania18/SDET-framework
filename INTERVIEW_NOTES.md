# Interview cheat-sheet (my own words)
**30-sec pitch:** I built a layered Python framework: pytest runs API, UI, DB and ETL tests; markers and xdist keep feedback fast; CI runs a smoke gate then regression.
**Why pytest?** Fixtures (shared setup), parametrize (many cases, one function), markers (slice the suite), plugins (xdist, html).
**Why Page Object?** Locators live in one place; tests read as business steps; maintenance cost drops.
**Why Playwright?** Auto-waiting => less flakiness, fast, built-in browsers.
**ETL testing = ** completeness (counts), accuracy (values/checksum), integrity (nulls/dupes/keys), schema. Done source vs target.
**AI use:** AI drafts test cases from a requirement using my standards file; I review/approve before automation. AI assists, I own quality.
**Demo flow (2 min):** run `pytest -n auto` -> open report -> show ETL test catching a dropped row -> show CSV of AI-drafted cases.
**Be honest:** public demo apps, SQLite stands in for Oracle/Postgres; swap driver only.
