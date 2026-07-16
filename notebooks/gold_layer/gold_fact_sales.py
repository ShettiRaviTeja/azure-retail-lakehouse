# Databricks notebook source
# MAGIC %md
# MAGIC ### Initialization

# COMMAND ----------

# MAGIC %run "/Workspace/azure-retail-platform/notebooks/serviceprincipal"

# COMMAND ----------

# MAGIC %md
# MAGIC ### Reading the files

# COMMAND ----------

crm_sales = (
    spark.read
    .format("delta")
    .load("abfss://silver@stretaildataplatform.dfs.core.windows.net/crm_sales")
)
dim_products = (
    spark.read
    .format("delta")
    .load("abfss://gold@stretaildataplatform.dfs.core.windows.net/dim_products")
)
dim_customers = (
    spark.read
    .format("delta")
    .load("abfss://gold@stretaildataplatform.dfs.core.windows.net/dim_customers")
)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Creating temp views

# COMMAND ----------

crm_sales.createOrReplaceTempView("crm_sales")
dim_products.createOrReplaceTempView("dim_products")
dim_customers.createOrReplaceTempView("dim_customers")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Integration

# COMMAND ----------

query = """
        SELECT 
        order_number,
        dp.product_key,
        dc.customer_key,
        order_date,
        shipping_date,
        due_date,
        sales_amount,
        quantity,
        price 
		FROM crm_sales sd
		LEFT JOIN dim_products dp
		ON sd.product_key = dp.product_number
		LEFT JOIN dim_customers dc
		ON sd.customer_id = dc.customer_id;
"""
df = spark.sql(query)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Writing to gold

# COMMAND ----------

(
    df.write
    .mode("overwrite")
    .format("delta")
    .save("abfss://gold@stretaildataplatform.dfs.core.windows.net/fact_sales")
)