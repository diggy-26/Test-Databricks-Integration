#!/usr/bin/env python3
"""
Example usage of databricks_io functions.
This demonstrates how to use the functions individually.
"""

from databricks_io import (
    create_spark_session,
    read_parquet,
    write_parquet,
    read_delta_table,
    write_delta_table,
    create_sample_dataframe
)


def example_parquet_operations():
    """Example: Working with Parquet files"""
    spark = create_spark_session()
    
    # Create sample data
    df = create_sample_dataframe(spark)
    
    # Write to Parquet
    parquet_path = "/tmp/test_parquet"
    write_parquet(df, parquet_path)
    
    # Read from Parquet
    loaded_df = read_parquet(spark, parquet_path)
    loaded_df.show()
    
    spark.stop()


def example_delta_operations():
    """Example: Working with Delta tables"""
    spark = create_spark_session()
    
    # Create sample data
    df = create_sample_dataframe(spark)
    
    # Write to Delta table
    delta_path = "/tmp/test_delta"
    write_delta_table(df, delta_path)
    
    # Read from Delta table
    loaded_df = read_delta_table(spark, delta_path)
    loaded_df.show()
    
    # Append more data
    new_df = spark.createDataFrame([(6, "Frank", 600)], ["id", "name", "value"])
    write_delta_table(new_df, delta_path, mode="append")
    
    # Read again to see appended data
    updated_df = read_delta_table(spark, delta_path)
    updated_df.show()
    
    spark.stop()


def example_custom_paths():
    """
    Example: Using custom Azure Databricks paths
    
    Update these paths to match your environment:
    """
    spark = create_spark_session()
    
    # Example Azure paths (update these)
    AZURE_PARQUET = "abfss://container@account.dfs.core.windows.net/data/parquet"
    AZURE_DELTA = "abfss://container@account.dfs.core.windows.net/data/delta"
    
    # Or DBFS paths
    DBFS_PARQUET = "/dbfs/mnt/data/parquet_data"
    DBFS_DELTA = "/dbfs/mnt/data/delta_table"
    
    df = create_sample_dataframe(spark)
    
    # Use whichever path format is appropriate for your setup
    # write_parquet(df, DBFS_PARQUET)
    # write_delta_table(df, DBFS_DELTA)
    
    spark.stop()


if __name__ == "__main__":
    print("Running Parquet operations example...")
    example_parquet_operations()
    
    print("\nRunning Delta operations example...")
    example_delta_operations()
    
    print("\nFor custom Azure paths, update example_custom_paths() function")
