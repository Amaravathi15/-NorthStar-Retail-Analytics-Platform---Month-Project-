# Module 3 — Cleaning


import pandas as pd
import os
import numpy as np



# ============================================================
# LOAD 1 — CAMPAIGNS
# ============================================================

campaigns = pd.read_json("campaigns.json")

print("Campaigns loaded successfully")
print("Shape:", campaigns.shape)
print(campaigns.head())

# ============================================================
# LOAD 2 customers
# ============================================================


customers = pd.read_csv("customers.csv")

print("Customers loaded successfully")
print("Shape:", customers.shape)
print(customers.head())
    
# ============================================================
# LOAD 3 inventory
# ============================================================


inventory = pd.read_csv("inventory.csv")

print("Inventory loaded successfully")
print("Shape:", inventory.shape)
print(inventory.head())

    
# ============================================================
# LOAD 4 products
# ============================================================

products = pd.read_csv("products.csv")

print("Products loaded successfully")
print("Shape:", products.shape)
print(products.head())


# ============================================================
# LOAD 5 returns
# ============================================================


returns = pd.read_csv("returns.csv")

print("Returns loaded successfully")
print("Shape:", returns.shape)
print(returns.head())


# ============================================================
# LOAD 6 Store_targets_legacy
# ============================================================


store_targets_legacy = pd.read_csv("store_targets_legacy.csv")

print("Store targets legacy loaded successfully")
print("Shape:", store_targets_legacy.shape)
print(store_targets_legacy.head())

# ============================================================
# LOAD 7 STORES DATA
# ============================================================


stores = pd.read_csv("stores.csv")

print("Stores loaded successfully")
print("Shape:", stores.shape)
print(stores.head())


# ============================================================
# LOAD 8 Transactions
# ============================================================


transactions = pd.read_csv("transactions.csv")

print("Transactions loaded successfully")
print("Shape:", transactions.shape)
print(transactions.head())


# ============================================================
# 1. CLEANING LOG
# ============================================================

cleaning_log = []


def log_cleaning(
    table,
    column,
    issue,
    rows_affected,
    action,
    justification
):

    cleaning_log.append({
        "Table": table,
        "Column": column,
        "Issue": issue,
        "Rows Affected": rows_affected,
        "Action": action,
        "Justification": justification
    })


# ============================================================
# 2. HELPER FUNCTION — STANDARDISE TEXT
# ============================================================

def standardise_text(df, table_name, column):

    if column not in df.columns:
        return

    before = df[column].copy()

    # Convert non-null values to string
    df[column] = df[column].apply(
        lambda x: x.strip() if isinstance(x, str) else x
    )

    # Replace multiple spaces with single space
    df[column] = df[column].apply(
        lambda x: " ".join(x.split()) if isinstance(x, str) else x
    )

    # Count changed rows
    changed = (
        before.fillna("__NULL__").astype(str)
        != df[column].fillna("__NULL__").astype(str)
    ).sum()

    if changed > 0:

        log_cleaning(
            table_name,
            column,
            "Leading/trailing or repeated whitespace",
            changed,
            "Trimmed whitespace and standardised spacing",
            "Text fields should have consistent formatting so that "
            "matching, grouping and joins are reliable."
        )


# ============================================================
# 3. CUSTOMERS
# ============================================================

print("\n" + "=" * 80)
print("CLEANING — CUSTOMERS")
print("=" * 80)


# CustomerID
# Keep identifiers unchanged except whitespace.

standardise_text(customers, "Customers", "CustomerID")


# CustomerName
standardise_text(customers, "Customers", "CustomerName")


# Gender
standardise_text(customers, "Customers", "Gender")

if "Gender" in customers.columns:

    before = customers["Gender"].copy()

    customers["Gender"] = (
        customers["Gender"]
        .astype("string")
        .str.strip()
        .str.title()
    )

    changed = (
        before.fillna("__NULL__").astype(str)
        != customers["Gender"].fillna("__NULL__").astype(str)
    ).sum()

    if changed > 0:

        log_cleaning(
            "Customers",
            "Gender",
            "Inconsistent text case",
            changed,
            "Standardised Gender to title case",
            "Consistent categorical labels are required for "
            "accurate grouping and reporting."
        )


# AgeBand
standardise_text(customers, "Customers", "AgeBand")


