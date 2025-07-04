import pandas as pd
import pytest


#Test Case 1: Whitespace is trimmed from string columns

def whitespace_strings ():
    try :
        df=pd.read_csv("../etl_Source/sales_data_raw.csv")
        #print(df)
        space1= ((df["CustomerName"] !=df["CustomerName"].str.lstrip()) |
                 (df["Region"] != df["Region"].str.lstrip()))
        space2 = ((df["CustomerName"] != df["CustomerName"].str.rstrip()) |
                  (df["Region"] != df["Region"].str.rstrip()))
        #print("Left space found:\n", df[space1])
        #print("Right space found:\n", df[space2])
    except :
        print("Error somewhere Please check code")

    finally:
        print("Finished")

#Test Case 2: Date format is standardized

def date_format():
    try :
        df=pd.read_csv("../etl_Source/sales_data_raw.csv")
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

        # Compare formatted version to original (convert original to string first)
        format_issue = df["Date"].dt.strftime("%Y/%m/%d") != df["Date"].astype(str)

        #print(df[format_issue])
    except:
        print("Error somewhere Please check code")

#Test Case 4: Total is correctly calculated

def compare_totals():
    # Load source and target
    df_source = pd.read_csv("../etl_Source/sales_data_raw.csv")
    df_target = pd.read_csv("../etl_Source/sales_data_clean.csv")

    # Clean and prepare source data
    df_source["Price"] = df_source["Price"].replace('[\$,]', '', regex=True).astype(float)
    df_source["Quantity"] = df_source["Quantity"].astype(float)
    df_source["CalculatedTotal"] = df_source["Price"] * df_source["Quantity"]
    #print(df_source)
    # Merge on TransactionID to align source and target
    df_merged = pd.merge(df_source, df_target[["TransactionID", "Total"]], on="TransactionID", how="inner", suffixes=('_source', '_target'))
    #print(df_merged)
    # Compare totals row by row
    for i, row in df_merged.iterrows():
        source_total = round(row["CalculatedTotal"], 2)
        target_total = round(row["Total_target"], 2)

        if source_total != target_total:
            print(f"❌ Mismatch in TransactionID {row['TransactionID']} — Source: {source_total}, Target: {target_total}")
        else:
            print(f"✅ Match in TransactionID {row['TransactionID']} — Total: {source_total}")

#Test Case 5: Rows with missing Date or CustomerName are dropped

def validate_dropped_rows():
    # Load source and target
    df_source = pd.read_csv("../etl_Source/sales_data_raw.csv")
    df_target = pd.read_csv("../etl_Source/sales_data_clean.csv")

    # 1. Identify rows with missing Date or CustomerName in the source
    dropped_rows = df_source[
        df_source["Date"].isna() | df_source["CustomerName"].isna() |
        (df_source["Date"].astype(str).str.strip() == "") |
        (df_source["CustomerName"].astype(str).str.strip() == "")
    ]
    #print(dropped_rows)

    # 2. Check if any of those TransactionIDs still exist in target
    missing_check = df_target[df_target["TransactionID"].isin(dropped_rows["TransactionID"])]

    # 3. Output the result
    if not missing_check.empty:
        print("❌ These rows with missing Date or CustomerName were NOT dropped from target:")
        print(missing_check)
    else:
        print("✅ All rows with missing Date or CustomerName were correctly dropped.")


def row_column_check():
    # Load source and target
    df_source = pd.read_csv("../etl_Source/sales_data_raw.csv")
    df_target = pd.read_csv("../etl_Source/sales_data_clean.csv")

    # Ensure same shape for row-wise comparison
    min_len = min(len(df_source), len(df_target))

    # Only compare matching rows by index
    for i in range(min_len):
        for col in df_source.columns:
            val_source = str(df_source.loc[i, col]).strip()
            val_target = str(df_target.loc[i, col]).strip()

            if val_source != val_target:
                print(f"❌ Mismatch at row {i}, column '{col}': Source='{val_source}' | Target='{val_target}'")

    print("✅ Row-column comparison complete.")



whitespace_strings()
date_format()
compare_totals()
validate_dropped_rows()
row_column_check()


