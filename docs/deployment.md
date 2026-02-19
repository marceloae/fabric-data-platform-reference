# Deployment Guide

## Overview

This guide provides step-by-step instructions for deploying the Fabric Data Platform Reference architecture in your environment.

## Prerequisites

### Access Requirements
- Microsoft Fabric capacity (F2 or higher recommended)
- Azure subscription (for related services)
- Azure Active Directory tenant
- Power BI Premium or Fabric capacity

### Required Permissions
- Fabric Administrator or Capacity Administrator
- Azure Subscription Contributor
- Power BI Workspace Admin
- Azure AD permissions for app registrations

### Tools Needed
- Azure Portal access
- Power BI Service access
- Visual Studio Code (recommended)
- Git for version control
- Azure CLI (optional)
- PowerShell or Bash

## Deployment Phases

### Phase 1: Environment Setup

#### 1.1 Provision Microsoft Fabric Capacity

1. Navigate to Azure Portal
2. Create Fabric Capacity resource
3. Select appropriate SKU (F2 minimum, F4+ recommended for production)
4. Configure region and settings
5. Assign capacity administrators

#### 1.2 Create Workspaces

Create workspaces for each environment:

**Development**
```
Name: fabric-dev-lakehouse
Capacity: Your Fabric capacity
License mode: Fabric
```

**Test/UAT**
```
Name: fabric-test-lakehouse
Capacity: Your Fabric capacity
License mode: Fabric
```

**Production**
```
Name: fabric-prod-lakehouse
Capacity: Your Fabric capacity
License mode: Fabric
```

#### 1.3 Configure Workspace Settings

For each workspace:
1. Assign Admin, Member, Contributor, Viewer roles
2. Configure workspace identity
3. Enable Git integration (optional)
4. Set up workspace-level settings

### Phase 2: Lakehouse Deployment

#### 2.1 Create Lakehouses

Create lakehouse for each environment:

**Development Lakehouse**
```powershell
# Using Fabric UI or API
Name: lh_platform_dev
Workspace: fabric-dev-lakehouse
```

**Production Lakehouse**
```powershell
Name: lh_platform_prod
Workspace: fabric-prod-lakehouse
```

#### 2.2 Create Folder Structure

Execute the following structure in each lakehouse:

```
/Files
├── bronze/
│   ├── erp/
│   │   ├── sales/
│   │   └── inventory/
│   ├── crm/
│   │   └── customers/
│   └── external/
│       └── reference_data/
├── silver/
│   ├── sales/
│   ├── customer/
│   └── inventory/
└── gold/
    ├── analytics/
    ├── reporting/
    └── ml_features/

/Tables
├── bronze/
├── silver/
└── gold/
```

#### 2.3 Configure Lakehouse Properties

Set properties for each lakehouse:
- Enable version control
- Configure default file format (Delta/Parquet)
- Set retention policies
- Configure compute settings

### Phase 3: Security & Governance

#### 3.1 Configure Azure AD Integration

1. Set up security groups:
   ```
   SG-Fabric-DataEngineers
   SG-Fabric-DataAnalysts
   SG-Fabric-BusinessUsers
   SG-Fabric-Admins
   ```

2. Assign workspace roles to groups:
   ```
   SG-Fabric-Admins → Admin
   SG-Fabric-DataEngineers → Member
   SG-Fabric-DataAnalysts → Contributor
   SG-Fabric-BusinessUsers → Viewer
   ```

#### 3.2 Set Up Row-Level Security

Implement RLS in semantic models:
```dax
# Example RLS rule
[Region] = USERPRINCIPALNAME()
```

#### 3.3 Configure Data Classification

1. Enable Microsoft Information Protection
2. Apply sensitivity labels
3. Configure auto-labeling policies
4. Set up DLP policies

#### 3.4 Set Up Azure Key Vault

1. Create Key Vault:
   ```bash
   az keyvault create \
     --name kv-fabric-platform-prod \
     --resource-group rg-fabric-prod \
     --location eastus
   ```