# City
if "City" in customers.columns:

    before = customers["City"].copy()

    customers["City"] = (
        customers["City"]
        .astype("string")
        .str.strip()
        .str.title()
    )

    changed = (
        before.fillna("__NULL__").astype(str)
        != customers["City"].fillna("__NULL__").astype(str)
    ).sum()

    if changed > 0:

        log_cleaning(
            "Customers",
            "City",
            "Inconsistent city formatting",
            changed,
            "Trimmed whitespace and standardised city names",
            "City values must use consistent labels for geographic analysis."
        )


# LoyaltyTier
if "LoyaltyTier" in customers.columns:

    before = customers["LoyaltyTier"].copy()

    customers["LoyaltyTier"] = (
        customers["LoyaltyTier"]
        .astype("string")
        .str.strip()
        .str.title()
    )

    changed = (
        before.fillna("__NULL__").astype(str)
        != customers["LoyaltyTier"].fillna("__NULL__").astype(str)
    ).sum()

    if changed > 0:

        log_cleaning(
            "Customers",
            "LoyaltyTier",
            "Inconsistent categorical formatting",
            changed,
            "Standardised LoyaltyTier labels",
            "Consistent categories are required for reliable customer segmentation."
        )


# JoinDate
if "JoinDate" in customers.columns:

    before_invalid = customers["JoinDate"].notna().sum()

    customers["JoinDate"] = pd.to_datetime(
        customers["JoinDate"],
        errors="coerce"
    )

    after_invalid = customers["JoinDate"].isna().sum()

    if after_invalid > 0:

        log_cleaning(
            "Customers",
            "JoinDate",
            "Invalid or missing dates",
            after_invalid,
            "Converted valid values to datetime; invalid values retained as NaT",
            "Invalid dates cannot be used reliably for customer tenure analysis."
        )


# EmailOptIn
standardise_text(customers, "Customers", "EmailOptIn")



# ============================================================
# 4. INVENTORY
# ============================================================

print("\n" + "=" * 80)
print("CLEANING — INVENTORY")
print("=" * 80)


standardise_text(inventory, "Inventory", "StoreID")
standardise_text(inventory, "Inventory", "ProductID")


# SnapshotMonth
if "SnapshotMonth" in inventory.columns:

    inventory["SnapshotMonth"] = pd.to_datetime(
        inventory["SnapshotMonth"],
        errors="coerce"
    )

    log_cleaning(
        "Inventory",
        "SnapshotMonth",
        "Date/period formatting",
        len(inventory),
        "Converted SnapshotMonth to datetime",
        "Monthly inventory snapshots should use a consistent date type."
    )


# OnHandUnits
if "OnHandUnits" in inventory.columns:

    negative_count = (inventory["OnHandUnits"] < 0).sum()

    if negative_count > 0:

        log_cleaning(
            "Inventory",
            "OnHandUnits",
            "Negative inventory quantity",
            negative_count,
            "Flagged for business review; values were not automatically replaced",
            "Negative stock may represent a legitimate adjustment or data issue. "
            "It should not be replaced without business evidence."
        )


# ReorderLevel
if "ReorderLevel" in inventory.columns:

    negative_count = (inventory["ReorderLevel"] < 0).sum()

    if negative_count > 0:

        log_cleaning(
            "Inventory",
            "ReorderLevel",
            "Negative reorder level",
            negative_count,
            "Flagged for business review; values were not automatically replaced",
            "A reorder threshold should normally be non-negative, but the correct "
            "replacement cannot be inferred from the dataset."
        )


# StockoutFlag
if "StockoutFlag" in inventory.columns:

    invalid_flag = ~inventory["StockoutFlag"].isin([0, 1])
    invalid_count = invalid_flag.sum()

    if invalid_count > 0:

        log_cleaning(
            "Inventory",
            "StockoutFlag",
            "Invalid flag values",
            invalid_count,
            "Flagged for review",
            "StockoutFlag should contain binary values only."
        )



# ============================================================
# 5. PRODUCTS
# ============================================================

print("\n" + "=" * 80)
print("CLEANING — PRODUCTS")
print("=" * 80)


standardise_text(products, "Products", "ProductID")
standardise_text(products, "Products", "ProductName")
standardise_text(products, "Products", "Category")
standardise_text(products, "Products", "SubCategory")
standardise_text(products, "Products", "Brand")


# LaunchDate
if "LaunchDate" in products.columns:

    products["LaunchDate"] = pd.to_datetime(
        products["LaunchDate"],
        errors="coerce"
    )

    log_cleaning(
        "Products",
        "LaunchDate",
        "Date formatting",
        len(products),
        "Converted LaunchDate to datetime",
        "A consistent date type is required for product age and launch analysis."
    )


