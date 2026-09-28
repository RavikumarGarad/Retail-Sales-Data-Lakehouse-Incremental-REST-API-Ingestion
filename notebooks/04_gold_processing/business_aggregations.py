# ============================================================
# Gold Layer Processing
# Project: Retail Sales Data Lakehouse
# Purpose: Create business-ready aggregated data
# ============================================================

from pyspark.sql import functions as F


# ------------------------------------------------------------
# 1. ADLS Paths
# ------------------------------------------------------------

storage_account = "<YOUR_STORAGE_ACCOUNT>"

silver_base_path = (
    f"abfss://silver@{storage_account}.dfs.core.windows.net"
)

gold_base_path = (
    f"abfss://gold@{storage_account}.dfs.core.windows.net"
)


# ============================================================
# 2. Read Silver Customer Data
# ============================================================

customer_path = f"{silver_base_path}/customer"

customer_df = (
    spark.read
    .format("delta")
    .load(customer_path)
)


# ============================================================
# 3. Read Silver Sales Data
# ============================================================

sales_path = f"{silver_base_path}/sales"

sales_df = (
    spark.read
    .format("delta")
    .load(sales_path)
)


# ============================================================
# 4. Customer Sales Summary
# ============================================================

customer_sales_df = (
    sales_df
    .groupBy("customer_id")
    .agg(
        F.countDistinct("sale_id").alias("total_orders"),
        F.sum("quantity").alias("total_quantity"),
        F.sum("amount").alias("total_sales"),
        F.avg("amount").alias("average_order_value")
    )
)


# ============================================================
# 5. Join Customer Information
# ============================================================

customer_gold_df = (
    customer_df.alias("c")
    .join(
        customer_sales_df.alias("s"),
        F.col("c.customer_id") == F.col("s.customer_id"),
        "left"
    )
    .select(
        F.col("c.customer_id"),
        F.col("c.customer_name"),
        F.col("c.email"),
        F.col("c.city"),
        F.col("c.country"),
        F.coalesce(F.col("s.total_orders"), F.lit(0)).alias("total_orders"),
        F.coalesce(F.col("s.total_quantity"), F.lit(0)).alias("total_quantity"),
        F.coalesce(F.col("s.total_sales"), F.lit(0)).alias("total_sales"),
        F.coalesce(
            F.col("s.average_order_value"),
            F.lit(0)
        ).alias("average_order_value"),
        F.current_timestamp().alias("_gold_processed_timestamp")
    )
)


# ============================================================
# 6. Write Customer Gold Table
# ============================================================

customer_gold_path = f"{gold_base_path}/customer_sales_summary"

(
    customer_gold_df.write
    .format("delta")
    .mode("overwrite")
    .option("mergeSchema", "true")
    .save(customer_gold_path)
)


print("Customer Sales Gold table created.")


# ============================================================
# 7. Overall Sales Summary
# ============================================================

sales_summary_df = (
    sales_df
    .agg(
        F.countDistinct("sale_id").alias("total_orders"),
        F.sum("quantity").alias("total_quantity_sold"),
        F.sum("amount").alias("total_sales"),
        F.avg("amount").alias("average_order_value")
    )
    .withColumn(
        "_gold_processed_timestamp",
        F.current_timestamp()
    )
)


# ============================================================
# 8. Write Sales Summary
# ============================================================

sales_summary_path = f"{gold_base_path}/sales_summary"

(
    sales_summary_df.write
    .format("delta")
    .mode("overwrite")
    .option("mergeSchema", "true")
    .save(sales_summary_path)
)


print("Sales Summary Gold table created.")


# ============================================================
# 9. Validate Gold Tables
# ============================================================

print("Customer Sales Summary:")
display(
    spark.read
    .format("delta")
    .load(customer_gold_path)
)


print("Overall Sales Summary:")
display(
    spark.read
    .format("delta")
    .load(sales_summary_path)
)