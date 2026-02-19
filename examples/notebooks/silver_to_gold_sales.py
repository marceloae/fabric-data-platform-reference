"""
Silver to Gold Transformation - Sales Analytics

This notebook reads cleansed data from the Silver layer,
creates aggregated views and dimensional models for the Gold layer.

Author: Data Platform Team
Last Modified: 2024-01
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, sum, count, avg, max, min, round, when,
    current_timestamp, date_format, year, month, dayofmonth
)
from pyspark.sql.window import Window
from delta.tables import DeltaTable
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# Configuration
# ============================================================================

SILVER_ORDERS_TABLE = "silver_sales_orders"
SILVER_CUSTOMERS_TABLE = "silver_customer_accounts"
GOLD_SALES_SUMMARY_TABLE = "gold_analytics_sales_summary"

# ============================================================================
# Transformation Functions
# ============================================================================

def create_daily_sales_summary(orders_df):
    """
    Create daily sales summary aggregation
    
    Args:
        orders_df: Orders dataframe from Silver
        
    Returns:
        Aggregated dataframe
    """
    return (orders_df
        .groupBy("order_date", "order_year", "order_month", "order_quarter")
        .agg(
            count("order_id").alias("total_orders"),
            sum("total_amount").alias("total_sales"),
            avg("total_amount").alias("average_order_value"),
            max("total_amount").alias("max_order_value"),
            min("total_amount").alias("min_order_value"),
            count(col("customer_id").distinct()).alias("unique_customers"),
            sum(when(col("is_high_value"), 1).otherwise(0)).alias("high_value_orders")
        )
        .withColumn("total_sales", round(col("total_sales"), 2))
        .withColumn("average_order_value", round(col("average_order_value"), 2))
        .withColumn("last_updated", current_timestamp())
    )

def create_customer_metrics(orders_df, customers_df):
    """
    Create customer-level metrics
    
    Args:
        orders_df: Orders dataframe from Silver
        customers_df: Customers dataframe from Silver
        
    Returns:
        Customer metrics dataframe
    """
    customer_orders = (orders_df
        .groupBy("customer_id")
        .agg(
            count("order_id").alias("lifetime_orders"),
            sum("total_amount").alias("lifetime_value"),
            max("order_date").alias("last_order_date"),
            min("order_date").alias("first_order_date"),
            avg("total_amount").alias("avg_order_value")
        )
    )
    
    # Join with customer data
    customer_360 = (customers_df
        .join(customer_orders, "customer_id", "left")
        .withColumn("lifetime_value", round(col("lifetime_value"), 2))
        .withColumn("avg_order_value", round(col("avg_order_value"), 2))
        .withColumn("last_updated", current_timestamp())
    )
    
    return customer_360

def create_product_performance(orders_df):
    """
    Create product performance metrics
    Note: This assumes order_items table exists with product details
    
    Args:
        orders_df: Orders dataframe
        
    Returns:
        Product performance metrics
    """
    # This is a simplified version
    # In production, join with order_items and products tables
    logger.info("Product performance aggregation would be implemented here")
    return None

# ============================================================================
# Main Processing
# ============================================================================

def main():
    """Main processing function"""
    
    logger.info("Starting Silver to Gold transformation")
    
    try:
        # Read from Silver layer
        logger.info(f"Reading from Silver table: {SILVER_ORDERS_TABLE}")
        orders_df = spark.read.format("delta").table(SILVER_ORDERS_TABLE)
        
        # Filter for active records only
        orders_df = orders_df.filter(col("is_active") == True)
        
        initial_count = orders_df.count()
        logger.info(f"Orders record count: {initial_count}")
        
        # Create daily sales summary
        logger.info("Creating daily sales summary...")
        daily_summary = create_daily_sales_summary(orders_df)
        
        summary_count = daily_summary.count()
        logger.info(f"Daily summary record count: {summary_count}")
        
        # Write to Gold layer
        logger.info(f"Writing to Gold table: {GOLD_SALES_SUMMARY_TABLE}")
        
        daily_summary.write \
            .format("delta") \
            .mode("overwrite") \
            .option("overwriteSchema", "true") \
            .saveAsTable(GOLD_SALES_SUMMARY_TABLE)
        
        logger.info("Daily sales summary created successfully")
        
        # Optimize the Gold table
        logger.info("Optimizing Gold table...")
        spark.sql(f"OPTIMIZE {GOLD_SALES_SUMMARY_TABLE}")
        
        # Z-order by frequently filtered columns
        spark.sql(f"""
            OPTIMIZE {GOLD_SALES_SUMMARY_TABLE}
            ZORDER BY (order_year, order_month, order_date)
        """)
        
        logger.info("Optimization completed")
        
        # Vacuum old files (retain 7 days)
        logger.info("Running vacuum...")
        spark.sql(f"VACUUM {GOLD_SALES_SUMMARY_TABLE} RETAIN 168 HOURS")
        
        logger.info("Transformation completed successfully")
        
        return {
            "status": "Success",
            "orders_processed": initial_count,
            "summary_records": summary_count
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
