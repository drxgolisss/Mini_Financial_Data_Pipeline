"""
Configuration module for the financial data pipeline.

TODO: Implement configuration loading from .env file
TODO: Add database connection settings
TODO: Add API configuration parameters
"""

# Database configuration
DB_CONFIG = {
    'server': 'localhost',
    'port': 1433,
    'database': 'financial_data',
    'username': 'sa',
    'password': '',
    'driver': 'ODBC Driver 18 for SQL Server',
    'trust_certificate': True
}

# API configuration
API_CONFIG = {
    'base_url': '',  # TODO: Add financial API base URL
    'api_key': '',   # TODO: Add API key
    'timeout': 30
}

# Data paths
DATA_PATHS = {
    'raw': 'data/raw',
    'processed': 'data/processed'
}