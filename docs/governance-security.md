# Governance & Security

## Overview

A robust governance and security framework is essential for a modern data platform. This document outlines best practices for implementing governance and security in Microsoft Fabric.

## Security Principles

### Defense in Depth
Implement multiple layers of security controls:
1. Network security
2. Identity and access management
3. Data encryption
4. Application security
5. Monitoring and auditing

### Least Privilege
- Grant minimum required permissions
- Use role-based access control (RBAC)
- Regular access reviews
- Time-limited access for sensitive operations

### Zero Trust
- Verify explicitly
- Use least privileged access
- Assume breach

## Identity & Access Management

### Authentication

**Azure Active Directory Integration**
- Single sign-on (SSO) for all users
- Multi-factor authentication (MFA) required
- Conditional access policies
- Service principals for automation

**Managed Identities**
- Use system-assigned managed identities when possible
- User-assigned identities for shared resources
- Avoid storing credentials in code or configuration

### Authorization

**Role-Based Access Control (RBAC)**

#### Workspace Roles
```
Admin       - Full control over workspace
Member      - Create and manage items
Contributor - Create items, view data
Viewer      - Read-only access
```

#### Lakehouse Layer Permissions

**Bronze Layer**
- **Data Engineers**: Read/Write
- **Data Analysts**: Read-only
- **Systems**: Write (ingestion)

**Silver Layer**
- **Data Engineers**: Read/Write
- **Data Analysts**: Read-only
- **Data Scientists**: Read-only

**Gold Layer**
- **Business Users**: Read-only
- **Data Analysts**: Read-only
- **Data Engineers**: Read/Write
- **Power BI**: Read-only

#### Sample Permission Matrix
```
Role                | Bronze | Silver | Gold | Workspace
--------------------|--------|--------|------|----------
Platform Admin      | RWD    | RWD    | RWD  | Admin
Data Engineer       | RW     | RW     | RW   | Member
Data Analyst        | R      | R      | R    | Contributor
Business User       | -      | -      | R    | Viewer
System Account      | W      | -      | -    | Contributor

R = Read, W = Write, D = Delete
```

### Row-Level Security (RLS)

Implement RLS for sensitive data:
```python
# Example RLS in Power BI
[Region] = USERPRINCIPALNAME()

# Dynamic RLS based on user attributes
FILTER('Sales', 
    'Sales'[SalesRegion] IN LOOKUPVALUE(
        'UserRegions'[Region],
        'UserRegions'[Email], 
        USERPRINCIPALNAME()
    )
)
```

### Column-Level Security

Protect sensitive columns:
- PII (Personally Identifiable Information)
- Financial data
- Health information
- Credentials and secrets

## Data Encryption

### Encryption at Rest
- **OneLake**: Encrypted by default with Microsoft-managed keys
- **Option**: Customer-managed keys (CMK) via Azure Key Vault
- **Delta Tables**: Transparent encryption

### Encryption in Transit
- TLS 1.2 or higher for all connections
- HTTPS for all API calls
- Private endpoints for enhanced security

## Data Classification

### Classification Levels

**Public**
- No restrictions
- Publicly available information

**Internal**
- Internal use only
- Non-sensitive business data

**Confidential**
- Restricted access
- Business-critical data
- Requires approval for access

**Highly Confidential**
- Strict access controls
- PII, financial, health data
- Regular access audits

### Sensitivity Labels

Apply Microsoft Information Protection labels:
```
├── Public
├── General
├── Confidential
│   ├── Confidential - Internal
│   └── Confidential - Partner
└── Highly Confidential
    ├── Highly Confidential - PII
    └── Highly Confidential - Financial
```

## Data Masking & Anonymization

### Dynamic Data Masking

Mask sensitive data for non-privileged users:
- Email masking: j***@example.com
- Phone masking: XXX-XXX-1234
- Credit card masking: XXXX-XXXX-XXXX-1234

### Tokenization

Replace sensitive values with tokens:
```python
# Example tokenization
original_ssn = "123-45-6789"
tokenized_ssn = "TKN_ABC123XYZ"
```

### Data Anonymization

For analytics on sensitive data:
- Remove direct identifiers
- Generalize quasi-identifiers
- Add noise to numeric values
- K-anonymity principles

## Compliance & Regulatory

### Regulations to Consider
- **GDPR**: EU data protection
- **CCPA**: California privacy rights
- **HIPAA**: Healthcare data (if applicable)
- **SOX**: Financial reporting
- **Industry-specific**: Banking, healthcare, etc.

### Compliance Features

**Data Residency**
- OneLake data stored in selected region
- Cross-region replication controls
- Data sovereignty compliance

**Right to be Forgotten**
- Implement deletion workflows
- Hard delete vs. soft delete
- Audit deletion operations

**Data Retention**
- Define retention policies per layer
- Automated archival and deletion
- Legal hold capabilities

### Audit & Compliance Reporting
```
├── Access logs (who accessed what)
├── Modification logs (who changed what)
├── Security events
├── Compliance reports
└── Data lineage
```

## Data Governance

### Data Catalog

