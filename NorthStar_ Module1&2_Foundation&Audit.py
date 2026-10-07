# WEEK 1 — Foundation


import pandas as pd
import numpy as np
import os


# ============================================================
# MODULE 1 — FILE INGESTION
# ============================================================



def load_file(file_path):

    try:

        if not os.path.exists(file_path):
            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        if file_path.lower().endswith(".csv"):

            try:
                df = pd.read_csv(file_path)

            except pd.errors.EmptyDataError:
                raise ValueError(
                    f"CSV file is empty: {file_path}"
                )

            except pd.errors.ParserError as e:
                raise ValueError(
                    f"CSV parsing error: {e}"
                )

        elif file_path.lower().endswith(".json"):

            try:
                df = pd.read_json(file_path)

            except ValueError as e:
                raise ValueError(
                    f"Invalid JSON file: {e}"
                )

        else:
            raise ValueError(
                "Unsupported file type. "
                "Only CSV and JSON are allowed."
            )

        if df.empty:
            raise ValueError(
                f"File contains no records: {file_path}"
            )

        print(f"Loaded successfully: {file_path}")

        return df

    except FileNotFoundError as e:
        print(f"ERROR: {e}")

    except ValueError as e:
        print(f"ERROR: {e}")

    except Exception as e:
        print(
            f"Unexpected error while loading "
            f"{file_path}: {e}"
        )

    return None


 #Validation functions

def validate_shape(df, expected_shape):

    if df.shape != expected_shape:
        raise ValueError(
            f"Shape mismatch. "
            f"Expected {expected_shape}, "
            f"but got {df.shape}"
        )

    print(f"PASS: Shape validated -> {df.shape}")


def validate_columns(df, expected_columns):

    actual_columns = list(df.columns)

    if actual_columns != expected_columns:
        raise ValueError(
            f"Column mismatch.\n"
            f"Expected: {expected_columns}\n"
            f"Actual: {actual_columns}"
        )

    print("PASS: Columns validated")


def validate_dtypes(df, expected_dtypes):

    for column, expected_dtype in expected_dtypes.items():

        actual_dtype = str(df[column].dtype)

        if actual_dtype != expected_dtype:
            raise ValueError(
                f"Dtype mismatch for {column},"
                f"Expected {expected_dtype}, "
                f"but got {actual_dtype}"
            )

    print("PASS: Data types validated")


def validate_file(
    df,
    expected_shape,
    expected_columns,
    expected_dtypes
):

    print("\n" + "=" * 60)
    print("POST-LOAD VALIDATION")
    print("=" * 60)

    validate_shape(df, expected_shape)
    validate_columns(df, expected_columns)
    validate_dtypes(df, expected_dtypes)

    print("VALIDATION SUCCESS")



# ============================================================
# FILE 1 — CUSTOMERS
# ============================================================

customers_path = "customers.csv"

customers = load_file(customers_path)

if customers is not None:

    customers_columns = [
        "CustomerID",
        "CustomerName",
        "Gender",
        "AgeBand",
        "City",
        "LoyaltyTier",
        "JoinDate",
        "EmailOptIn"
    ]

    customers_dtypes = {
        "CustomerID": "str",
        "CustomerName": "str",
        "Gender": "str",
        "AgeBand": "str",
        "City": "str",
        "LoyaltyTier": "str",
        "JoinDate": "str",
        "EmailOptIn": "str"
    }

    validate_file(
        customers,
        (3022, 8),
        customers_columns,
        customers_dtypes
    )



# ============================================================
# FILE 2 — inventory
# ============================================================

inventory_path = "inventory.csv"

inventory = load_file(inventory_path)

if inventory is not None:

    inventory_columns = [
        "SnapshotMonth",
        "StoreID",
        "ProductID",
        "OnHandUnits",
        "ReorderLevel",
        "StockoutFlag",
    ]

    inventory_dtypes = {
        "SnapshotMonth": "str",
        "StoreID": "str",
        "ProductID": "str",
        "OnHandUnits": "float64",
        "ReorderLevel": "int64",
        "StockoutFlag": "int64",
    }

    validate_file(
        inventory,
        (25920, 6),
        inventory_columns,
        inventory_dtypes
    )


# ============================================================
# FILE 3 — PRODUCTS
# ============================================================

products_path = "products.csv"

products = load_file(products_path)