# UnitCost
if "UnitCost" in products.columns:

    negative_count = (products["UnitCost"] < 0).sum()

    if negative_count > 0:

        log_cleaning(
            "Products",
            "UnitCost",
            "Negative cost",
            negative_count,
            "Flagged for review",
            "Product cost cannot normally be negative; automatic replacement "
            "would require a business rule."
        )


# MRP
if "MRP" in products.columns:

    negative_count = (products["MRP"] < 0).sum()

    if negative_count > 0:

        log_cleaning(
            "Products",
            "MRP",
            "Negative selling price",
            negative_count,
            "Flagged for review",
            "MRP should not be negative and should be investigated before replacement."
        )




# ============================================================
# 6. RETURNS
# ============================================================

print("\n" + "=" * 80)
print("CLEANING — RETURNS")
print("=" * 80)


standardise_text(returns, "Returns", "ReturnID")
standardise_text(returns, "Returns", "TransactionID")
standardise_text(returns, "Returns", "Reason")
standardise_text(returns, "Returns", "Condition")


# ReturnDate
if "ReturnDate" in returns.columns:

    returns["ReturnDate"] = pd.to_datetime(
        returns["ReturnDate"],
        errors="coerce"
    )

    log_cleaning(
        "Returns",
        "ReturnDate",
        "Date formatting",
        len(returns),
        "Converted ReturnDate to datetime",
        "Return dates must use a consistent date type for return trend analysis."
    )


# RefundAmount
if "RefundAmount" in returns.columns:

    negative_count = (returns["RefundAmount"] < 0).sum()

    if negative_count > 0:

        log_cleaning(
            "Returns",
            "RefundAmount",
            "Negative refund amount",
            negative_count,
            "Flagged for review",
            "Negative refunds require business confirmation and should not "
            "be replaced automatically."
        )



# ============================================================
# 7. STORE TARGETS LEGACY
# ============================================================

print("\n" + "=" * 80)
print("CLEANING — STORE TARGETS LEGACY")
print("=" * 80)


standardise_text(
    store_targets_legacy,
    "Store Targets Legacy",
    "store_code"
)


standardise_text(
    store_targets_legacy,
    "Store Targets Legacy",
    "period"
)

if "period" in store_targets_legacy.columns:

    store_targets_legacy["period"] = pd.to_datetime(
        store_targets_legacy["period"],
        format="%b-%Y",
        errors="coerce"
    )

    log_cleaning(
        "Store Targets Legacy",
        "period",
        "Period formatting",
        len(store_targets_legacy),
        "Converted Jan-YYYY values to datetime",
        "Consistent period dates are required for target-versus-actual analysis."
    )

# Sales target
if "sales_target_inr" in store_targets_legacy.columns:

    negative_count = (
        store_targets_legacy["sales_target_inr"] < 0
    ).sum()

    if negative_count > 0:

        log_cleaning(
            "Store Targets Legacy",
            "sales_target_inr",
            "Negative sales target",
            negative_count,
            "Flagged for review",
            "Sales targets should not normally be negative."
        )


# Footfall target
if "footfall_target" in store_targets_legacy.columns:

    negative_count = (
        store_targets_legacy["footfall_target"] < 0
    ).sum()

    if negative_count > 0:

        log_cleaning(
            "Store Targets Legacy",
            "footfall_target",
            "Negative footfall target",
            negative_count,
            "Flagged for review",
            "Footfall targets should not normally be negative."
        )



# ============================================================
# 8. STORES
# ============================================================

print("\n" + "=" * 80)
print("CLEANING — STORES")
print("=" * 80)


standardise_text(stores, "Stores", "StoreID")
standardise_text(stores, "Stores", "StoreName")
standardise_text(stores, "Stores", "City")
standardise_text(stores, "Stores", "State")
standardise_text(stores, "Stores", "Format")
standardise_text(stores, "Stores", "Region")


# OpenDate
if "OpenDate" in stores.columns:

    stores["OpenDate"] = pd.to_datetime(
        stores["OpenDate"],
        errors="coerce"
    )

    log_cleaning(
        "Stores",
        "OpenDate",
        "Date formatting",
        len(stores),
        "Converted OpenDate to datetime",
        "Store opening dates need a consistent date type for store age analysis."
    )


# SqFt
if "SqFt" in stores.columns:

    negative_count = (stores["SqFt"] < 0).sum()

    if negative_count > 0:

        log_cleaning(
            "Stores",
            "SqFt",
            "Negative store area",
            negative_count,
            "Flagged for review",
            "Store area cannot normally be negative."
        )



