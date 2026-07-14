-- Gold daily order metrics
CREATE TABLE IF NOT EXISTS gold.fct_daily_orders (
    order_date DATE,
    order_count BIGINT,
    revenue_total DECIMAL(14, 2)
)
USING DELTA
LOCATION 's3://retail-lakehouse-dev-gold/fct_daily_orders/';
