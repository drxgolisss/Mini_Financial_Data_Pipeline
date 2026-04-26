# Financial Market Data Platform

A data engineering project for extracting, validating, and analyzing financial market data.

## Description

This project builds a data pipeline to:
1. Extract historical financial market data from an external API
2. Save raw data locally
3. Validate data quality
4. Load cleaned data into Microsoft SQL Server
5. Calculate financial analytics (daily returns, volatility, average close price, min/max price, latest price)

## Pipeline Flow

```
API → Extract → Raw Storage → Quality Checks → Microsoft SQL Server → Analytics Tables
```

## Tech Stack

- **Language**: Python
- **Data Processing**: pandas
- **API Calls**: requests
- **Database**: Microsoft SQL Server
- **ORM**: SQLAlchemy
- **DB Driver**: pyodbc
- **Environment**: python-dotenv

## Current Status

**Project skeleton created** - Basic structure and placeholder files ready.

## Future Roadmap

### Stage 1: Extract data
- Connect to financial API (e.g., Alpha Vantage, Yahoo Finance)
- Fetch historical market data (OHLCV data)

### Stage 2: Save raw data
- Store raw API responses as CSV files
- Implement basic file organization

### Stage 3: Add data quality checks
- Validate data completeness
- Check for missing values
- Verify data types and ranges

### Stage 4: Load to Microsoft SQL Server
- Set up SQLAlchemy connection
- Create target tables
- Implement bulk insert logic

### Stage 5: Add transformations and analytics
- Calculate daily returns
- Compute volatility
- Generate min/max/avg statistics

### Stage 6: Optional Airflow/dbt integration
- Orchestrate pipeline with Apache Airflow
- Add dbt for transformations