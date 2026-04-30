"""
Configuration module for the financial data pipeline.
"""

from os import getenv
from urllib.parse import quote_plus

from dotenv import load_dotenv


def get_database_config() -> dict:
    """
    Load Microsoft SQL Server settings from environment variables.
    """
    load_dotenv()

    return {
        "server": getenv("DB_SERVER", "localhost"),
        "port": getenv("DB_PORT", "1433"),
        "database": getenv("DB_NAME", "financial_data"),
        "username": getenv("DB_USER", ""),
        "password": getenv("DB_PASSWORD", ""),
        "driver": getenv("DB_DRIVER", "ODBC Driver 18 for SQL Server"),
        "trust_server_certificate": getenv("DB_TRUST_SERVER_CERTIFICATE", "yes"),
    }


def build_sqlserver_connection_string() -> str:
    """
    Build a SQLAlchemy connection string for Microsoft SQL Server.
    """
    db_config = get_database_config()
    driver = quote_plus(db_config["driver"])
    username = quote_plus(db_config["username"])
    password = quote_plus(db_config["password"])

    return (
        f"mssql+pyodbc://{username}:{password}"
        f"@{db_config['server']}:{db_config['port']}/{db_config['database']}"
        f"?driver={driver}"
        f"&TrustServerCertificate={db_config['trust_server_certificate']}"
    )


DATA_PATHS = {
    "raw": "data/raw",
    "processed": "data/processed",
}
