# Naming Conventions

## Overview

Consistent naming conventions are critical for maintainability, discoverability, and collaboration in a data platform. This document defines standards for naming resources in Microsoft Fabric.

## General Principles

1. **Descriptive**: Names should clearly indicate purpose
2. **Consistent**: Follow patterns across all resources
3. **Concise**: Keep names short but meaningful
4. **Lowercase**: Use lowercase with separators
5. **No Spaces**: Use underscores or hyphens
6. **Avoid Abbreviations**: Unless widely understood
7. **Include Context**: Layer, domain, purpose

## Separator Standards

| Context | Separator | Example |
|---------|-----------|---------|
| Files/Tables | Underscore `_` | `customer_orders` |
| Folders | Forward slash `/` | `bronze/sales/` |
| Workspace | Hyphen `-` | `data-platform-prod` |
| Variable/Column | Snake case | `order_total_amount` |

## Workspace Naming

### Pattern
```
<platform>-<environment>-<purpose>
```

### Examples
```
fabric-prod-lakehouse
fabric-dev-analytics
fabric-test-dataeng
```

### Environments
- `dev` - Development
- `test` - Testing/QA
- `uat` - User Acceptance Testing
- `prod` - Production

## Lakehouse Naming

### Pattern
```
lh_<domain>_<environment>
```

### Examples
```
lh_sales_prod
lh_finance_dev
lh_customer_prod
```

## Folder Structure Naming

### Bronze Layer
```
bronze/<source_system>/<domain>/<entity>/<year>/<month>/<day>
```

**Examples:**
```
bronze/sap/sales/orders/2024/01/15
bronze/salesforce/crm/accounts/2024/01/15
bronze/api/weather/forecasts/2024/01/15
```

### Silver Layer
```
silver/<domain>/<entity>
```

**Examples:**
```
silver/sales/orders
silver/customer/accounts
silver/inventory/products
```

### Gold Layer
```
gold/<business_domain>/<purpose>
```

**Examples:**
```
gold/analytics/sales_summary
gold/reporting/monthly_metrics
gold/ml_features/customer_churn
```

## Table Naming

### Pattern
```
<layer>_<domain>_<entity>_<optional_descriptor>
```

### Bronze Tables
```
bronze_<source>_<entity>_raw
```

**Examples:**
```
bronze_sap_orders_raw
bronze_crm_customers_raw
bronze_api_weather_raw
```

### Silver Tables
```
silver_<domain>_<entity>
```

**Examples:**
```
silver_sales_orders
silver_customer_accounts
silver_inventory_products
silver_hr_employees
```

### Gold Tables
```
gold_<purpose>_<entity>
```

**Examples:**
```
gold_analytics_sales_summary
gold_reporting_daily_metrics
gold_ml_customer_features
gold_exec_dashboard_kpis
```

### Fact Tables
```
fact_<business_process>
```

**Examples:**
```
fact_sales
fact_orders
fact_transactions
```

### Dimension Tables
```
dim_<entity>
```

**Examples:**
```
dim_customer
dim_product
dim_date
dim_geography
```

### Bridge Tables
```
bridge_<entity1>_<entity2>
```

**Examples:**
```
bridge_product_category
bridge_customer_account
```

## Column Naming

### General Rules
- Use snake_case: `customer_id`, `order_total`
- Be descriptive: `order_creation_date` not `ord_dt`
- Use standard suffixes

### Standard Suffixes

| Suffix | Meaning | Example |
|--------|---------|---------|
| `_id` | Identifier | `customer_id`, `order_id` |
| `_key` | Surrogate key | `customer_key`, `date_key` |
| `_sk` | Surrogate key (alt) | `customer_sk` |
| `_date` | Date only | `order_date`, `birth_date` |
| `_datetime` | Date with time | `created_datetime` |
| `_timestamp` | Unix timestamp | `ingestion_timestamp` |
| `_amount` | Money value | `order_amount`, `total_amount` |
| `_qty` | Quantity | `order_qty`, `stock_qty` |
| `_pct` | Percentage | `discount_pct`, `tax_pct` |
| `_flag` | Boolean | `is_active_flag`, `deleted_flag` |
| `_ind` | Indicator (alt) | `is_active_ind` |
| `_code` | Code value | `country_code`, `status_code` |
| `_name` | Name | `customer_name`, `product_name` |
| `_desc` | Description | `product_desc`, `category_desc` |
| `_count` | Count | `order_count`, `customer_count` |

### Standard Audit Columns

All tables should include:
```
created_at         # When record was created
created_by         # Who created the record
updated_at         # When record was last updated
updated_by         # Who last updated the record
is_active          # Soft delete flag
_metadata          # Additional metadata (optional)
```

### Data Lineage Columns

For Bronze/Silver tables:
```
source_system       # Origin system
source_file         # Source file name
ingestion_timestamp # When data was ingested
batch_id            # Batch identifier
```

## Pipeline Naming

### Pattern
```
<layer>_<action>_<domain>_<entity>
```

### Examples
```
bronze_ingest_sales_orders
silver_transform_customer_accounts
gold_aggregate_sales_summary
```

### Pipeline Types
- `ingest` - Data ingestion
- `transform` - Data transformation
- `aggregate` - Data aggregation
- `validate` - Data validation
- `export` - Data export

## Notebook Naming

### Pattern
```
<layer>_<purpose>_<entity>
```

### Examples
```
bronze_load_sap_orders
silver_cleanse_customer_data
gold_build_sales_features
util_data_quality_checks
```

