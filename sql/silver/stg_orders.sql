-- Silver conformed orders
CREATE TABLE IF NOT EXISTS silver.stg_orders (
    order_id STRING,
    customer_id STRING,
    order_total DECIMAL(12, 2),
    status STRING,
    updated_at TIMESTAMP
)
USING DELTA
LOCATION 's3://retail-lakehouse-dev-silver/stg_orders/';
