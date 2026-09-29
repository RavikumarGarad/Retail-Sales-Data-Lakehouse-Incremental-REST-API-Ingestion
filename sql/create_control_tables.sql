-- ============================================================
-- Control Tables
-- Project: Retail Sales Data Lakehouse
-- Purpose: Manage incremental API ingestion
-- ============================================================


-- ============================================================
-- 1. Create Control Table
-- ============================================================

CREATE TABLE IF NOT EXISTS ingestion_control
(
    ConfigId        INT,
    Source          STRING,
    SourceSchema    STRING,
    SourceTable     STRING,
    TargetPath      STRING,
    WatermarkColumn STRING,
    LastWatermark   TIMESTAMP,
    CriticalColumns STRING,
    IsActive        BOOLEAN
)
USING DELTA;


-- ============================================================
-- 2. Insert Customer Configuration
-- ============================================================

INSERT INTO ingestion_control
VALUES
(
    1,
    'customer_api',
    'api',
    'customer',
    'bronze/customer',
    'updated_at',
    TIMESTAMP '1900-01-01 00:00:00',
    'customer_id',
    TRUE
);


-- ============================================================
-- 3. Insert Sales Configuration
-- ============================================================

INSERT INTO ingestion_control
VALUES
(
    2,
    'sales_api',
    'api',
    'sales',
    'bronze/sales',
    'updated_at',
    TIMESTAMP '1900-01-01 00:00:00',
    'sale_id,customer_id',
    TRUE
);


-- ============================================================
-- 4. Verify Control Table
-- ============================================================

SELECT *
FROM ingestion_control
ORDER BY ConfigId;