2. Store secrets:
   ```bash
   az keyvault secret set \
     --vault-name kv-fabric-platform-prod \
     --name "sql-connection-string" \
     --value "your-connection-string"
   ```

3. Configure access policies for Fabric workspace identity

#### 3.5 Enable Auditing & Monitoring

1. Configure activity logs
2. Set up Azure Monitor
3. Create alert rules
4. Enable diagnostic settings

### Phase 4: Data Pipelines

#### 4.1 Create Sample Ingestion Pipeline

Create a Bronze ingestion pipeline:

**Pipeline: pl_bronze_ingest_orders**
```json
{
  "name": "pl_bronze_ingest_orders",
  "activities": [
    {
      "name": "Copy_Orders_To_Bronze",
      "type": "Copy",
      "source": {
        "type": "SqlSource"
      },
      "sink": {
        "type": "LakehouseSink",
        "path": "bronze/erp/sales/orders/"
      }
    }
  ]
}
```

#### 4.2 Create Transformation Notebooks

**Bronze to Silver Notebook**
```python
# bronze_to_silver_orders.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

# Read bronze data
bronze_df = spark.read.format("delta").load("Tables/bronze/erp_orders_raw")

# Transform and clean
silver_df = (bronze_df
    .dropDuplicates(["order_id"])
    .filter(col("order_id").isNotNull())
    .withColumn("order_date", to_date(col("order_date")))
    .withColumn("created_at", current_timestamp())
)

# Write to silver
silver_df.write.format("delta").mode("overwrite").save("Tables/silver/sales_orders")
```

#### 4.3 Set Up Orchestration

Create a master pipeline to orchestrate all data flows:

**Pipeline: pl_master_daily_load**
- Schedule: Daily at 2:00 AM
- Trigger: Time-based trigger
- Activities: Execute bronze, silver, gold pipelines in sequence

### Phase 5: Semantic Layer

#### 5.1 Create Power BI Semantic Models

1. Create semantic model from Gold tables
2. Define relationships
3. Create measures and calculations
4. Implement RLS
5. Optimize for performance

#### 5.2 Create Sample Reports

Deploy initial reports:
- Executive Dashboard
- Operational Metrics
- Data Quality Dashboard

### Phase 6: Monitoring & Alerting

#### 6.1 Configure Monitoring

Set up monitoring for:
- Pipeline execution status
- Data quality metrics
- Query performance
- Resource utilization
- Security events

#### 6.2 Create Alerts

Configure alerts for:
```
- Pipeline failures
- Data quality threshold violations
- Unusual access patterns
- Performance degradation
- Capacity utilization (>80%)
```

#### 6.3 Set Up Dashboards

Create operational dashboards:
- Pipeline health dashboard
- Data quality metrics
- Performance monitoring
- Cost tracking

### Phase 7: Documentation & Training

#### 7.1 Complete Documentation

Document:
- Architecture decisions
- Data models and schemas
- Pipeline configurations
- Security policies
- Operational procedures
- Troubleshooting guides

#### 7.2 Create User Guides

Prepare guides for:
- Data Engineers
- Data Analysts
- Business Users
- Administrators

#### 7.3 Conduct Training

Training sessions on:
- Platform overview
- Self-service analytics
- Data governance
- Security best practices
- Support procedures

## Post-Deployment Checklist

### Immediate Tasks
- [ ] Verify all workspaces created
- [ ] Confirm lakehouse structure is correct
- [ ] Test pipeline execution
- [ ] Validate security configuration
- [ ] Verify data flows end-to-end
- [ ] Test report access
- [ ] Confirm monitoring is active
- [ ] Document all configurations

### Week 1 Tasks
- [ ] Monitor pipeline execution
- [ ] Review security logs
- [ ] Check data quality metrics
- [ ] Gather user feedback
- [ ] Adjust configurations as needed
- [ ] Fine-tune performance
- [ ] Update documentation

### Month 1 Tasks
- [ ] Review access patterns
- [ ] Optimize queries and pipelines
- [ ] Assess capacity requirements
- [ ] Review cost and usage
- [ ] Conduct security review
- [ ] Plan scaling strategies
- [ ] Update operational procedures

