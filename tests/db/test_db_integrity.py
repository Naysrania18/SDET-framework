import sqlite3

import pytest

pytestmark = pytest.mark.db


@pytest.mark.smoke
def test_all_rows_loaded(conn, source_df):
    assert conn.execute("SELECT COUNT(*) FROM trades").fetchone()[0] == len(source_df)


def test_primary_key_rejects_duplicates(conn):
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute("INSERT INTO trades VALUES (1001,'FND-A','ACME',1,1.0,'2026-01-05')")


def test_check_constraint_rejects_non_positive_quantity(conn):
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute("INSERT INTO trades VALUES (9999,'FND-A','ACME',0,1.0,'2026-01-05')")


def test_notional_per_fund_aggregation(conn):
    """SQL GROUP BY check: the business total must equal the hand-calculated value."""
    rows = dict(conn.execute("SELECT fund_code, ROUND(SUM(quantity*price),2) FROM trades GROUP BY fund_code"))
    assert rows["FND-A"] == 100 * 12.50 + 250 * 8.10
    assert rows["FND-C"] == 40 * 310.20
