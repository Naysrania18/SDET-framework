import sqlite3
from pathlib import Path

import pandas as pd
import pytest

DATA = Path(__file__).resolve().parents[2] / "data" / "source_trades.csv"


@pytest.fixture
def source_df():
    return pd.read_csv(DATA)


@pytest.fixture
def conn(source_df, tmp_path):
    """The 'ETL load': CSV -> SQLite with constraints, like a target warehouse table."""
    c = sqlite3.connect(tmp_path / "target.db")
    c.execute("""CREATE TABLE trades (
        trade_id INTEGER PRIMARY KEY, fund_code TEXT NOT NULL, security TEXT NOT NULL,
        quantity INTEGER NOT NULL CHECK (quantity > 0), price REAL NOT NULL, trade_date TEXT NOT NULL)""")
    source_df.to_sql("trades", c, if_exists="append", index=False)
    yield c
    c.close()