if products is not None:

    products_columns = [
    
        "ProductID",
        "ProductName",
        "Category",
        "SubCategory",
        "Brand",
        "UnitCost",
        "MRP",
        "LaunchDate"
    ]

    products_dtypes = {
        "ProductID": "str",
        "ProductName": "str",
        "Category": "str",
        "SubCategory": "str",
        "Brand": "str",
        "UnitCost": "float64",
        "MRP": "float64",
        "LaunchDate": "str"
    }

    validate_file(
        products,
        (528, 8),
        products_columns,
        products_dtypes
    )

# ============================================================
# FILE 4 — Returns
# ============================================================

returns_path = "returns.csv"

returns = load_file(returns_path)

if returns is not None:

    returns_columns = [
        "ReturnID",
        "TransactionID",
        "ReturnDate",
        "Reason",
        "RefundAmount",
        "Condition",
    ]

    returns_dtypes = {
        "ReturnID": "str",
        "TransactionID": "str",
        "ReturnDate": "str",
        "Reason": "str",
        "RefundAmount": "float64",
        "Condition": "str",
    }

    validate_file(
         returns,
        (3415, 6),
       returns_columns,
        returns_dtypes
    )


# ============================================================
# FILE 5 — store_targets_legacy
# ============================================================

store_targets_legacy_path = "store_targets_legacy.csv"

store_targets_legacy = load_file(store_targets_legacy_path)

if store_targets_legacy is not None:

    store_targets_legacy_columns = [
        "store_code",
        "period",
        "sales_target_inr",
        "footfall_target",
    ]

    store_targets_legacy_dtypes = {
        "store_code": "str",
        "period": "str",
        "sales_target_inr": "float64",
        "footfall_target": "int64",
    }

    validate_file(
         store_targets_legacy,
        (432, 4),
       store_targets_legacy_columns,
        store_targets_legacy_dtypes
    )


# ============================================================
# FILE 6 — Stores
# ============================================================

stores_path = "stores.csv"

stores = load_file(stores_path)

if stores is not None:

    stores_columns = [
    
        "StoreID",
        "StoreName",
        "City",
        "State",
        "Format",
        "OpenDate",
        "SqFt",
        "Region"
    ]

    stores_dtypes = {
        "StoreID": "str",
        "StoreName": "str",
        "City": "str",
        "State": "str",
        "Format": "str",
        "OpenDate": "str",
        "SqFt": "float64",
        "Region": "str"
    }

    validate_file(
        stores,
        (18, 8),
        stores_columns,
        stores_dtypes
    )



# ============================================================
# FILE 7 — Transactions
# ============================================================

transactions_path = "transactions.csv"

transactions = load_file(transactions_path)

if transactions is not None:

    transactions_columns = [
        "TransactionID",
        "OrderDate",
        "CustomerID",
        "StoreID",
        "ProductID",
        "Quantity",
        "Discount",
        "LineAmount",
        "Channel",
        "PaymentMode",
    ]

    transactions_dtypes = {
        "TransactionID": "str",
        "OrderDate": "str",
        "CustomerID": "str",
        "StoreID": "str",
        "ProductID": "str",
        "Quantity": "int64",
        "Discount": "float64",
        "LineAmount": "float64",
        "Channel" : "str",
        "PaymentMode": "str",
    }

    validate_file(
        transactions,
        (60577, 10),
        transactions_columns,
        transactions_dtypes
    )


# ============================================================
# FILE 8 — campaigns.json
# ============================================================

campaigns_path = "campaigns.json"

campaigns = load_file(campaigns_path)

if campaigns is not None:
   print(campaigns.shape)
   print(campaigns.columns.tolist())
   print(campaigns.dtypes)
  
   campaigns_columns = [
       "campaign_id",
       "name",
       "channel",
       "start_date",
       "end_date",
       "spend_inr",
       "impressions",
       "clicks",
       "target_category",
   ]

   campaigns_dtypes = {
        "campaign_id": "str",
        "name": "str",
        "channel": "str",
        "start_date": "str",
        "end_date": "str",
        "spend_inr": "float64",
        "impressions": "int64",
        "clicks": "int64",
        "target_category": "str",
  }

   validate_file(  
          campaigns,
        (40, 9),
         campaigns_columns,
         campaigns_dtypes
    )

