"""Reusable source-to-target validation checks. Each returns a list of problems ([] = pass)."""
import pandas as pd


def check_row_count(src: pd.DataFrame, tgt: pd.DataFrame):
    return [] if len(src) == len(tgt) else [f"row count: source={len(src)} target={len(tgt)}"]


def check_schema(src: pd.DataFrame, tgt: pd.DataFrame):
    return [] if list(src.columns) == list(tgt.columns) else [f"columns differ: {list(src.columns)} vs {list(tgt.columns)}"]


def check_no_nulls(df: pd.DataFrame, columns):
    return [f"nulls in {c}: {int(df[c].isna().sum())}" for c in columns if df[c].isna().any()]


def check_no_duplicates(df: pd.DataFrame, key):
    dups = int(df.duplicated(subset=key).sum())
    return [f"{dups} duplicate {key}"] if dups else []


def check_value_checksum(src: pd.DataFrame, tgt: pd.DataFrame, column):
    s, t = round(float(src[column].sum()), 2), round(float(tgt[column].sum()), 2)
    return [] if s == t else [f"sum({column}) source={s} target={t}"]


def check_rows_match(src: pd.DataFrame, tgt: pd.DataFrame, key):
    """Row-level comparison: finds rows missing in target or with different values."""
    merged = src.merge(tgt, on=key, how="outer", suffixes=("_src", "_tgt"), indicator=True)
    problems = [f"{key}={r[key]} only in {r['_merge']}" for _, r in merged[merged["_merge"] != "both"].iterrows()]
    for col in [c for c in src.columns if c != key]:
        diff = merged[(merged["_merge"] == "both") & (merged[f"{col}_src"] != merged[f"{col}_tgt"])]
        problems += [f"{key}={r[key]} {col}: {r[f'{col}_src']} != {r[f'{col}_tgt']}" for _, r in diff.iterrows()]
    return problems
