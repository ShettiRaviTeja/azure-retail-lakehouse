BASEPATH = "abfss://landing@stretaildataplatform.dfs.core.windows.net"

INGESTION_CONFIG = [
    # CRM
    {
        "path": f"{BASEPATH}/source_crm/cust_info.csv",
        "table": "crm_cust_info"
    },
    {
        "path": f"{BASEPATH}/source_crm/prd_info.csv",
        "table": "crm_prd_info"
    },
    {
        "path": f"{BASEPATH}/source_crm/sales_details.csv",
        "table": "crm_sales_details"
    },

    # ERP
    {
        "path": f"{BASEPATH}/source_erp/CUST_AZ12.csv",
        "table": "erp_cust_az12"
    },
    {
        "path": f"{BASEPATH}/source_erp/LOC_A101.csv",
        "table": "erp_loc_a101"
    },
    {
        "path": f"{BASEPATH}/source_erp/PX_CAT_G1V2.csv",
        "table": "erp_px_cat_g1v2"
    }
]
