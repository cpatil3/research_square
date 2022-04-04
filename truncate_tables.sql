-- ----------------Truncate Staging tables ------------
truncate table edw.customer_stg;
truncate table edw.transaction_stg;

-- ----------------Truncate Data Warehouse tables ------------
SET FOREIGN_KEY_CHECKS = 0;
truncate table order_f;
truncate table customer_dim;
truncate table product_dim;
SET FOREIGN_KEY_CHECKS = 1;