### Notebook Prefixes
- `bronze_` - Bronze layer processing
- `silver_` - Silver layer processing
- `gold_` - Gold layer processing
- `util_` - Utility/helper notebooks
- `test_` - Testing notebooks
- `explore_` - Data exploration notebooks

## Data Factory Naming

### Pipelines
```
pl_<layer>_<action>_<entity>
```

**Examples:**
```
pl_bronze_ingest_orders
pl_silver_transform_customers
pl_gold_aggregate_sales
```

### Datasets
```
ds_<source>_<entity>
```

**Examples:**
```
ds_sap_orders
ds_salesforce_accounts
ds_onelake_customers
```

### Linked Services
```
ls_<service_type>_<name>
```

**Examples:**
```
ls_sql_adventureworks
ls_adls_datalake
ls_keyvault_secrets
```

### Activities
```
act_<action>_<target>
```

**Examples:**
```
act_copy_orders
act_transform_customers
act_validate_data
```

## Power BI Naming

### Semantic Models (Datasets)
```
sm_<domain>_<purpose>
```

**Examples:**
```
sm_sales_analytics
sm_finance_reporting
sm_hr_dashboard
```

### Reports
```
rpt_<domain>_<purpose>
```

**Examples:**
```
rpt_sales_executive_dashboard
rpt_finance_monthly_review
rpt_operations_daily_metrics
```

### Dataflows
```
df_<layer>_<entity>
```

**Examples:**
```
df_silver_customers
df_gold_sales_summary
```

## File Naming

### Data Files
```
<entity>_<date>_<sequence>.<extension>
```

**Examples:**
```
orders_20240115_001.parquet
customers_20240115_001.csv
transactions_20240115_001.json
```

### Configuration Files
```
config_<environment>_<purpose>.<extension>
```

**Examples:**
```
config_prod_pipelines.json
config_dev_connections.yaml
config_test_settings.json
```

### Script Files
```
<action>_<entity>.<extension>
```

**Examples:**
```
deploy_lakehouse.ps1
setup_permissions.sh
validate_schema.py
```

## Variable Naming (Code)

### Python/PySpark
```python
# Variables: snake_case
customer_id = 123
order_total_amount = 100.50

# Functions: snake_case
def calculate_order_total(items):
    pass

# Classes: PascalCase
class CustomerOrder:
    pass

# Constants: UPPER_SNAKE_CASE
MAX_RETRY_COUNT = 3
DEFAULT_TIMEOUT = 30
```

### SQL
```sql
-- Variables: snake_case with @ prefix
@customer_id = 123
@start_date = '2024-01-01'

-- Tables: snake_case
FROM silver_sales_orders

-- Aliases: Short, lowercase
SELECT o.order_id, c.customer_name
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
```

## Environment Specific Suffixes

Add environment suffix when needed:
```
resource_name_dev
resource_name_test
resource_name_prod
```

**Examples:**
```
lh_sales_dev
config_prod_pipelines.json
sm_sales_analytics_test
```

## Special Cases

### Temporary Objects
Prefix with `temp_` or `tmp_`:
```
temp_staging_data
tmp_calculation_results
```

### Archive/Historical Data
Use `archive_` or `hist_` prefix:
```
archive_orders_2023
hist_customer_changes
```

### Backup Files
Use `backup_` or `bak_` prefix with timestamp:
```
backup_20240115_customer_data
bak_20240115_sales_orders
```

## Anti-Patterns (Avoid)

❌ **Don't Use:**
- Spaces in names: `customer orders`
- Special characters: `customer$orders`, `data@warehouse`
- Inconsistent casing: `CustomerOrders`, `customer_Orders`
- Unclear abbreviations: `cust_ord`, `prd_inv`
- Version numbers in names: `orders_v2`, `customers_final_v3`
- Hungarian notation: `tblCustomers`, `strName`

✅ **Do Use:**
- Consistent separators: `customer_orders`
- Clear, full words: `customer_orders`, `product_inventory`
- Consistent casing: `customer_orders`, `order_items`
- Descriptive names: `silver_sales_orders`
- Layer prefixes: `bronze_`, `silver_`, `gold_`

## Naming Convention Summary

| Resource Type | Pattern | Example |
|---------------|---------|---------|
| Workspace | `<platform>-<env>-<purpose>` | `fabric-prod-lakehouse` |
| Lakehouse | `lh_<domain>_<env>` | `lh_sales_prod` |
| Bronze Table | `bronze_<source>_<entity>_raw` | `bronze_sap_orders_raw` |
| Silver Table | `silver_<domain>_<entity>` | `silver_sales_orders` |
| Gold Table | `gold_<purpose>_<entity>` | `gold_analytics_sales` |
| Pipeline | `pl_<layer>_<action>_<entity>` | `pl_bronze_ingest_orders` |
| Notebook | `<layer>_<purpose>_<entity>` | `bronze_load_orders` |
| Column | `<name>_<suffix>` | `customer_id`, `order_date` |

## Implementation Checklist

- [ ] Document organization-specific standards
- [ ] Create naming convention templates
- [ ] Set up naming validation rules
- [ ] Train team on conventions
- [ ] Implement automated checks
- [ ] Review existing resources for compliance
- [ ] Update documentation regularly
- [ ] Provide naming examples in wiki

## Next Steps

1. Review [Architecture Documentation](architecture.md)
2. Implement [Governance & Security](governance-security.md)
3. Follow [Deployment Guide](deployment.md)
4. See [Examples](/examples) for practical applications
