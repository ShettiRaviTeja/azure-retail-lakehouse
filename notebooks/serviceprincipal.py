# Databricks notebook source
# MAGIC %md
# MAGIC ### Service Principal

# COMMAND ----------

app_secret = dbutils.secrets.get("retailscope", "appsecret")

spark.conf.set("fs.azure.account.auth.type.stretaildataplatform.dfs.core.windows.net", "OAuth")
spark.conf.set("fs.azure.account.oauth.provider.type.stretaildataplatform.dfs.core.windows.net", "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
spark.conf.set("fs.azure.account.oauth2.client.id.stretaildataplatform.dfs.core.windows.net", "7bb7f7a2-5a84-47a9-bc34-2796d1da2a2a")
spark.conf.set("fs.azure.account.oauth2.client.secret.stretaildataplatform.dfs.core.windows.net", app_secret)
spark.conf.set("fs.azure.account.oauth2.client.endpoint.stretaildataplatform.dfs.core.windows.net", "https://login.microsoftonline.com/5014c5f0-3a1b-45c9-a0ff-dbff2dbc7fed/oauth2/token")