**Microsoft Purview Integration**
- Automatic data discovery
- Business glossary
- Data lineage tracking
- Metadata management

**Catalog Structure**
```
Data Asset
├── Technical Metadata
│   ├── Schema
│   ├── Format
│   └── Location
├── Business Metadata
│   ├── Owner
│   ├── Description
│   └── Tags
├── Operational Metadata
│   ├── Refresh schedule
│   ├── Dependencies
│   └── Quality metrics
└── Governance Metadata
    ├── Classification
    ├── Retention policy
    └── Access controls
```

### Data Quality

**Quality Dimensions**
- **Accuracy**: Data is correct
- **Completeness**: All required data present
- **Consistency**: Data is consistent across systems
- **Timeliness**: Data is up-to-date
- **Validity**: Data conforms to business rules

**Quality Checks**
```python
# Example quality checks
def validate_data_quality(df):
    checks = {
        'null_check': df.isNull().sum() == 0,
        'duplicate_check': df.count() == df.distinct().count(),
        'range_check': df['amount'].between(0, 1000000).all(),
        'format_check': df['email'].rlike(r'^[\w\.-]+@[\w\.-]+\.\w+$').all()
    }
    return checks
```

### Data Lineage

Track data from source to consumption:
```
Source System → Bronze → Silver → Gold → Report
     │            │        │        │        │
     └────────────┴────────┴────────┴────────┴─── Lineage Tracked
```

### Data Ownership

**Define Ownership**
- **Data Owner**: Business accountable for data
- **Data Steward**: Manages data quality and policies
- **Data Custodian**: IT responsible for storage and security
- **Data User**: Consumes data for business purposes

## Network Security

### Private Endpoints

Configure private endpoints for:
- OneLake storage
- Fabric workspace access
- Related Azure services

### Virtual Network Integration

**VNet Configuration**
```
├── Fabric Workspace
│   └── Private Endpoint → Subnet A
├── Azure Key Vault
│   └── Private Endpoint → Subnet B
└── Network Security Groups
    ├── Allow Fabric services
    └── Deny public internet
```

### Firewall Rules

- Restrict IP ranges
- Use service tags
- Implement network policies

## Secrets Management

### Azure Key Vault Integration

Store secrets in Key Vault:
- Connection strings
- API keys
- Certificates
- Passwords

**Usage in Fabric**
```python
# Reference Key Vault secrets
secret_value = mssparkutils.credentials.getSecret(
    "https://keyvault.vault.azure.net/", 
    "secret-name"
)
```

### Best Practices
- Never hardcode secrets
- Rotate secrets regularly
- Use short-lived tokens when possible
- Audit secret access

## Monitoring & Auditing

### Logging

**Activity Logs**
- User access and operations
- Data modifications
- Permission changes
- Failed access attempts

**Security Logs**
- Authentication events
- Authorization failures
- Suspicious activities
- Policy violations

### Monitoring Tools

**Azure Monitor**
- Workspace activity
- Performance metrics
- Resource utilization
- Custom alerts

**Microsoft Defender for Cloud**
- Security posture assessment
- Threat detection
- Compliance monitoring
- Recommendations

### Alerting

Configure alerts for:
- Unauthorized access attempts
- Unusual data access patterns
- Permission changes
- Data quality issues
- Pipeline failures

## Incident Response

### Security Incident Plan

1. **Detection**: Identify security event
2. **Containment**: Limit impact
3. **Investigation**: Determine root cause
4. **Remediation**: Fix vulnerability
5. **Recovery**: Restore normal operations
6. **Lessons Learned**: Update procedures

### Breach Response

**Immediate Actions**
- Isolate affected systems
- Preserve evidence
- Notify security team
- Document timeline

**Communication Plan**
- Internal stakeholders
- Affected users
- Regulatory bodies (if required)
- Legal counsel

## Best Practices Summary

1. **Implement defense in depth**: Multiple security layers
2. **Use least privilege**: Minimum necessary permissions
3. **Encrypt everything**: At rest and in transit
4. **Monitor continuously**: Real-time security monitoring
5. **Classify data**: Apply appropriate controls
6. **Audit regularly**: Review access and permissions
7. **Train users**: Security awareness program
8. **Plan for incidents**: Have response procedures
9. **Document policies**: Clear governance documentation
10. **Test controls**: Regular security assessments

## Governance Checklist

- [ ] Define data classification scheme
- [ ] Implement RBAC for all layers
- [ ] Configure encryption (at rest and in transit)
- [ ] Set up Microsoft Purview integration
- [ ] Define data retention policies
- [ ] Implement data quality framework
- [ ] Configure audit logging
- [ ] Set up security monitoring and alerts
- [ ] Document incident response procedures
- [ ] Conduct regular access reviews
- [ ] Implement secrets management
- [ ] Configure private endpoints
- [ ] Define data ownership model
- [ ] Create compliance reports
- [ ] Train users on security policies

## Next Steps

1. Review [Naming Conventions](naming-conventions.md)
2. Follow [Deployment Guide](deployment.md)
3. Implement [Data Quality Framework](lakehouse-zones.md)
4. Set up monitoring and alerting
