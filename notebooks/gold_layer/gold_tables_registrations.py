# Databricks notebook source
# MAGIC %md
# MAGIC ### Registering the tables

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE adb_retail_data_platform.gold.dim_customers
# MAGIC USING DELTA
# MAGIC LOCATION 'abfss://gold@stretaildataplatform.dfs.core.windows.net/dim_customers'

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE adb_retail_data_platform.gold.dim_products
# MAGIC USING DELTA
# MAGIC LOCATION 'abfss://gold@stretaildataplatform.dfs.core.windows.net/dim_products'

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE adb_retail_data_platform.gold.fact_sales
# MAGIC USING DELTA
# MAGIC LOCATION 'abfss://gold@stretaildataplatform.dfs.core.windows.net/fact_sales'