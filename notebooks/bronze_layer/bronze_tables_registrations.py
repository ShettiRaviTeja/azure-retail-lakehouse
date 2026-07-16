# Databricks notebook source
# MAGIC %md
# MAGIC ### Registering the tables

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE adb_retail_data_platform.bronze.crm_cust_info
# MAGIC USING DELTA
# MAGIC LOCATION 'abfss://bronze@stretaildataplatform.dfs.core.windows.net/crm_cust_info';

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE adb_retail_data_platform.bronze.crm_prd_info
# MAGIC USING DELTA
# MAGIC LOCATION 'abfss://bronze@stretaildataplatform.dfs.core.windows.net/crm_prd_info'

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE adb_retail_data_platform.bronze.crm_sales_details
# MAGIC USING DELTA
# MAGIC LOCATION 'abfss://bronze@stretaildataplatform.dfs.core.windows.net/crm_sales_details'

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE adb_retail_data_platform.bronze.erp_cust_az12
# MAGIC USING DELTA
# MAGIC LOCATION 'abfss://bronze@stretaildataplatform.dfs.core.windows.net/erp_cust_az12'

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE adb_retail_data_platform.bronze.erp_loc_a101
# MAGIC USING DELTA
# MAGIC LOCATION 'abfss://bronze@stretaildataplatform.dfs.core.windows.net/erp_loc_a101'

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE adb_retail_data_platform.bronze.erp_px_cat_g1v2
# MAGIC USING DELTA
# MAGIC LOCATION 'abfss://bronze@stretaildataplatform.dfs.core.windows.net/erp_px_cat_g1v2'