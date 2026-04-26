# Financial Market Data Platform - Architecture

## Overview

This document describes the planned architecture for the financial data pipeline in simple terms.

## Data Flow

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   External  │───▶│   Extract   │───▶│    Raw      │───▶│   Quality   │
│      API    │    │    Module   │    │   Storage   │    │    Checks   │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                                                              │
                                                              ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Analytics │◀───│  Transform  │◀───│     SQL     │◀───│    Load     │
│    Tables   │    │   Module    │    │   Server    │    │   Module    │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

## Pipeline Stages

### 1. API (External Data Source)
- Connects to a financial data provider (e.g., Alpha Vantage, Yahoo Finance)
- Fetches historical stock data: Open, High, Low, Close, Volume (OHLCV)
- Returns data in JSON format

### 2. Extract Module
- Python code that calls the external API
- Handles API authentication and rate limits
- Converts JSON response to pandas DataFrame

### 3. Raw Storage
- Saves extracted data as CSV files in `data/raw/` folder
- Preserves original data before any transformations
- Allows reprocessing from raw data if needed

### 4. Quality Checks
- Validates data completeness (no missing values)
- Checks data types (dates, numbers)
- Verifies price relationships (High >= Low)
- Removes duplicate records

### 5. Microsoft SQL Server
- Stores cleaned data in relational database
- Uses SQLAlchemy + pyodbc for connection
- Tables: market_data, daily_returns, price_statistics

### 6. Transform Module
- Calculates financial analytics:
  - Daily returns (percentage change)
  - Volatility (standard deviation of returns)
  - Average, min, max close prices
  - Latest available price

### 7. Analytics Tables
- Final output tables with computed metrics
- Ready for reporting and visualization

## Component Responsibilities

| Component | Purpose |
|-----------|---------|
| `config.py` | Store settings (DB connection, API keys) |
| `extract.py` | Fetch data from external API |
| `quality.py` | Validate data before loading |
| `load.py` | Insert data into SQL Server |
| `transform.py` | Calculate analytics |
| `main.py` | Orchestrate the pipeline |

## Database Schema

### market_data
- Stores raw OHLCV data
- Primary key: (symbol, date)

### daily_returns
- Stores calculated daily returns
- Used for volatility calculations

### price_statistics
- Stores aggregated statistics per symbol
- Updated periodically

## Future Enhancements

- **Airflow**: Orchestrate pipeline scheduling
- **dbt**: Transform data in the warehouse
- **Docker**: Containerize the application
- **CI/CD**: Automate testing and deployment

## Simple Analogy

Think of this pipeline like a factory:
1. **Raw materials** (API data) arrive at the dock
2. **Quality control** checks each item
3. **Approved items** go into storage
4. **Processing** creates finished products
5. **Products** are shipped to customers (analytics)

This project follows the same pattern but for financial data!