from pyspark.sql import functions as F
from pyspark.sql.window import Window

# Bronze Sales Path
storage_account = "<YOUR_STORAGE_ACCOUNT>"

bronze_path = (
    f"abfss://bronze@{storage_account}.dfs.core.windows.net/sales"
)

silver_path = (
    f"abfss://silver@{storage_account}.dfs.core.windows.net/sales"
)


# Read Bronze Sales
sales_df = (
    spark.read
    .format("delta")
    .load(bronze_path)
)


# Remove invalid records
sales_clean_df = (
    sales_df
    .filter(F.col("sale_id").isNotNull())
    .filter(F.col("customer_id").isNotNull())
)


# Deduplicate using latest ingestion record
window_spec = (
    Window
    .partitionBy("sale_id")
    .orderBy(F.col("_ingestion_timestamp").desc())
)

sales_silver_df = (
    sales_clean_df
    .withColumn("_row_number", F.row_number().over(window_spec))
    .filter(F.col("_row_number") == 1)
    .drop("_row_number")
    .withColumn("product_id", F.trim(F.col("product_id")))
    .withColumn("customer_id", F.trim(F.col("customer_id")))
    .withColumn("quantity", F.col("quantity").cast("integer"))
    .withColumn("amount", F.col("amount").cast("double"))
    .withColumn("_processed_timestamp", F.current_timestamp())
)


# Write Sales Silver
(
    sales_silver_df.write
    .format("delta")
    .mode("overwrite")
    .option("mergeSchema", "true")
    .save(silver_path)
)


print("Sales Silver processing completed.")

display(sales_silver_df)