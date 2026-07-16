# Databricks notebook source
# MAGIC %md
# MAGIC ### Initialization

# COMMAND ----------

# MAGIC %run "/Workspace/azure-retail-platform/notebooks/serviceprincipal"

# COMMAND ----------

# MAGIC %md
# MAGIC ### Reading the files

# COMMAND ----------

crm_products = (
    spark.read
    .format('delta')
    .load("abfss://silver@stretaildataplatform.dfs.core.windows.net/crm_products")
)
erp_prd = (
    spark.read
    .format("delta")
    .load("abfss://silver@stretaildataplatform.dfs.core.windows.net/erp_prd_cat")
)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Creating temp views

# COMMAND ----------

crm_products.createOrReplaceTempView("crm_products")
erp_prd.createOrReplaceTempView("erp_prd_cat")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Integrations

# COMMAND ----------

query = """
SELECT 
        ROW_NUMBER() OVER(ORDER BY pri.product_id) AS product_key,
        pri.product_id AS product_id,
        pri.product_key AS product_number,
        pri.product_name AS product_name,
        pri.category_id AS category_id,
        prc.category AS category,
        prc.subcategory AS subcategory,
        prc.maintenance,
        pri.product_cost AS cost,
        pri.product_line AS product_line,
        pri.start_date AS start_date
		FROM crm_products pri
		LEFT JOIN erp_prd_cat prc
		ON pri.category_id = prc.category_id
		WHERE pri.end_date IS NULL;
"""
df = spark.sql(query)

# COMMAND ----------

(
    df.write
    .mode("overwrite")
    .format("delta")
    .save("abfss://gold@stretaildataplatform.dfs.core.windows.net/dim_products")
)