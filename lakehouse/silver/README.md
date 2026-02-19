# Silver Layer

## Purpose
The Silver layer contains validated, cleaned, and enriched data ready for analytics.

## Structure
```
silver/
├── sales/        # Sales domain data
├── customer/     # Customer domain data
└── inventory/    # Inventory domain data
```

## Characteristics
- **Data Quality**: Validated and cleaned
- **Schema**: Enforced and standardized
- **Format**: Delta tables with schema enforcement
- **Transformations**: Deduplication, validation, enrichment
- **Retention**: Medium to long-term

## Usage
1. Receive cleansed data from Bronze layer
2. Apply business rules and validations
3. Enforce schema and data types
4. Store as foundation for Gold layer

## Next Steps
Data flows from Silver → Gold for aggregation and modeling.

See: [Lakehouse Zones Documentation](/docs/lakehouse-zones.md)
