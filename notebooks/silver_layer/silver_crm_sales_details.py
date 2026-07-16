# Databricks notebook source
# MAGIC %md
# MAGIC # Initialization

# COMMAND ----------

from pyspark.sql import functions as F

# COMMAND ----------

# MAGIC %run "/Workspace/azure-retail-platform/notebooks/serviceprincipal"

# COMMAND ----------

SALES_RENAME_MAP = {
    "sls_ord_num": "order_number",
    "sls_prd_key": "product_key",
    "sls_cust_id": "customer_id",
    "sls_order_dt": "order_date",
    "sls_ship_dt": "shipping_date",
    "sls_due_dt": "due_date",
    "sls_sales": "sales_amount",
    "sls_quantity": "quantity",
    "sls_price": "price"
}

# COMMAND ----------

# MAGIC %md
# MAGIC # Reading From bronze Table

# COMMAND ----------

df = (
    spark.read
         .format("delta")
         .load("abfss://bronze@stretaildataplatform.dfs.core.windows.net/crm_sales_details")
)

# COMMAND ----------

# MAGIC %md
# MAGIC # Transformations

# COMMAND ----------

# MAGIC %md
# MAGIC ## Renaming the Columns

# COMMAND ----------

for old_name, new_name in SALES_RENAME_MAP.items():
    df = df.withColumnRenamed(old_name, new_name)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Date Conversion

# COMMAND ----------

df = df.withColumn(
    "order_date",
    F.when(
        F.col("order_date").cast("string") == "0",
        None
    ).otherwise(F.col("order_date"))
)

df = df.withColumn(
    "order_date",
    F.when(
        F.length(F.col("order_date").cast("string")) == 8,
        F.to_date(
            F.col("order_date").cast("string"),
            "yyyyMMdd"
        )
    ).otherwise(None)
)

# COMMAND ----------

df = df.withColumn(
    "shipping_date",
    F.when(
        F.col("shipping_date").cast("string") == "0",
        None
    ).otherwise(F.col("shipping_date"))
)

df = df.withColumn(
    "shipping_date",
    F.when(
        F.length(F.col("shipping_date").cast("string")) == 8,
        F.to_date(
            F.col("shipping_date").cast("string"),
            "yyyyMMdd"
        )
    ).otherwise(None)
)

# COMMAND ----------

df = df.withColumn(
    "due_date",
    F.when(
        F.col("due_date").cast("string") == "0",
        None
    ).otherwise(F.col("due_date"))
)

df = df.withColumn(
    "due_date",
    F.when(
        F.length(F.col("due_date").cast("string")) == 8,
        F.to_date(
            F.col("due_date").cast("string"),
            "yyyyMMdd"
        )
    ).otherwise(None)
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Correcting Sales Amount

# COMMAND ----------

df = df.withColumn(
    "sales_amount",
    F.when(
        (F.col("sales_amount").isNull()) |
        (F.col("sales_amount") <= 0) |
        (
            F.col("sales_amount") !=
            F.col("quantity") *
            F.abs(F.col("price"))
        ),
        F.col("quantity") *
        F.abs(F.col("price"))
    )
    .otherwise(F.col("sales_amount"))
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Correcting the Price

# COMMAND ----------

df = df.withColumn(
    "price",
    F.when(
        (F.col("price").isNull()) |
        (F.col("price") <= 0),
        F.col("sales_amount") /
        F.when(
            F.col("quantity") == 0,
            None
        ).otherwise(F.col("quantity"))
    )
    .otherwise(F.col("price"))
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Handling Correct Order Dates

# COMMAND ----------

df = df.withColumn(
    "order_date",
    F.when(
        (F.col("order_date") > F.col("shipping_date")) |
        (F.col("order_date") > F.col("due_date")),
        None
    )
    .otherwise(F.col("order_date"))
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Selecting Columns

# COMMAND ----------

df = df.select(
    "order_number",
    "product_key",
    "customer_id",
    "order_date",
    "shipping_date",
    "due_date",
    "sales_amount",
    "quantity",
    "price"
)

# COMMAND ----------

# MAGIC %md
# MAGIC # Writing into Silver Table

# COMMAND ----------

(
    df.write
    .mode("overwrite")
    .format("delta")
    .save("abfss://silver@stretaildataplatform.dfs.core.windows.net/crm_sales")
)