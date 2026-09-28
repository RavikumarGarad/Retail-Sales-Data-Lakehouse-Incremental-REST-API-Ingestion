from pyspark.sql import functions as F

# Bronze Customer Path
storage_account = "<YOUR_STORAGE_ACCOUNT>"

bronze_path = (
    f"abfss://bronze@{storage_account}.dfs.core.windows.net/customer"
)

silver_path = (
    f"abfss://silver@{storage_account}.dfs.core.windows.net/customer"
)


# Read Bronze Customer
customer_df = (
    spark.read
    .format("delta")
    .load(bronze_path)
)


# Clean and standardize Customer data
customer_silver_df = (
    customer_df
    .filter(F.col("customer_id").isNotNull())
    .dropDuplicates(["customer_id"])
    .withColumn("customer_name", F.trim(F.col("customer_name")))
    .withColumn("email", F.lower(F.trim(F.col("email"))))
    .withColumn("city", F.trim(F.col("city")))
    .withColumn("country", F.trim(F.col("country")))
    .withColumn("_processed_timestamp", F.current_timestamp())
)


# Write Customer Silver
(
    customer_silver_df.write
    .format("delta")
    .mode("overwrite")
    .option("mergeSchema", "true")
    .save(silver_path)
)


print("Customer Silver processing completed.")

display(customer_silver_df)