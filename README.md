# 🚀 Azure Retail Data Platform

> An end-to-end Azure Data Engineering project implementing a modern Lakehouse Architecture using **Azure Databricks, PySpark, Delta Lake, Unity Catalog, and Azure Data Lake Storage Gen2 (ADLS Gen2).**

---

## 📌 Overview

This project demonstrates the implementation of a scalable Azure Lakehouse that ingests CRM and ERP datasets, transforms them through the **Medallion Architecture (Landing → Bronze → Silver → Gold)**, and delivers analytics-ready data while implementing enterprise-grade governance using **Unity Catalog**.

---

## 🏗️ Architecture

<p align="center">
  <img src="docs/azure_lakehouse_diagram.png" width="100%" alt="Azure Retail Data Platform Architecture">
</p>

---

## ⚙️ Tech Stack

| Category | Technologies |
|----------|--------------|
| ☁️ **Cloud Platform** | Microsoft Azure |
| ⚡ **Compute & Processing** | Azure Databricks, Apache Spark (PySpark) |
| 💻 **Programming Languages** | Python, SQL |
| 💾 **Storage & Data Format** | Azure Data Lake Storage Gen2 (ADLS Gen2), Delta Lake |
| 🛡️ **Data Governance & Security** | Unity Catalog, Azure Managed Identity, Azure Access Connector, Storage Credential, External Location |
| 🌿 **Version Control** | Git, GitHub |

---

## 📂 Project Structure

```text
azure-retail-data-platform
│
├── notebooks
│   ├── bronze_layer
│   ├── silver_layer
│   ├── gold_layer
│   └── serviceprincipal
│
├── datasets
│   ├── source_crm
│   │   ├── cust_info.csv
│   │   ├── prd_info.csv
│   │   └── sales_details.csv
│   │
│   └── source_erp
│       ├── CUST_AZ12.csv
│       ├── LOC_A101.csv
│       └── PX_CAT_G1V2.csv
│
├── docs
│   └── azure_lakehouse_architecture.png
│
├── README.md
└── LICENSE
```

---

## 🏛️ Medallion Architecture

| Layer | Purpose |
|--------|---------|
| 📥 **Landing** | Stores raw CRM & ERP source files in ADLS Gen2 |
| 🥉 **Bronze** | Ingests raw data into External Delta Tables |
| 🥈 **Silver** | Cleanses, validates, and standardizes data |
| 🥇 **Gold** | Builds business-ready dimensional models for analytics |

---

## ✨ Key Features

- End-to-End Azure Data Engineering Pipeline
- Medallion Architecture (Landing → Bronze → Silver → Gold)
- Batch ETL Pipeline using PySpark
- Delta Lake for ACID-compliant storage
- Unity Catalog for centralized data governance
- External Delta Tables
- Secure ADLS access using Managed Identity
- Enterprise authentication using Azure Access Connector
- Storage Credentials & External Locations
- Modular and reusable notebook design

---

## 🔐 Security & Governance

This project follows enterprise security best practices by implementing:

- Azure Managed Identity
- Azure Access Connector
- Unity Catalog
- Storage Credentials
- External Locations
- External Delta Tables
- Fine-grained data governance

---

## 🚀 Future Enhancements

- Auto Loader
- Incremental Data Loading
- Structured Streaming
- Delta Live Tables (DLT)
- Databricks Workflows
- Azure Data Factory Integration
- Power BI Dashboard

---

## 👨‍💻 Author

**Ravi Teja**

Aspiring Data Engineer passionate about building scalable cloud-native data platforms using Azure, Databricks, and PySpark.

---

⭐ **If you found this project useful, consider giving it a star!**
