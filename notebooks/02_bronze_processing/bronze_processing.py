# ============================================================
# Bronze Layer Processing
# Project: Retail Sales Data Lakehouse
# Purpose: Convert raw API JSON data into Bronze Delta tables
# ============================================================

from pyspark.sql import functions as F
from pyspark.sql.types import *
from datetime import datetime


# ------------------------------------------------------------
# 1. ADLS Paths
# ------------------------------------------------------------

storage_account = "<YOUR_STORAGE_ACCOUNT>"

landing_base_path = f"abfss://landing@{storage_account}.dfs.core.windows.net"
bronze_base_path = f"abfss://bronze@{storage_account}.dfs.core.windows.net"


# ------------------------------------------------------------
# 2. Customer Data - Read Raw API Data
# ------------------------------------------------------------

customer_landing_path = f"{landing_base_path}/customer"

customer_df = (
    spark.read
    .json(customer_landing_path)
)


# ------------------------------------------------------------
# 3. Add Bronze Metadata
# ------------------------------------------------------------

customer_bronze_df = (
    customer_df
    .withColumn("_source", F.lit("customer_api"))
    .withColumn("_ingestion_timestamp", F.current_timestamp())
    .withColumn("_ingestion_date", F.current_date())
)


# ------------------------------------------------------------
# 4. Write Customer Data to Bronze Delta
# ------------------------------------------------------------

customer_bronze_path = f"{bronze_base_path}/customer"

(
    customer_bronze_df.write
    .format("delta")
    .mode("append")
    .option("mergeSchema", "true")
    .save(customer_bronze_path)
)


print("Customer data successfully written to Bronze.")


# ------------------------------------------------------------
# 5. Sales Data - Read Raw API Data
# ------------------------------------------------------------

sales_landing_path = f"{landing_base_path}/sales"

sales_df = (
    spark.read
    .json(sales_landing_path)
)


# ------------------------------------------------------------
# 6. Add Bronze Metadata
# ------------------------------------------------------------

sales_bronze_df = (
    sales_df
    .withColumn("_source", F.lit("sales_api"))
    .withColumn("_ingestion_timestamp", F.current_timestamp())
    .withColumn("_ingestion_date", F.current_date())
)


# ------------------------------------------------------------
# 7. Write Sales Data to Bronze Delta
# ------------------------------------------------------------

sales_bronze_path = f"{bronze_base_path}/sales"

(
    sales_bronze_df.write
    .format("delta")
    .mode("append")
    .option("mergeSchema", "true")
    .save(sales_bronze_path)
)


print("Sales data successfully written to Bronze.")


# ------------------------------------------------------------
# 8. Verify Bronze Data
# ------------------------------------------------------------

print("Customer Bronze Records:")
display(
    spark.read.format("delta").load(customer_bronze_path)
)


print("Sales Bronze Records:")
display(
    spark.read.format("delta").load(sales_bronze_path)
)