import pyodbc as pd
import pytest

@pytest.fixture
def connection():
    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=LAPTOP-4HC9J5AE\SQLEXPRESS;"
        "DATABASE=ETl_pipeline;"
        "Trusted_Connection=yes;"
    )
    return pd.connect(conn_str)