#============================================================
# 9. TRANSACTIONS
# ============================================================

print("\n" + "=" * 80)
print("CLEANING — TRANSACTIONS")
print("=" * 80)


standardise_text(transactions, "Transactions", "TransactionID")
standardise_text(transactions, "Transactions", "CustomerID")
standardise_text(transactions, "Transactions", "StoreID")
standardise_text(transactions, "Transactions", "ProductID")
standardise_text(transactions, "Transactions", "Channel")
standardise_text(transactions, "Transactions", "PaymentMode")


# OrderDate
if "OrderDate" in transactions.columns:

    transactions["OrderDate"] = pd.to_datetime(
        transactions["OrderDate"],
        errors="coerce"
    )

    log_cleaning(
        "Transactions",
        "OrderDate",
        "Date formatting",
        len(transactions),
        "Converted OrderDate to datetime",
        "Transaction dates must use a consistent date type for sales analysis."
    )


# Quantity
if "Quantity" in transactions.columns:

    negative_count = (
        transactions["Quantity"] < 0
    ).sum()

    if negative_count > 0:

        log_cleaning(
            "Transactions",
            "Quantity",
            "Negative quantity",
            negative_count,
            "Flagged for review",
            "Negative quantities may represent returns or adjustments and "
            "should not be overwritten without business rules."
        )


# Discount
if "Discount" in transactions.columns:

    invalid_discount = (
        (transactions["Discount"] < 0)
        | (transactions["Discount"] > 1)
    )

    invalid_count = invalid_discount.sum()

    if invalid_count > 0:

        log_cleaning(
            "Transactions",
            "Discount",
            "Discount outside expected range",
            invalid_count,
            "Flagged for review",
            "Discount values should follow a consistent business definition."
        )


# LineAmount
if "LineAmount" in transactions.columns:

    negative_count = (
        transactions["LineAmount"] < 0
    ).sum()

    if negative_count > 0:

        log_cleaning(
            "Transactions",
            "LineAmount",
            "Negative transaction amount",
            negative_count,
            "Flagged for review",
            "Negative amounts may represent refunds or adjustments and "
            "should not be automatically deleted."
        )




# ============================================================
# 10. CAMPAIGNS
# ============================================================

print("\n" + "=" * 80)
print("CLEANING — CAMPAIGNS")
print("=" * 80)


standardise_text(campaigns, "Campaigns", "campaign_id")
standardise_text(campaigns, "Campaigns", "name")
standardise_text(campaigns, "Campaigns", "channel")
standardise_text(campaigns, "Campaigns", "target_category")


# Start date
if "start_date" in campaigns.columns:

    campaigns["start_date"] = pd.to_datetime(
        campaigns["start_date"],
        errors="coerce"
    )

    log_cleaning(
        "Campaigns",
        "start_date",
        "Date formatting",
        len(campaigns),
        "Converted start_date to datetime",
        "Campaign dates must use a consistent date type for campaign analysis."
    )


# End date
if "end_date" in campaigns.columns:

    campaigns["end_date"] = pd.to_datetime(
        campaigns["end_date"],
        errors="coerce"
    )

    log_cleaning(
        "Campaigns",
        "end_date",
        "Date formatting",
        len(campaigns),
        "Converted end_date to datetime",
        "Campaign dates must use a consistent date type for duration analysis."
    )


# Spend
if "spend_inr" in campaigns.columns:

    negative_count = (
        campaigns["spend_inr"] < 0
    ).sum()

    if negative_count > 0:

        log_cleaning(
            "Campaigns",
            "spend_inr",
            "Negative campaign spend",
            negative_count,
            "Flagged for review",
            "Campaign spend should not normally be negative."
        )


# Impressions
if "impressions" in campaigns.columns:

    negative_count = (
        campaigns["impressions"] < 0
    ).sum()

    if negative_count > 0:

        log_cleaning(
            "Campaigns",
            "impressions",
            "Negative impressions",
            negative_count,
            "Flagged for review",
            "Impressions represent counts and should not be negative."
        )


# Clicks
if "clicks" in campaigns.columns:

    negative_count = (
        campaigns["clicks"] < 0
    ).sum()

    if negative_count > 0:

        log_cleaning(
            "Campaigns",
            "clicks",
            "Negative clicks",
            negative_count,
            "Flagged for review",
            "Clicks represent counts and should not be negative."
        )


