# Databricks notebook source
# MAGIC %md
# MAGIC # Initialization

# COMMAND ----------

from pyspark.sql import functions as F
from pyspark.sql.window import Window

# COMMAND ----------

# MAGIC %run "/Workspace/azure-retail-platform/notebooks/serviceprincipal"

# COMMAND ----------

PRODUCT_RENAME_MAP = {
    "prd_id": "product_id",
    "cat_id": "category_id",
    "prd_key": "product_key",
    "prd_nm": "product_name",
    "prd_cost": "product_cost",
    "prd_line": "product_line",
    "prd_start_dt": "start_date",
    "prd_end_dt": "end_date"
}

# COMMAND ----------

# MAGIC %md
# MAGIC # Reading from Bronze table

# COMMAND ----------

df = (
    spark.read
         .format("delta")
         .load("abfss://bronze@stretaildataplatform.dfs.core.windows.net/crm_prd_info")
)

# COMMAND ----------

# MAGIC %md
# MAGIC # Transformations

# COMMAND ----------

# MAGIC %md
# MAGIC ## Renaming the Columns

# COMMAND ----------

for old_name, new_name in PRODUCT_RENAME_MAP.items():
    df = df.withColumnRenamed(old_name, new_name)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Extract Category ID

# COMMAND ----------

df = df.withColumn(
    "category_id",
    F.regexp_replace(
        F.substring("product_key", 1, 5),
        "-",
        "_"
    )
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Extract Product Key

# COMMAND ----------

df = df.withColumn(
    "product_key",
    F.substring(
        "product_key",
        7,
        100
    )
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Replace NULL Cost

# COMMAND ----------

df = df.withColumn(
    "product_cost",
    F.coalesce(
        F.col("product_cost"),
        F.lit(0)
    )
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Standardize Product Line

# COMMAND ----------

df = df.withColumn(
    "product_line",
    F.when(
        F.upper(F.trim(F.col("product_line"))) == "R",
        "Road"
    )
    .when(
        F.upper(F.trim(F.col("product_line"))) == "M",
        "Mountains"
    )
    .when(
        F.upper(F.trim(F.col("product_line"))) == "S",
        "Other Sales"
    )
    .when(
        F.upper(F.trim(F.col("product_line"))) == "T",
        "Touring"
    )
    .otherwise("Unknown")
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Convert to Date

# COMMAND ----------

df = df.withColumn(
    "start_date",
    F.to_date("start_date")
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Calculate End Date Using LEAD

# COMMAND ----------

window_spec = Window.partitionBy("product_key") \
                    .orderBy("start_date")

df = df.withColumn(
    "end_date",
    F.lead("start_date")
    .over(window_spec)
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Subtract One Day

# COMMAND ----------

df = df.withColumn(
    "end_date",
    F.date_sub(
        F.col("end_date"),
        1
    )
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Selecting the Columns

# COMMAND ----------

df = df.select(
    "product_id",
    "category_id",
    "product_key",
    "product_name",
    "product_cost",
    "product_line",
    "start_date",
    "end_date"
)

# COMMAND ----------

# MAGIC %md
# MAGIC # Writing into Silver Table

# COMMAND ----------

(
    df.write
    .mode("overwrite")
    .format("delta")
    .save("abfss://silver@stretaildataplatform.dfs.core.windows.net/crm_products")
)