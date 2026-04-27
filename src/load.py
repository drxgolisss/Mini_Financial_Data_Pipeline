"""
Data loading module for Microsoft SQL Server.

TODO: Create SQLAlchemy engine
TODO: Implement table creation
TODO: Add bulk insert functionality
TODO: Handle connection errors
"""
from os import getenv

import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv


def get_db_connection(connection_string: str):
    """
    Create database connection.
    
    Args:
        connection_string: SQLAlchemy connection string
    
    Returns:
        Database engine
    """
    # TODO: Create and return engine
    load_dotenv()
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    server = os.getenv("DB_SERVER")
    port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    driver = os.getenv("DB_DRIVER").replace(" ", "+")  # Для URL пробелы заменяем на +

    # Собираем строку подключения для SQL Server (через pyodbc)
    # Формат: mssql+pyodbc://user:pass@server:port/db?driver=...
    connection_string = (
        f"mssql+pyodbc://{user}:{password}@{server}:{port}/{db_name}?"
        f"driver={driver}&TrustServerCertificate=yes"
    )

    engine = create_engine(connection_string)
    return engine



def load_to_sqlserver(df: pd.DataFrame, table_name: str, connection_string: str):
    """
    Load DataFrame to SQL Server table.
    
    Args:
        df: DataFrame to load
        table_name: Target table name
        connection_string: Database connection string
    """
    # TODO: Implement bulk insert
    pass


def create_table_if_not_exists(engine, table_schema: dict):
    """
    Create table if it doesn't exist.
    
    Args:
        engine: SQLAlchemy engine
        table_schema: Dictionary with table definition
    """
    # TODO: Implement table creation
    pass