# ============================================================
# 11. REFERENTIAL INTEGRITY CHECK
# ============================================================

print("\n" + "=" * 80)
print("11. REFERENTIAL INTEGRITY CHECK")
print("=" * 80)

referential_issues = []


# ------------------------------------------------------------
# Helper function: check child IDs against parent IDs
# ------------------------------------------------------------

def check_referential_integrity(
    child_df,
    child_column,
    parent_df,
    parent_column,
    child_table,
    parent_table,
    allow_values=None
):

    if allow_values is None:
        allow_values = []

    # Normalise IDs for comparison without changing source columns
    child_ids = (
        child_df[child_column]
        .astype("string")
        .str.strip()
    )

    parent_ids = set(
        parent_df[parent_column]
        .dropna()
        .astype("string")
        .str.strip()
    )

    # Missing foreign keys
    missing_mask = child_df[child_column].isna()

    # Allowed special values, such as ONLINE
    allowed_mask = child_ids.isin(allow_values)

    # Orphan foreign keys
    orphan_mask = (
        child_ids.notna()
        & ~child_ids.isin(parent_ids)
        & ~allowed_mask
    )

    missing_count = int(missing_mask.sum())
    orphan_count = int(orphan_mask.sum())

    print(f"\n{child_table} -> {parent_table}")
    print(f"Missing {child_column}: {missing_count}")
    print(f"Orphan {child_column}: {orphan_count}")

    # Record missing foreign keys
    if missing_count > 0:

        log_cleaning(
            child_table,
            child_column,
            "Missing foreign key",
            missing_count,
            "Retained and flagged for review",
            "The correct ID cannot be safely inferred."
        )

        for row_index in child_df.index[missing_mask]:

            referential_issues.append({
                "Table": child_table,
                "Column": child_column,
                "RowIndex": row_index,
                "InvalidID": None,
                "Issue": "Missing foreign key",
                "ParentTable": parent_table
            })

    # Record orphan foreign keys
    if orphan_count > 0:

        log_cleaning(
            child_table,
            child_column,
            "Referential mismatch",
            orphan_count,
            "Retained and flagged for review",
            f"ID does not exist in {parent_table}."
        )

        for row_index in child_df.index[orphan_mask]:

            referential_issues.append({
                "Table": child_table,
                "Column": child_column,
                "RowIndex": row_index,
                "InvalidID": child_ids.loc[row_index],
                "Issue": "Referential mismatch",
                "ParentTable": parent_table
            })

    return {
        "missing_count": missing_count,
        "orphan_count": orphan_count
    }



# ------------------------------------------------------------
# 11.1 Transactions.CustomerID -> Customers.CustomerID
# ------------------------------------------------------------

check_referential_integrity(
    transactions,
    "CustomerID",
    customers,
    "CustomerID",
    "Transactions",
    "Customers"
)


# ------------------------------------------------------------
# 11.2 Transactions.StoreID -> Stores.StoreID
# ------------------------------------------------------------

check_referential_integrity(
    transactions,
    "StoreID",
    stores,
    "StoreID",
    "Transactions",
    "Stores",
    allow_values=["ONLINE"]
)


# ------------------------------------------------------------
# 11.3 Transactions.ProductID -> Products.ProductID
# ------------------------------------------------------------

check_referential_integrity(
    transactions,
    "ProductID",
    products,
    "ProductID",
    "Transactions",
    "Products"
)


# ------------------------------------------------------------
# 11.4 Inventory.StoreID -> Stores.StoreID
# ------------------------------------------------------------

check_referential_integrity(
    inventory,
    "StoreID",
    stores,
    "StoreID",
    "Inventory",
    "Stores"
)


# ------------------------------------------------------------
# 11.5 Inventory.ProductID -> Products.ProductID
# ------------------------------------------------------------

check_referential_integrity(
    inventory,
    "ProductID",
    products,
    "ProductID",
    "Inventory",
    "Products"
)


# ------------------------------------------------------------
# 11.6 Returns.TransactionID -> Transactions.TransactionID
# ------------------------------------------------------------

check_referential_integrity(
    returns,
    "TransactionID",
    transactions,
    "TransactionID",
    "Returns",
    "Transactions"
)


# ------------------------------------------------------------
# 11.7 Store Targets.store_code -> Stores.StoreID
# ------------------------------------------------------------

check_referential_integrity(
    store_targets_legacy,
    "store_code",
    stores,
    "StoreID",
    "Store Targets Legacy",
    "Stores"
)


