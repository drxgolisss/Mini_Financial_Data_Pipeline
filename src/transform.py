"""
Data transformation and analytics module.
"""

import pandas as pd

from src.quality import REQUIRED_COLUMNS


def clean_market_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean raw market data and prepare it for analytics.
    """
    df = df.copy()

    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["symbol"] = df["symbol"].astype(str).str.upper().str.strip()

    price_columns = ["open", "high", "low", "close"]
    for column in price_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df["volume"] = pd.to_numeric(df["volume"], errors="coerce")

    df = df.dropna(subset=REQUIRED_COLUMNS)
    df = df.drop_duplicates(subset=["symbol", "date"])
    df = df.sort_values(["symbol", "date"])

    df["volume"] = df["volume"].astype("int64")

    return df


def calculate_daily_returns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate daily percentage returns.
    
    Args:
        df: DataFrame with close prices
    
    Returns:
        DataFrame with daily_return column
    """
    df = df.copy()
    df = df.sort_values(["symbol", "date"])

    df["previous_close"] = df.groupby("symbol")["close"].shift(1)
    df["daily_return"] = (df["close"] - df["previous_close"]) / df["previous_close"]

    return df


def calculate_volatility(df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
    """
    Calculate rolling volatility.
    
    Args:
        df: DataFrame with returns
        window: Rolling window size
    
    Returns:
        DataFrame with volatility column
    """
    df = df.copy()
    df = df.sort_values(["symbol", "date"])

    if "daily_return" not in df.columns:
        df = calculate_daily_returns(df)

    df["volatility"] = (
        df.groupby("symbol")["daily_return"]
        .rolling(window=window)
        .std()
        .reset_index(level=0, drop=True)
    )

    return df


def calculate_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate basic statistics (min, max, avg close price).
    
    Args:
        df: DataFrame with market data
    
    Returns:
        DataFrame with statistics
    """
    df = df.copy()
    df = df.sort_values(["symbol", "date"])

    price_statistics = (
        df.groupby("symbol")
        .agg(
            avg_close=("close", "mean"),
            min_close=("close", "min"),
            max_close=("close", "max"),
            total_volume=("volume", "sum"),
        )
        .reset_index()
    )

    df_sorted = df.sort_values(["symbol", "date"])

    latest_rows = df_sorted.groupby("symbol").tail(1)

    latest_prices = latest_rows[["symbol", "date", "close"]]

    latest_prices = latest_prices.rename(columns={
        "date": "latest_date",
        "close": "latest_close"
    })

    statistics = price_statistics.merge(
        latest_prices,
        on="symbol",
        how="left"
    )

    return statistics[
        [
            "symbol",
            "latest_date",
            "latest_close",
            "avg_close",
            "min_close",
            "max_close",
            "total_volume",
        ]
    ]


def get_latest_price(df: pd.DataFrame) -> dict:
    """
    Get the latest available price for each symbol.
    
    Args:
        df: DataFrame with market data
    
    Returns:
        Dictionary with latest prices
    """
    latest_rows = df.sort_values(["symbol", "date"]).groupby("symbol").tail(1)
    latest_prices = {}

    for _, row in latest_rows.iterrows():
        latest_prices[row["symbol"]] = {
            "latest_date": row["date"],
            "latest_close": row["close"],
        }

    return latest_prices
