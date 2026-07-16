# Databricks notebook source
# MAGIC %md
# MAGIC # Initialization

# COMMAND ----------

# MAGIC %run "/Workspace/azure-retail-platform/notebooks/serviceprincipal"

# COMMAND ----------

# MAGIC %md
# MAGIC ### Reading the files

# COMMAND ----------

crm_customers = spark.read.format("delta").load(
    "abfss://silver@stretaildataplatform.dfs.core.windows.net/crm_customers"
)

erp_customers_info = spark.read.format("delta").load(
    "abfss://silver@stretaildataplatform.dfs.core.windows.net/erp_cust_details"
)

erp_locations = spark.read.format("delta").load(
    "abfss://silver@stretaildataplatform.dfs.core.windows.net/erp_cust_loc"
)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Creating temp views

# COMMAND ----------

crm_customers.createOrReplaceTempView("crm_customers")
erp_customers_info.createOrReplaceTempView("erp_customers_info")
erp_locations.createOrReplaceTempView("erp_locations")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Integrations

# COMMAND ----------

query = """
		SELECT 
            ROW_NUMBER() OVER(ORDER BY ci.customer_id) AS customer_key,
			ci.customer_id AS customer_id,
			ci.customer_key AS customer_number,
			ci.first_name AS first_name,
			ci.last_name AS last_name,
			cl.country AS country,
			ci.marital_status AS marital_status,
			CASE 
				WHEN ci.gender <> 'Unknown' THEN ci.gender
				ELSE COALESCE(ca.gender, 'Unknown')
			END AS gender,
			ca.birth_date AS birthdate,
			ci.created_date AS created_date
		FROM crm_customers ci
		LEFT JOIN erp_customers_info ca
		ON ci.customer_key = ca.customer_id
		LEFT JOIN erp_locations cl
		ON ci.customer_key = cl.customer_id;
"""
df = spark.sql(query)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Writing to gold container

# COMMAND ----------

(
    df.write
    .mode("overwrite")
    .format("delta")
    .save("abfss://gold@stretaildataplatform.dfs.core.windows.net/dim_customers")
)