## Deployment Scripts

### PowerShell: Create Workspace Structure

```powershell
# create-workspace-structure.ps1

# Variables
$tenantId = "your-tenant-id"
$workspaceName = "fabric-prod-lakehouse"
$capacityId = "your-capacity-id"

# Create workspace
$workspace = New-PowerBIWorkspace -Name $workspaceName

# Assign capacity
Set-PowerBIWorkspace -Id $workspace.Id -CapacityId $capacityId

Write-Host "Workspace created: $workspaceName"
```

### Python: Create Folder Structure

```python
# create_lakehouse_structure.py
import os

def create_folder_structure(base_path):
    """Create standard lakehouse folder structure"""
    
    folders = [
        "bronze/erp/sales",
        "bronze/erp/inventory",
        "bronze/crm/customers",
        "bronze/external/reference_data",
        "silver/sales",
        "silver/customer",
        "silver/inventory",
        "gold/analytics",
        "gold/reporting",
        "gold/ml_features"
    ]
    
    for folder in folders:
        full_path = os.path.join(base_path, folder)
        os.makedirs(full_path, exist_ok=True)
        print(f"Created: {full_path}")

if __name__ == "__main__":
    # Update with your lakehouse path
    lakehouse_path = "/lakehouse/default/Files"
    create_folder_structure(lakehouse_path)
```

### Bash: Setup Script

```bash
#!/bin/bash
# setup-environment.sh

# Set variables
ENVIRONMENT="prod"
RESOURCE_GROUP="rg-fabric-$ENVIRONMENT"
LOCATION="eastus"
KEYVAULT_NAME="kv-fabric-$ENVIRONMENT"

# Create resource group
az group create \
  --name $RESOURCE_GROUP \
  --location $LOCATION

# Create Key Vault
az keyvault create \
  --name $KEYVAULT_NAME \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION

echo "Environment setup complete"
```

## Troubleshooting

### Common Issues

**Issue: Pipeline Execution Fails**
```
Solution:
1. Check activity logs
2. Verify source/sink connections
3. Validate permissions
4. Check data format compatibility
```

**Issue: Lakehouse Access Denied**
```
Solution:
1. Verify workspace role assignments
2. Check item-level permissions
3. Confirm Azure AD group membership
4. Review conditional access policies
```

**Issue: Poor Query Performance**
```
Solution:
1. Check table partitioning
2. Analyze query execution plans
3. Optimize Delta table structure
4. Review capacity utilization
5. Consider Z-ordering for frequently filtered columns
```

**Issue: Data Quality Problems**
```
Solution:
1. Review source data
2. Check transformation logic
3. Validate data type conversions
4. Implement additional quality checks
5. Review business rules
```

## Rollback Procedures

### Pipeline Rollback
1. Disable failing pipeline
2. Restore previous version from Git
3. Validate in lower environment
4. Re-deploy to production

### Data Rollback
1. Use Delta Lake time travel
2. Restore from backup tables
3. Rerun pipelines from specific checkpoint
4. Validate data integrity

## Support & Maintenance

### Regular Maintenance Tasks

**Daily**
- Monitor pipeline execution
- Review error logs
- Check data quality metrics

**Weekly**
- Review capacity utilization
- Analyze query performance
- Check security logs
- Review access patterns

**Monthly**
- Capacity planning review
- Cost optimization
- Security audit
- Performance tuning
- Documentation updates

### Getting Help

1. Check documentation
2. Review Azure/Fabric status
3. Consult troubleshooting guide
4. Contact support team
5. Engage Microsoft support if needed

## Next Steps

1. Review [Architecture Documentation](architecture.md)
2. Understand [Lakehouse Zones](lakehouse-zones.md)
3. Implement [Governance & Security](governance-security.md)
4. Follow [Naming Conventions](naming-conventions.md)
5. Explore [Examples](/examples)

## Additional Resources

- Microsoft Fabric Documentation
- Delta Lake Documentation
- Power BI Documentation
- Azure Architecture Center
- Fabric Community Forums
