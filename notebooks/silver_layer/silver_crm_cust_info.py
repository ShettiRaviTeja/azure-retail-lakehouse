# Databricks notebook source
# MAGIC %md
# MAGIC # Initialization

# COMMAND ----------

import pyspark.sql.functions as F
from pyspark.sql.types import StringType

# COMMAND ----------

# MAGIC %run "/Workspace/azure-retail-platform/notebooks/serviceprincipal"

# COMMAND ----------

RENAME_MAP = {
    "cst_id" : "customer_id",
    "cst_key" : "customer_key",
    "cst_firstname" : "first_name",
    "cst_lastname" : "last_name",
    "cst_marital_status" : "marital_status",
    "cst_gndr" : "gender",
    "cst_create_date" : "created_date"
}

# COMMAND ----------

# MAGIC %md
# MAGIC # Reading from bronze tables

# COMMAND ----------

df = (
    spark.read
         .format("delta")
         .load("abfss://bronze@stretaildataplatform.dfs.core.windows.net/crm_cust_info")
)

# COMMAND ----------

# MAGIC %md
# MAGIC # Transformations

# COMMAND ----------

# MAGIC %md
# MAGIC ## Trimming the Values

# COMMAND ----------

for field in df.schema.fields:
    if isinstance(field.dataType, StringType):
        df = df.withColumn(field.name, F.trim(F.col(field.name)))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Normalization

# COMMAND ----------

df = (
    df
    .withColumn(
        "cst_marital_status",
        F.when(F.upper(F.col("cst_marital_status")) == "S", "Single")
        .when(F.upper(F.col("cst_marital_status")) == "M", "Married")
        .otherwise("n/a")
    )
    .withColumn(
        "cst_gndr",
        F.when(F.upper(F.col("cst_gndr")) == "M", "Male")
        .when(F.upper(F.col("cst_gndr")) == "F", "Female")
        .otherwise("n/a")
    )
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Renaming the columns

# COMMAND ----------

for old_name, new_name in RENAME_MAP.items():
    df = df.withColumnRenamed(old_name, new_name)

# COMMAND ----------

# MAGIC %md
# MAGIC # Write to Silver Tables

# COMMAND ----------

(
    df.write
    .mode("overwrite")
    .format("delta")
    .save("abfss://silver@stretaildataplatform.dfs.core.windows.net/crm_customers")
)