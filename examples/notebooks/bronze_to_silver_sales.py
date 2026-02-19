"""
Bronze to Silver Transformation - Sales Orders

This notebook reads raw sales order data from the Bronze layer,
applies data quality checks, cleanses the data, and writes it to the Silver layer.

Author: Data Platform Team
Last Modified: 2024-01
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, when, trim, upper, lower, current_timestamp, 
    to_date, to_timestamp, regexp_replace, coalesce, lit
)
from pyspark.sql.types import DecimalType
from delta.tables import DeltaTable
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# Configuration
# ============================================================================

BRONZE_TABLE = "bronze_erp_orders_raw"
SILVER_TABLE = "silver_sales_orders"
BATCH_ID = "batch_001"  # Pass as parameter in production

# ============================================================================
# Helper Functions
# ============================================================================

def validate_data_quality(df):
    """
    Perform data quality checks on the dataframe
    
    Args:
        df: Input dataframe
        
    Returns:
        dict: Quality metrics
    """
    total_records = df.count()
    null_order_ids = df.filter(col("order_id").isNull()).count()
    null_customers = df.filter(col("customer_id").isNull()).count()
    invalid_amounts = df.filter(
        (col("total_amount").isNull()) | (col("total_amount") < 0)
    ).count()
    
    quality_metrics = {
        "total_records": total_records,
        "null_order_ids": null_order_ids,
        "null_customers": null_customers,
        "invalid_amounts": invalid_amounts,
        "quality_score": (1 - (null_order_ids + null_customers + invalid_amounts) / total_records) * 100
    }
    
    logger.info(f"Quality Metrics: {quality_metrics}")
    return quality_metrics

def cleanse_orders(df):
    """
    Cleanse and transform order data
    
    Args:
        df: Raw dataframe from Bronze
        
    Returns:
        Cleansed dataframe
    """
    return (df
        # Remove duplicates based on order_id
        .dropDuplicates(["order_id"])
        
        # Filter out invalid records
        .filter(col("order_id").isNotNull())
        .filter(col("customer_id").isNotNull())
        .filter(col("total_amount").isNotNull())
        
        # Standardize data types
        .withColumn("order_id", col("order_id").cast("long"))
        .withColumn("customer_id", col("customer_id").cast("long"))
        .withColumn("total_amount", col("total_amount").cast(DecimalType(18, 2)))
        
        # Cleanse string fields
        .withColumn("status", upper(trim(col("status"))))
        
        # Standardize date fields
        .withColumn("order_date", to_date(col("order_date")))
        
        # Add audit columns
        .withColumn("processed_at", current_timestamp())
        .withColumn("batch_id", lit(BATCH_ID))
        .withColumn("is_active", lit(True))
        
        # Handle nulls with default values
        .withColumn("status", coalesce(col("status"), lit("UNKNOWN")))
    )

def enrich_orders(df):
    """
    Enrich order data with additional calculations and flags
    
    Args:
        df: Cleansed dataframe
        
    Returns:
        Enriched dataframe
    """
    return (df
        # Add business logic derived columns
        .withColumn("is_high_value", 
            when(col("total_amount") > 1000, True).otherwise(False)
        )
        .withColumn("order_year", 
            col("order_date").substr(1, 4).cast("int")
        )
        .withColumn("order_month", 
            col("order_date").substr(6, 2).cast("int")
        )
        .withColumn("order_quarter",
            when(col("order_month").isin(1, 2, 3), "Q1")
            .when(col("order_month").isin(4, 5, 6), "Q2")
            .when(col("order_month").isin(7, 8, 9), "Q3")
            .otherwise("Q4")
        )
    )

# ============================================================================
# Main Processing
# ============================================================================

def main():
    """Main processing function"""
    
    logger.info(f"Starting Bronze to Silver transformation for {BRONZE_TABLE}")
    
    try:
        # Read from Bronze layer
        logger.info(f"Reading from Bronze table: {BRONZE_TABLE}")
        bronze_df = spark.read.format("delta").table(BRONZE_TABLE)
        
        initial_count = bronze_df.count()
        logger.info(f"Initial record count: {initial_count}")
        
        # Validate data quality
        quality_metrics = validate_data_quality(bronze_df)
        
        # Cleanse data
        logger.info("Cleansing data...")
        cleansed_df = cleanse_orders(bronze_df)
        
        # Enrich data
        logger.info("Enriching data...")
        enriched_df = enrich_orders(cleansed_df)
        
        final_count = enriched_df.count()
        logger.info(f"Final record count: {final_count}")
        logger.info(f"Records filtered: {initial_count - final_count}")
        
        # Write to Silver layer using merge for upsert
        logger.info(f"Writing to Silver table: {SILVER_TABLE}")
        
        # Check if table exists
        if spark.catalog.tableExists(SILVER_TABLE):
            # Perform merge (upsert)
            silver_table = DeltaTable.forName(spark, SILVER_TABLE)
            
            silver_table.alias("target").merge(
                enriched_df.alias("source"),
                "target.order_id = source.order_id"
            ).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
            
            logger.info("Merge completed successfully")
        else:
            # First load - create table
            enriched_df.write.format("delta").mode("overwrite").saveAsTable(SILVER_TABLE)
            logger.info("Table created successfully")
        
        # Log success metrics
        logger.info("Transformation completed successfully")
        logger.info(f"Quality Score: {quality_metrics['quality_score']:.2f}%")
        
        return {
            "status": "Success",
            "records_processed": final_count,
            "quality_score": quality_metrics['quality_score']
        }
        
    except Exception as e:
        logger.error(f"Error during transformation: {str(e)}")
        raise

# ============================================================================
# Execute
# ============================================================================

if __name__ == "__main__":
    result = main()
    print(f"Processing Result: {result}")
