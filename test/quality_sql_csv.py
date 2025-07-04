import pandas as pd
import pyodbc as py


# Function to create SQL Server connection
def connection():
    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=LAPTOP-4HC9J5AE\\SQLEXPRESS;"  # double backslash for Windows
        "DATABASE=ETl_pipeline;"
        "Trusted_Connection=yes;"
    )
    return py.connect(conn_str)


# Function to compare rows and columns
def row_column():
    # Read data from SQL Server
    query = "SELECT * FROM SampleDataValidation"
    df_target = pd.read_sql(query, connection())

    # Read data from CSV
    df_source = pd.read_csv("../sample_data_validation.csv")

    # Reset index to make sure they align
    df_source = df_source.reset_index(drop=True)
    df_target = df_target.reset_index(drop=True)

    # Ensure same number of rows and columns
    min_rows = min(len(df_source), len(df_target))
    common_columns = set(df_source.columns) & set(df_target.columns)

    # Compare row by row, column by column
    for i in range(min_rows):
        for col in common_columns:
            val_source = str(df_source.at[i, col]).strip()
            val_target = str(df_target.at[i, col]).strip()
            if val_source != val_target:
                print(f"Row {i + 1}, Column '{col}': Mismatch → Source: {val_source} | Target: {val_target}")

    print("✅ Comparison completed.")


def date_format():
    # Load from database
    query = "SELECT * FROM SampleDataValidation"
    df_target = pd.read_sql(query, connection())

    # Load from CSV
    df_source = pd.read_csv("../sample_data_validation.csv")

    # Ensure DateOfBirth columns are datetime
    df_target["DateOfBirth"] = pd.to_datetime(df_target["DateOfBirth"], errors='coerce')
    df_source["DateOfBirth"] = pd.to_datetime(df_source["DateOfBirth"], errors='coerce')

    # Format both to string format "YYYY/MM/DD"
    target_formatted = df_target["DateOfBirth"].dt.strftime("%Y/%m/%d")
    source_formatted = df_source["DateOfBirth"].dt.strftime("%Y/%m/%d")

    # Compare row by row
    for i in range(min(len(target_formatted), len(source_formatted))):
        if target_formatted[i] != source_formatted[i]:
            print(f"Row {i+1}: Mismatch → Source: {source_formatted[i]} | Target: {target_formatted[i]}")

    print("✅ Date comparison completed.")


# Run the comparison
row_column()
date_format()
