# Gold Layer

## Purpose
The Gold layer contains business-level aggregations, dimensional models, and feature sets optimized for consumption.

## Structure
```
gold/
├── analytics/    # Analytics and aggregations
├── reporting/    # Reporting datasets
└── ml_features/  # Machine learning features
```

## Characteristics
- **Data Quality**: Production-grade, highly trusted
- **Schema**: Optimized for consumption patterns
- **Format**: Highly optimized Delta tables
- **Transformations**: Aggregations, denormalization, modeling
- **Retention**: Based on business requirements

## Usage
1. Create dimensional models (star schema)
2. Build pre-aggregated metrics
3. Generate ML feature sets
4. Serve data to reports and dashboards

## Consumption
Gold layer data is consumed by:
- Power BI reports and dashboards
- SQL analytics endpoints
- Machine learning models
- External APIs

See: [Lakehouse Zones Documentation](/docs/lakehouse-zones.md)
