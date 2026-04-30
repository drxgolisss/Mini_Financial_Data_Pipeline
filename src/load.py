"""
Data loading module for Microsoft SQL Server.
"""

import pandas as pd
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import Engine

from src.config import build_sqlserver_connection_string


def get_db_connection() -> Engine:
    """
    Create a SQLAlchemy engine for Microsoft SQL Server.

    Returns:
        SQLAlchemy database engine
    """
    connection_string = build_sqlserver_connection_string()
    engine = create_engine(connection_string)

    return engine


def test_db_connection() -> bool:
    """
    Check whether the SQL Server connection works.

    Returns:
        True if connection succeeds, False otherwise
    """
    try:
        engine = get_db_connection()

        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return True
    except Exception as error:
        print(f"Database connection failed: {error}")
        print("Check that SQL Server is running and the ODBC driver is installed.")
        return False


def load_to_sqlserver(df: pd.DataFrame, table_name: str) -> None:
    """
    Load DataFrame to SQL Server table.

    Args:
        df: DataFrame to load
        table_name: Target table name
    """
    engine = get_db_connection()

    inspector = inspect(engine)
    if not inspector.has_table(table_name, schema="dbo"):
        raise ValueError(
            f"Table dbo.{table_name} does not exist. "
            "Run sql/create_tables.sql before loading data."
        )

    df.to_sql(
        name=table_name,
        con=engine,
        schema="dbo",
        if_exists="append",
        index=False,
    )


if __name__ == "__main__":
    if test_db_connection():
        print("Database connection successful")
