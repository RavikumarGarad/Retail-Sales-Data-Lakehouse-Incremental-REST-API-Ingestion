-- ============================================================
-- Gold Layer Tables
-- Project: Retail Sales Data Lakehouse
-- Purpose: Create business-ready Gold Delta tables
-- ============================================================


-- ============================================================
-- 1. Customer Sales Summary
-- ============================================================

CREATE TABLE IF NOT EXISTS customer_sales_summary
(
    customer_id             STRING,
    customer_name           STRING,
    email                   STRING,
    city                    STRING,
    country                 STRING,
    total_orders            BIGINT,
    total_quantity          BIGINT,
    total_sales             DOUBLE,
    average_order_value     DOUBLE,
    _gold_processed_timestamp TIMESTAMP
)
USING DELTA;


-- ============================================================
-- 2. Overall Sales Summary
-- ============================================================

CREATE TABLE IF NOT EXISTS sales_summary
(
    total_orders            BIGINT,
    total_quantity_sold     BIGINT,
    total_sales             DOUBLE,
    average_order_value     DOUBLE,
    _gold_processed_timestamp TIMESTAMP
)
USING DELTA;


-- ============================================================
-- 3. Verify Gold Tables
-- ============================================================

SHOW TABLES;


-- ============================================================
-- 4. Check Customer Sales Summary Structure
-- ============================================================

DESCRIBE customer_sales_summary;


-- ============================================================
-- 5. Check Sales Summary Structure
-- ============================================================

DESCRIBE sales_summary;