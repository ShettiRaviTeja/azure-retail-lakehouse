# Databricks notebook source
# MAGIC %md
# MAGIC # Initialization

# COMMAND ----------

import pyspark.sql.functions as F

# COMMAND ----------

# MAGIC %run "/Workspace/azure-retail-platform/notebooks/serviceprincipal"

# COMMAND ----------

ERP_CUSTOMER_RENAME_MAP = {
    "cid": "customer_id",
    "bdate": "birth_date",
    "gen": "gender"
}

# COMMAND ----------

# MAGIC %md
# MAGIC # Reading From bronze table

# COMMAND ----------

df = (
    spark.read
        .format('delta')
        .load("abfss://bronze@stretaildataplatform.dfs.core.windows.net/erp_cust_az12")
)

# COMMAND ----------

# MAGIC %md
# MAGIC # Transformations

# COMMAND ----------

# MAGIC %md
# MAGIC ## Renaming columns

# COMMAND ----------

for old_name, new_name in ERP_CUSTOMER_RENAME_MAP.items():
    df = df.withColumnRenamed(old_name, new_name)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Remove the prefix "NAS"

# COMMAND ----------

df = df.withColumn(
    "customer_id",
    F.when(
        F.col("customer_id").startswith("NAS"),
        F.substring("customer_id", 4, 100)
    )
    .otherwise(F.col("customer_id"))
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Birth Date Validation

# COMMAND ----------

df = df.withColumn(
    "birth_date",
    F.when(
        F.col("birth_date") > F.current_date(),
        None
    )
    .otherwise(F.col("birth_date"))
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Gender Standardization

# COMMAND ----------

df = df.withColumn(
    "gender",
    F.when(
        F.upper(F.trim(F.col("gender"))).isin("M", "MALE"),
        "Male"
    )
    .when(
        F.upper(F.trim(F.col("gender"))).isin("F", "FEMALE"),
        "Female"
    )
    .otherwise("Unknown")
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Selecting Final Columns

# COMMAND ----------

df = df.select(
    "customer_id",
    "birth_date",
    "gender"
)

# COMMAND ----------

# MAGIC %md
# MAGIC # Writing into Silver table

# COMMAND ----------

(
    df.write
    .mode("overwrite")
    .format("delta")
    .save("abfss://silver@stretaildataplatform.dfs.core.windows.net/erp_cust_details")
)