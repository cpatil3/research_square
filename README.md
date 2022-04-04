# RESEARCH_SQURE
Assignment

## Tech & Tools:
- Python
- MySQL DB Server
- MySQL Workbench

## Tasks Description:
- Read "customer.csv" file having customer info from legacy system.
- Read "transactions.json" with transaction data from API
- Run ingestion process to load customer and transactions data to Staging tables for raw data from source.
- Run dataflow process to load customer, product and order info to Data Warehouse tables.
- Run SQL’s on Data Warehouse tables for required analytics.

## Steps To Follow:
1) Download the "customer.csv" and "transactions.json" files to local directory where all the source codes will be located.
2) Create **“edw”** database schema on MySQL db.
3) Create staging and Data Warehouse tables by running the **“create_tables.sql”** on MySQL workbench after connecting to “edw” schema.
4) The Database connection details and login credentials needs to be updated in **“config.json”** file and save it to local directory where all the source codes will be located.
5) Run the **customer_ingestion.py”** script for ingesting customer csv data to **customer_stg** table.
6) Run the **“transaction_ingestion.py”** script for ingesting transaction json data to **transaction_stg** table.
7) Run the **“edw_dataflow.py”** script for loading data from customer_stg and transaction_stg to data warehouse tables **customer_dim, product_dim & order_f**.
8) Run the required analytics SQL’s on Data Warehouse tables customer_dim, product_dim and order_f on MySQL workbench.
9) If tables need to be truncated, then run **“truncate_tables.sql”** on MySQL.

## Notes:
- The transaction_stg staging table is in de-normalized form so that process for raw data dumping can be easier.
- Data Warehouse tables are normalized and modeled using Star Schema where customer_dim, product_dim are dimensions and order_f is a fact table.
- Schema and all tables structures, columns, indexes and foreign key definitions are all included in “edw” schema model files **“edw_model.pdf”** and **“edw_model.mwb”**. The details are also in **“create_tables.sql”** script.
- The output of SQL for getting Average monthly sales by city is in **“final_output.csv”** file. The related sql is in **“Avg_mnthl_sales.sql”**.
