# Databricks notebook source
# MAGIC %md
# MAGIC # Initialization

# COMMAND ----------

# MAGIC %run "/Workspace/azure-retail-platform/notebooks/serviceprincipal"

# COMMAND ----------

ERP_PRODUCT_CATEGORY_RENAME_MAP = {
    "id": "category_id",
    "cat": "category",
    "subcat": "subcategory",
    "maintenance": "maintenance"
}

# COMMAND ----------

# MAGIC %md
# MAGIC # Reading from bronze table

# COMMAND ----------

df = (
    spark.read
            .format("delta")
            .load("abfss://bronze@stretaildataplatform.dfs.core.windows.net/erp_px_cat_g1v2")
)

# COMMAND ----------

# MAGIC %md
# MAGIC # Transformations

# COMMAND ----------

# MAGIC %md
# MAGIC ## Renaming columns

# COMMAND ----------

for old_name, new_name in ERP_PRODUCT_CATEGORY_RENAME_MAP.items():
    df = df.withColumnRenamed(old_name, new_name)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Selecting the columns

# COMMAND ----------

df = df.select(
    "category_id",
    "category",
    "subcategory",
    "maintenance"
)

# COMMAND ----------

# MAGIC %md
# MAGIC # Writing to Silver Table

# COMMAND ----------

(
    df.write
    .mode("overwrite")
    .format("delta")
    .save("abfss://silver@stretaildataplatform.dfs.core.windows.net/erp_prd_cat")
)