# Databricks notebook source
# MAGIC %md
# MAGIC # Initialization

# COMMAND ----------

from bronze_config import INGESTION_CONFIG

# COMMAND ----------

# MAGIC %run "/Workspace/azure-retail-platform/notebooks/serviceprincipal"

# COMMAND ----------

# MAGIC %md
# MAGIC # Read from CSV and Write bronze table

# COMMAND ----------

for config in INGESTION_CONFIG:
    df = (
        spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv(config["path"])
    )

    (
        df.write
        .mode("overwrite")
        .format("delta")
        .save(
            f"abfss://bronze@stretaildataplatform.dfs.core.windows.net/{config['table']}"
        )
    )