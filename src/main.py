"""Main entry point for the financial data pipeline."""

from pathlib import Path

from src import extract
from src import quality
from src import transform
from src import load


def run_pipeline(
    symbols: list,
    start_date: str,
    end_date: str,
    load_to_database: bool = False,
):
    """
    Run the complete data pipeline.
    
    Args:
        symbols: List of stock ticker symbols
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        load_to_database: Whether to load processed data into SQL Server
    """
    raw_data = extract.extract_batch(
        symbols,
        start_date,
        end_date
    )

    print("Data quality report:\n")
    quality_report = quality.validate_data_quality(raw_data)
    quality.print_quality_report(quality_report)

    output_path = Path("data/raw/market_data.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    raw_data.to_csv(output_path, index=False)

    print(f"Saved {len(raw_data)} rows to {output_path}")

    clean_data = transform.clean_market_data(raw_data)

    cleaned_output_path = Path("data/processed/market_data.csv")
    cleaned_output_path.parent.mkdir(parents=True, exist_ok=True)
    clean_data.to_csv(cleaned_output_path, index=False)
    print(f"Saved {len(clean_data)} rows to {cleaned_output_path}")

    daily_returns_mart = transform.build_daily_returns_mart(clean_data)
    price_statistics_mart = transform.build_price_statistics_mart(
        clean_data,
        daily_returns_mart,
    )

    returns_output_path = Path("data/processed/daily_returns.csv")
    daily_returns_mart.to_csv(returns_output_path, index=False)
    print(f"Saved {len(daily_returns_mart)} rows to {returns_output_path}")

    statistics_output_path = Path("data/processed/price_statistics.csv")
    price_statistics_mart.to_csv(statistics_output_path, index=False)
    print(f"Saved {len(price_statistics_mart)} rows to {statistics_output_path}")

    if load_to_database:
        load.load_to_sqlserver(clean_data, "market_data")
        load.load_to_sqlserver(daily_returns_mart, "daily_returns")
        load.load_to_sqlserver(price_statistics_mart, "price_statistics")
        print("Loaded processed data to SQL Server")


if __name__ == '__main__':
    run_pipeline(["AAPL", "MSFT", "T", "BAC", "BLK"], '2023-01-01', '2024-01-01', True)