# ============================================================
# 12. SAVE REFERENTIAL ISSUES REPORT
# ============================================================

os.makedirs("NorthStar_Cleaned_Data", exist_ok=True)

referential_issues_df = pd.DataFrame(
    referential_issues,
    columns=[
        "Table",
        "Column",
        "RowIndex",
        "InvalidID",
        "Issue",
        "ParentTable"
    ]
)

referential_issues_df.to_csv(
    "NorthStar_Cleaned_Data/referential_issues.csv",
    index=False
)

print("\nReferential issues saved.")

# ============================================================
# 13. SAVE DATA CLEANING LOG
# ============================================================

cleaning_log_df = pd.DataFrame(
    cleaning_log,
    columns=[
        "Table",
        "Column",
        "Issue",
        "Rows Affected",
        "Action",
        "Justification"
    ]
)

cleaning_log_df.to_csv(
    "NorthStar_Cleaned_Data/data_cleaning_log.csv",
    index=False
)

print("Cleaning log saved.")



# ============================================================
# 14. EXPORT ALL EIGHT CLEANED TABLES
# ============================================================

cleaned_tables = {
    "customers": customers,
    "inventory": inventory,
    "products": products,
    "returns": returns,
    "store_targets_legacy": store_targets_legacy,
    "stores": stores,
    "transactions": transactions,
    "campaigns": campaigns
}

for table_name, dataframe in cleaned_tables.items():

    output_path = os.path.join(
        "NorthStar_Cleaned_Data",
        f"cleaned_{table_name}.csv"
    )

    dataframe.to_csv(
        output_path,
        index=False
    )

    print(
        f"Saved {table_name}: "
        f"{dataframe.shape} -> {output_path}"
    )


# ============================================================
# 15. FINAL DATA QUALITY VALIDATION
# ============================================================

validation_results = []

for table_name, dataframe in cleaned_tables.items():

    print("\n" + "=" * 70)
    print(f"FINAL VALIDATION: {table_name}")
    print("=" * 70)

    print("Shape:", dataframe.shape)

    print("\nMissing values:")
    print(dataframe.isna().sum())

    duplicate_count = int(dataframe.duplicated().sum())

    print("\nDuplicate full rows:", duplicate_count)

    print("\nData types:")
    print(dataframe.dtypes)

    # Count remaining text whitespace issues
    text_columns = dataframe.select_dtypes(
        include=["object", "string"]
    ).columns

    whitespace_issues = 0

    for column in text_columns:

        values = dataframe[column].dropna().astype(str)

        whitespace_issues += int(
            (
                values.str.strip() != values
            ).sum()
        )

    # Count remaining invalid dates in date-like columns
    date_columns = [
        column
        for column in dataframe.columns
        if (
            "date" in column.lower()
            or "month" in column.lower()
            or "period" in column.lower()
        )
        and not pd.api.types.is_datetime64_any_dtype(
            dataframe[column]
        )
    ]

    invalid_dates = 0

    for column in date_columns:

        converted_dates = pd.to_datetime(
            dataframe[column],
            errors="coerce"
        )

        invalid_dates += int(
            (
                dataframe[column].notna()
                & converted_dates.isna()
            ).sum()
        )

    validation_results.append({
        "Table": table_name,
        "Rows": dataframe.shape[0],
        "Columns": dataframe.shape[1],
        "MissingCells": int(
            dataframe.isna().sum().sum()
        ),
        "DuplicateFullRows": duplicate_count,
        "WhitespaceIssues": whitespace_issues,
        "InvalidDates": invalid_dates
    })


# Save validation summary
validation_df = pd.DataFrame(validation_results)

validation_df.to_csv(
    "NorthStar_Cleaned_Data/data_validation_summary.csv",
    index=False
)

print("\nValidation summary saved.")


#============================================================
# 16. MODULE 3 COMPLETION SUMMARY
# ============================================================

print("\n" + "=" * 80)
print("MODULE 3 — DATA CLEANING COMPLETED")
print("=" * 80)

print("Tables exported:", len(cleaned_tables))
print("Cleaning log entries:", len(cleaning_log))
print(
    "Referential issue records:",
    len(referential_issues_df)
)

print("\nOutput folder: cleaned")

for table_name in cleaned_tables:

    print(f"- cleaned_{table_name}.csv")

print("- data_cleaning_log.csv")
print("- referential_issues.csv")
print("- data_validation_summary.csv")

print("\nReview remaining issues before proceeding to analysis.")