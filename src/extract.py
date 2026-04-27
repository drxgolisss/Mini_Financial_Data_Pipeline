"""Data extraction module."""

import pandas as pd
import yfinance as yf


def extract_market_data(symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Extract market data for a given symbol and date range.
    
    Args:
        symbol: Stock ticker symbol (e.g., 'AAPL', 'MSFT')
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
    
    Returns:
        DataFrame with columns: date, open, high, low, close, volume
    """

    data = yf.download(
        symbol,
        start=start_date,
        end=end_date,
        progress=False,
        auto_adjust=False,
    )

    if data.empty:
        raise ValueError(f"data of the company {symbol} is empty")

    data = data.reset_index()

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    data = data.rename(
        columns={
            "Date": "date",
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume",
        }
    )

    data["symbol"] = symbol
    return data[["symbol", "date", "open", "high", "low", "close", "volume"]]


def extract_batch(symbols: list, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Extract data for multiple symbols.
    
    Args:
        symbols: List of stock ticker symbols
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
    
    Returns:
        Combined DataFrame with all symbols
    """
    batches = []
    for symbol in symbols:
        batches.append(extract_market_data(symbol, start_date, end_date))

    return pd.concat(batches, ignore_index=True)
