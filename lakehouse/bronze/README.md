# Bronze Layer

## Purpose
The Bronze layer is the landing zone for raw data, preserving source data in its original form.

## Structure
```
bronze/
├── erp/          # Enterprise Resource Planning data
├── crm/          # Customer Relationship Management data
└── external/     # External/third-party data sources
```

## Characteristics
- **Data Quality**: As-is from source
- **Schema**: Flexible, schema-on-read
- **Format**: Original format or Delta/Parquet
- **Transformations**: Minimal (metadata addition only)
- **Retention**: Long-term storage

## Usage
1. Land raw data from source systems
2. Preserve original structure and format
3. Add ingestion metadata
4. Store for audit and replay scenarios

## Next Steps
Data flows from Bronze → Silver for cleansing and validation.

See: [Lakehouse Zones Documentation](/docs/lakehouse-zones.md)
