"""
Data quality validation module.

This module contains simple validation checks for financial market data.
"""

import pandas as pd


REQUIRED_COLUMNS = ["date", "symbol", "open", "high", "low", "close", "volume"]


def validate_data_quality(df: pd.DataFrame) -> dict:
    """
    Run basic data quality checks on market data.
    """
    results = {
        "row_count": len(df),
        "missing_columns": check_required_columns(df),
        "missing_values": check_missing_values(df),
        "duplicate_rows": check_duplicates(df),
        "invalid_prices": check_invalid_prices(df),
    }

    return results


def check_required_columns(df: pd.DataFrame) -> list:
    """
    Check whether all required columns exist.
    """
    missing_columns = []

    for column in REQUIRED_COLUMNS:
        if column not in df.columns:
            missing_columns.append(column)

    return missing_columns


def check_missing_values(df: pd.DataFrame) -> dict:
    """
    Count missing values in each column.
    """
    return df.isna().sum().to_dict()


def check_duplicates(df: pd.DataFrame) -> int:
    """
    Count duplicated rows by symbol and date.
    """
    return df.duplicated(subset=["symbol", "date"]).sum()


def check_invalid_prices(df: pd.DataFrame) -> int:

        """
            Count rows with invalid price values.
        """

        invalid_count = 0

        for _, row in df.iterrows():
            open_p = row["open"]
            high_p = row["high"]
            low_p = row["low"]
            close_p = row["close"]

            if open_p <= 0 or high_p <= 0 or low_p <= 0 or close_p <= 0:
                invalid_count += 1
                continue

            if not (high_p >= open_p and high_p >= close_p and high_p >= low_p):
                invalid_count += 1
                continue

            if not (low_p <= open_p and low_p <= close_p):
                invalid_count += 1

        return invalid_count