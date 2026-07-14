-- Bronze landing: raw orders from API
CREATE TABLE IF NOT EXISTS bronze.raw_orders (
    order_id STRING,
    customer_id STRING,
    order_total DECIMAL(12, 2),
    status STRING,
    updated_at TIMESTAMP
)
USING PARQUET
LOCATION 's3://retail-lakehouse-dev-bronze/raw_orders/';
