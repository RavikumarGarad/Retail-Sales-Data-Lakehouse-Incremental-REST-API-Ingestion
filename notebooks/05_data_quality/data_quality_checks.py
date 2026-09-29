# ============================================================
# Data Quality Checks
# Project: Retail Sales Data Lakehouse
# Purpose: Validate Silver and Gold data
# ============================================================

from pyspark.sql import functions as F


# ============================================================
# 1. ADLS PATHS
# ============================================================

storage_account = "<YOUR_STORAGE_ACCOUNT>"

silver_base_path = (
    f"abfss://silver@{storage_account}.dfs.core.windows.net"
)

gold_base_path = (
    f"abfss://gold@{storage_account}.dfs.core.windows.net"
)


# ============================================================
# 2. CUSTOMER SILVER DATA
# ============================================================

customer_path = f"{silver_base_path}/customer"

customer_df = (
    spark.read
    .format("delta")
    .load(customer_path)
)

print("Customer Silver Data Loaded")


# ------------------------------------------------------------
# Customer Record Count
# ------------------------------------------------------------

customer_count = customer_df.count()

print(f"Customer record count: {customer_count}")


# ------------------------------------------------------------
# NULL Customer ID Check
# ------------------------------------------------------------

customer_null_count = (
    customer_df
    .filter(F.col("customer_id").isNull())
    .count()
)

print(f"NULL customer_id records: {customer_null_count}")


# ------------------------------------------------------------
# Duplicate Customer ID Check
# ------------------------------------------------------------

customer_duplicate_count = (
    customer_df
    .groupBy("customer_id")
    .count()
    .filter(F.col("count") > 1)
    .count()
)

print(f"Duplicate customer IDs: {customer_duplicate_count}")


# ============================================================
# 3. SALES SILVER DATA
# ============================================================

sales_path = f"{silver_base_path}/sales"

sales_df = (
    spark.read
    .format("delta")
    .load(sales_path)
)

print("Sales Silver Data Loaded")


# ------------------------------------------------------------
# Sales Record Count
# ------------------------------------------------------------

sales_count = sales_df.count()

print(f"Sales record count: {sales_count}")


# ------------------------------------------------------------
# NULL Sale ID Check
# ------------------------------------------------------------

sales_null_id_count = (
    sales_df
    .filter(F.col("sale_id").isNull())
    .count()
)

print(f"NULL sale_id records: {sales_null_id_count}")


# ------------------------------------------------------------
# Duplicate Sale ID Check
# ------------------------------------------------------------

sales_duplicate_count = (
    sales_df
    .groupBy("sale_id")
    .count()
    .filter(F.col("count") > 1)
    .count()
)

print(f"Duplicate sale IDs: {sales_duplicate_count}")


# ------------------------------------------------------------
# Invalid Quantity Check
# ------------------------------------------------------------

invalid_quantity_count = (
    sales_df
    .filter(
        F.col("quantity").isNull() |
        (F.col("quantity") <= 0)
    )
    .count()
)

print(f"Invalid quantity records: {invalid_quantity_count}")


# ------------------------------------------------------------
# Invalid Amount Check
# ------------------------------------------------------------

invalid_amount_count = (
    sales_df
    .filter(
        F.col("amount").isNull() |
        (F.col("amount") < 0)
    )
    .count()
)

print(f"Invalid amount records: {invalid_amount_count}")


# ============================================================
# 4. GOLD CUSTOMER SALES SUMMARY
# ============================================================

customer_gold_path = (
    f"{gold_base_path}/customer_sales_summary"
)

customer_gold_df = (
    spark.read
    .format("delta")
    .load(customer_gold_path)
)

print("Gold Customer Sales Summary Loaded")


# ------------------------------------------------------------
# Gold Customer ID Check
# ------------------------------------------------------------

gold_null_customer_count = (
    customer_gold_df
    .filter(F.col("customer_id").isNull())
    .count()
)

print(
    f"Gold NULL customer_id records: "
    f"{gold_null_customer_count}"
)


# ------------------------------------------------------------
# Gold Sales Validation
# ------------------------------------------------------------

gold_negative_sales_count = (
    customer_gold_df
    .filter(F.col("total_sales") < 0)
    .count()
)

print(
    f"Gold negative total_sales records: "
    f"{gold_negative_sales_count}"
)


# ============================================================
# 5. FINAL DATA QUALITY RESULT
# ============================================================

quality_checks = {
    "customer_null_id": customer_null_count,
    "customer_duplicates": customer_duplicate_count,
    "sales_null_id": sales_null_id_count,
    "sales_duplicates": sales_duplicate_count,
    "invalid_quantity": invalid_quantity_count,
    "invalid_amount": invalid_amount_count,
    "gold_null_customer_id": gold_null_customer_count,
    "gold_negative_sales": gold_negative_sales_count
}


failed_checks = {
    check: value
    for check, value in quality_checks.items()
    if value > 0
}


# ============================================================
# 6. FINAL STATUS
# ============================================================

print("\n========================================")
print("DATA QUALITY SUMMARY")
print("========================================")

for check, value in quality_checks.items():
    print(f"{check}: {value}")


if len(failed_checks) == 0:

    print("\n========================================")
    print("DATA QUALITY CHECK PASSED")
    print("========================================")

else:

    print("\n========================================")
    print("DATA QUALITY CHECK FAILED")
    print("========================================")

    print("\nFailed checks:")

    for check, value in failed_checks.items():
        print(f"- {check}: {value}")