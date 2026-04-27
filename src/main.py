"""Main entry point for the financial data pipeline."""

from pathlib import Path

from src import extract
from src import quality
from src import transform


def run_pipeline(symbols: list, start_date: str, end_date: str):
    """
    Run the complete data pipeline.
    
    Args:
        symbols: List of stock ticker symbols
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
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


if __name__ == '__main__':
    run_pipeline(["AAPL", "MSFT"], '2023-01-01', '2024-01-01')
