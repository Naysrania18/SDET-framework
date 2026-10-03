import pandas as pd
import pytest

from src import etl_checks as chk

pytestmark = pytest.mark.etl
KEY = "trade_id"


@pytest.fixture
def target_df(conn):
    return pd.read_sql("SELECT * FROM trades", conn)


@pytest.mark.smoke
def test_clean_load_passes_every_check(source_df, target_df):
    assert chk.check_row_count(source_df, target_df) == []
    assert chk.check_schema(source_df, target_df) == []
    assert chk.check_no_duplicates(target_df, KEY) == []
    assert chk.check_no_nulls(target_df, list(target_df.columns)) == []
    assert chk.check_value_checksum(source_df, target_df, "price") == []
    assert chk.check_rows_match(source_df, target_df, KEY) == []


# --- Defect detection: plant a bad row and prove the checks catch it ---
def test_checks_detect_dropped_row(source_df):
    bad = source_df.iloc[:-1]
    assert chk.check_row_count(source_df, bad)
    assert any("only in left_only" in p for p in chk.check_rows_match(source_df, bad, KEY))


def test_checks_detect_changed_value(source_df):
    bad = source_df.copy()
    bad.loc[0, "price"] = 99.99
    assert chk.check_value_checksum(source_df, bad, "price")
    assert any("price" in p for p in chk.check_rows_match(source_df, bad, KEY))


def test_checks_detect_null_and_duplicate(source_df):
    bad = pd.concat([source_df, source_df.iloc[[0]]], ignore_index=True)
    bad.loc[1, "security"] = None
    assert chk.check_no_duplicates(bad, KEY)
    assert chk.check_no_nulls(bad, ["security"])
