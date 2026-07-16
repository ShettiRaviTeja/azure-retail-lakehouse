# Databricks notebook source
# MAGIC %md
# MAGIC ### Registering the tables

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE adb_retail_data_platform.silver.crm_customers
# MAGIC USING DELTA
# MAGIC LOCATION 'abfss://silver@stretaildataplatform.dfs.core.windows.net/crm_customers'

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE adb_retail_data_platform.silver.crm_products
# MAGIC USING DELTA
# MAGIC LOCATION 'abfss://silver@stretaildataplatform.dfs.core.windows.net/crm_products'

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE adb_retail_data_platform.silver.crm_sales
# MAGIC USING DELTA
# MAGIC LOCATION 'abfss://silver@stretaildataplatform.dfs.core.windows.net/crm_sales'

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE adb_retail_data_platform.silver.erp_cust_details
# MAGIC USING DELTA
# MAGIC LOCATION 'abfss://silver@stretaildataplatform.dfs.core.windows.net/erp_cust_details'

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE adb_retail_data_platform.silver.erp_cust_loc
# MAGIC USING DELTA
# MAGIC LOCATION 'abfss://silver@stretaildataplatform.dfs.core.windows.net/erp_cust_loc'

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE adb_retail_data_platform.silver.erp_prd_cat
# MAGIC USING DELTA
# MAGIC LOCATION 'abfss://silver@stretaildataplatform.dfs.core.windows.net/erp_prd_cat'