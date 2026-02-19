# Examples

This directory contains practical examples and patterns for implementing the Fabric Data Platform Reference architecture.

## Contents

### Pipelines
Sample data pipelines demonstrating common patterns:
- Bronze ingestion pipelines
- Silver transformation pipelines
- Gold aggregation pipelines
- Error handling and retry logic

### Notebooks
Example notebooks for data processing:
- Data quality checks
- Bronze to Silver transformations
- Silver to Gold aggregations
- Utility functions

## Getting Started

1. Review the pipeline examples in `/pipelines`
2. Examine notebook examples in `/notebooks`
3. Adapt examples to your specific use cases
4. Follow naming conventions from `/docs/naming-conventions.md`

## Example Scenarios

### Scenario 1: Daily Sales Data Processing
See: `pipelines/pl_daily_sales_load.json` and `notebooks/bronze_to_silver_sales.py`

### Scenario 2: Customer Data Enrichment
See: `pipelines/pl_customer_enrichment.json` and `notebooks/silver_to_gold_customer.py`

### Scenario 3: Real-time Streaming
See: `pipelines/pl_streaming_events.json`

## Best Practices

- Always include error handling
- Implement data quality checks
- Log processing metrics
- Use parameterized pipelines
- Follow the medallion architecture pattern

## Contributing

When adding new examples:
1. Follow existing patterns and structure
2. Include comprehensive comments
3. Add README documentation
4. Test thoroughly before committing