# ============================================================
# MODULE 2 — DATA AUDIT 
# ============================================================

# 1. STORE ALL TABLES

tables = {
    "Customers": customers,
    "Inventory": inventory,
    "Products": products,
    "Returns": returns,
    "Store Targets Legacy": store_targets_legacy,
    "Stores": stores,
    "Transactions": transactions,
    "Campaigns" : campaigns
}

# ============================================================
# 2.  DATA  AUDIT
# ============================================================

def audit_table(df, table_name):


    print("\n" + "=" * 80)
    print(f"AUDIT — {table_name}")
    print("=" * 80)


# ============================================================
# 3. BEFORE-CLEANING AUDIT
# ============================================================


print("\n\n" + "#" * 80)
print("NORTHSTAR RETAIL — MODULE 2 DATA QUALITY AUDIT")
print("#" * 80)

for name, df in tables.items():

    audit_table(df, name)

# ============================================================
# 3 Audit Issues and Document 
# ============================================================

audit_issues = []


def audit_table(df, table_name):

    print("\n" + "=" * 80)
    print(f"DATA QUALITY AUDIT — {table_name}")
    print("=" * 80)

    # ========================================================
    # 1. SHAPE
    # ========================================================

    print("\n1. SHAPE")

    print(f"Rows    : {df.shape[0]}")
    print(f"Columns : {df.shape[1]}")

    # ========================================================
    # 2. DATA TYPES
    # ========================================================

    print("\n2. DATA TYPES")

    print(df.dtypes)

    # ========================================================
    # 3. MISSING VALUES
    # ========================================================

    print("\n3. MISSING VALUES")

    missing_count = df.isna().sum()

    missing_percent = (
        missing_count / len(df) * 100
    ).round(2)

    missing_report = pd.DataFrame({
        "Missing_Count": missing_count,
        "Missing_Percent": missing_percent
    })

    missing_report = missing_report[
        missing_report["Missing_Count"] > 0
    ]

    if missing_report.empty:

        print("PASS — No missing values.")

    else:

        print(missing_report)

        for column, row in missing_report.iterrows():

            audit_issues.append({
                "Table": table_name,
                "Column": column,
                "Issue": "Missing values",
                "Rows Affected": int(row["Missing_Count"]),
                "Details": f"{row['Missing_Percent']}% missing"
            })

    # ========================================================
    # 4. DUPLICATE ROWS
    # ========================================================

    print("\n4. DUPLICATE ROWS")

    duplicate_count = df.duplicated().sum()

    if duplicate_count == 0:

        print("PASS — No duplicate rows.")

    else:

        print(
            f"ISSUE — {duplicate_count} duplicate rows found."
        )

        audit_issues.append({
            "Table": table_name,
            "Column": "ALL",
            "Issue": "Duplicate rows",
            "Rows Affected": int(duplicate_count),
            "Details": "Complete duplicate records"
        })

    # ========================================================
    # 5. ID / KEY AUDIT
    # ========================================================

    print("\n5. ID / KEY AUDIT")

    id_columns = [
        column
        for column in df.columns
        if "id" in column.lower()
        or column.lower().endswith("_code")
    ]

    if not id_columns:

        print("No ID columns detected.")

    else:

        for column in id_columns:

            null_count = df[column].isna().sum()

            duplicate_count = df[column].duplicated(
                keep=False
            ).sum()

            print(f"\n{column}")
            print(f"  Null IDs      : {null_count}")
            print(f"  Duplicate IDs : {duplicate_count}")

            if null_count > 0:

                audit_issues.append({
                    "Table": table_name,
                    "Column": column,
                    "Issue": "Null ID",
                    "Rows Affected": int(null_count),
                    "Details": "ID/key value is missing"
                })

            if duplicate_count > 0:

                audit_issues.append({
                    "Table": table_name,
                    "Column": column,
                    "Issue": "Duplicate ID",
                    "Rows Affected": int(duplicate_count),
                    "Details": "ID/key value occurs multiple times"
                })

    # ========================================================
    # 6. TEXT QUALITY
    # ========================================================

    print("\n6. TEXT QUALITY")

    text_columns = df.select_dtypes(
        include=["object", "string"]
    ).columns

    text_issue_found = False

    for column in text_columns:

        series = df[column].dropna().astype(str)

        whitespace_count = (
            series.str.strip() != series
        ).sum()

        empty_count = (
            df[column]
            .fillna("")
            .astype(str)
            .str.strip()
            .eq("")
            .sum()
        )

        if whitespace_count > 0:

            text_issue_found = True

            print(
                f"{column}: "
                f"{whitespace_count} leading/trailing "
                f"whitespace issues"
            )

            audit_issues.append({
                "Table": table_name,
                "Column": column,
                "Issue": "Whitespace",
                "Rows Affected": int(whitespace_count),
                "Details": "Leading/trailing spaces found"
            })

        if empty_count > 0:

            text_issue_found = True

            print(
                f"{column}: "
                f"{empty_count} empty strings"
            )

            audit_issues.append({
                "Table": table_name,
                "Column": column,
                "Issue": "Empty strings",
                "Rows Affected": int(empty_count),
                "Details": "Blank text values found"
            })

    if not text_issue_found:

        print("PASS — No obvious text-formatting issues.")

    # ========================================================
    # 7. UNIQUE / CATEGORICAL VALUES
    # ========================================================

    print("\n7. UNIQUE VALUES")

    for column in text_columns:

        unique_values = (
            df[column]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
        )

        print(f"\n{column}:")
        print(unique_values)

    # ========================================================
    # 8. NUMERIC AUDIT
    # ========================================================

    print("\n8. NUMERIC AUDIT")

    numeric_columns = df.select_dtypes(
        include=np.number
    ).columns

    if len(numeric_columns) == 0:

        print("No numeric columns.")

    else:

        for column in numeric_columns:

            negative_count = (
                df[column] < 0
            ).sum()

            zero_count = (
                df[column] == 0
            ).sum()

            print(
                f"{column}: "
                f"negative={negative_count}, "
                f"zero={zero_count}"
            )

            if negative_count > 0:

                audit_issues.append({
                    "Table": table_name,
                    "Column": column,
                    "Issue": "Negative numeric values",
                    "Rows Affected": int(negative_count),
                    "Details": "Negative values require business review"
                })

    # ========================================================
    # 9. DATE AUDIT
    # ========================================================

    print("\n9. DATE AUDIT")

    date_columns = [
        column
        for column in df.columns
        if "date" in column.lower()
        or "month" in column.lower()
        or "period" in column.lower()
    ]

    if not date_columns:

        print("No date/period columns detected.")

    else:

        for column in date_columns:

            converted_dates = pd.to_datetime(
                df[column],
                errors="coerce"
            )

            invalid_dates = (
                df[column].notna()
                & converted_dates.isna()
            ).sum()

            print(
                f"{column}: "
                f"{invalid_dates} invalid dates"
            )

            if invalid_dates > 0:

                audit_issues.append({
                    "Table": table_name,
                    "Column": column,
                    "Issue": "Invalid date values",
                    "Rows Affected": int(invalid_dates),
                    "Details": "Values cannot be converted to valid dates"
                })

    # ========================================================
    # 10. AUDIT SUMMARY
    # ========================================================

    table_issues = [
        issue
        for issue in audit_issues
        if issue["Table"] == table_name
    ]

    print("\n" + "-" * 80)
    print(f"AUDIT SUMMARY — {table_name}")
    print("-" * 80)

    if len(table_issues) == 0:

        print("PASS — No issues documented.")

    else:

        print(f"ISSUES FOUND: {len(table_issues)}")

        for issue in table_issues:

            print(
                f"- {issue['Column']} | "
                f"{issue['Issue']} | "
                f"Rows: {issue['Rows Affected']}"
            )

    print("-" * 80)


# ============================================================
# RUN AUDIT ON ALL TABLES
# ============================================================

print("\n" + "#" * 80)
print("NORTHSTAR RETAIL — MODULE 2 DATA QUALITY AUDIT")
print("#" * 80)

for name, df in tables.items():
    audit_table(df, name)

# ============================================================
# CREATE AUDIT LOG
# ============================================================

audit_log = pd.DataFrame(audit_issues)

print("\n" + "=" * 80)
print("COMPLETE DATA AUDIT LOG")
print("=" * 80)

if audit_log.empty:

    print("PASS — No data quality issues found.")

else:

    print(audit_log)

    audit_log.to_csv(
        "data_audit_log.csv",
        index=False
    )

    print("\nAudit log saved as: data_audit_log.csv")