# Databricks notebook source
# MAGIC %md
# MAGIC # Initialization

# COMMAND ----------

import pyspark.sql.functions as F

# COMMAND ----------

# MAGIC %run "/Workspace/azure-retail-platform/notebooks/serviceprincipal"

# COMMAND ----------

ERP_LOCATION_RENAME_MAP = {
    "cid": "customer_id",
    "cntry": "country"
}

# COMMAND ----------

# MAGIC %md
# MAGIC # Reading from bronze table

# COMMAND ----------

df = (
    spark.read
    .format("delta")
    .load("abfss://bronze@stretaildataplatform.dfs.core.windows.net/erp_loc_a101")
)

# COMMAND ----------

# MAGIC %md
# MAGIC # Transformations

# COMMAND ----------

# MAGIC %md
# MAGIC ## Renaming the columns

# COMMAND ----------

for old_name, new_name in ERP_LOCATION_RENAME_MAP.items():
    df = df.withColumnRenamed(old_name, new_name)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Removing '-' symbol

# COMMAND ----------

df = df.withColumn(
    "customer_id",
    F.regexp_replace(
        F.col("customer_id"),
        "-",
        ""
    )
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Country Standardization

# COMMAND ----------

df = df.withColumn(
    "country",
    F.when(
        F.upper(F.trim(F.col("country"))).isin("US", "USA", "UNITED STATES"),
        "United States"
    )
    .when(
        F.upper(F.trim(F.col("country"))).isin("DE", "GERMANY"),
        "Germany"
    )
    .when(
        (F.trim(F.col("country")) == "") |
        (F.col("country").isNull()),
        "Unknown"
    )
    .otherwise(
        F.trim(F.col("country"))
    )
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Selecting the columns

# COMMAND ----------

df = df.select(
    "customer_id",
    "country"
)

# COMMAND ----------

# MAGIC %md
# MAGIC # Writing into Silver table

# COMMAND ----------

(
    df.write
    .mode("overwrite")
    .format("delta")
    .save("abfss://silver@stretaildataplatform.dfs.core.windows.net/erp_cust_loc")
)