#!/usr/bin/env python3
"""
Minimal executable code to read and write data from Delta tables and Parquet files.
This script is designed for Azure Databricks integration testing.

Usage:
    python databricks_io.py
"""

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from delta import configure_spark_with_delta_pip


def create_spark_session():
    """
    Create a Spark session with Delta Lake support.
    
    Returns:
        SparkSession: Configured Spark session
    """
    builder = SparkSession.builder \
        .appName("DatabricksIntegrationTest") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    
    spark = configure_spark_with_delta_pip(builder).getOrCreate()
    return spark


def read_parquet(spark, parquet_path):
    """
    Read data from a Parquet file.
    
    Args:
        spark (SparkSession): Spark session
        parquet_path (str): Path to the Parquet file
        
    Returns:
        DataFrame: Spark DataFrame with the data
    """
    print(f"Reading Parquet file from: {parquet_path}")
    df = spark.read.parquet(parquet_path)
    print(f"Successfully read {df.count()} rows")
    return df


def write_parquet(df, parquet_path, mode="overwrite"):
    """
    Write DataFrame to a Parquet file.
    
    Args:
        df (DataFrame): Spark DataFrame to write
        parquet_path (str): Path where to write the Parquet file
        mode (str): Write mode - 'overwrite', 'append', 'ignore', 'error'
    """
    print(f"Writing Parquet file to: {parquet_path}")
    df.write.mode(mode).parquet(parquet_path)
    print("Successfully wrote Parquet file")


def read_delta_table(spark, delta_path):
    """
    Read data from a Delta table.
    
    Args:
        spark (SparkSession): Spark session
        delta_path (str): Path to the Delta table
        
    Returns:
        DataFrame: Spark DataFrame with the data
    """
    print(f"Reading Delta table from: {delta_path}")
    df = spark.read.format("delta").load(delta_path)
    print(f"Successfully read {df.count()} rows")
    return df


def write_delta_table(df, delta_path, mode="overwrite"):
    """
    Write DataFrame to a Delta table.
    
    Args:
        df (DataFrame): Spark DataFrame to write
        delta_path (str): Path where to write the Delta table
        mode (str): Write mode - 'overwrite', 'append', 'ignore', 'error'
    """
    print(f"Writing Delta table to: {delta_path}")
    df.write.format("delta").mode(mode).save(delta_path)
    print("Successfully wrote Delta table")


def create_sample_dataframe(spark):
    """
    Create a sample DataFrame for testing.
    
    Args:
        spark (SparkSession): Spark session
        
    Returns:
        DataFrame: Sample Spark DataFrame
    """
    schema = StructType([
        StructField("id", IntegerType(), True),
        StructField("name", StringType(), True),
        StructField("value", IntegerType(), True)
    ])
    
    data = [
        (1, "Alice", 100),
        (2, "Bob", 200),
        (3, "Charlie", 300),
        (4, "Diana", 400),
        (5, "Eve", 500)
    ]
    
    df = spark.createDataFrame(data, schema)
    return df


def main():
    """
    Main function to demonstrate reading and writing Parquet files and Delta tables.
    
    Update the paths below to match your Azure Databricks environment:
    - PARQUET_PATH: Path to your Parquet file/directory
    - DELTA_TABLE_PATH: Path to your Delta table
    """
    
    # TODO: Update these paths to match your Azure Databricks environment
    PARQUET_PATH = "/dbfs/mnt/data/parquet_data"  # Update this path
    DELTA_TABLE_PATH = "/dbfs/mnt/data/delta_table"  # Update this path
    
    # Create Spark session
    print("Creating Spark session with Delta Lake support...")
    spark = create_spark_session()
    
    try:
        # Example 1: Create sample data and write to Parquet
        print("\n=== Example 1: Write to Parquet ===")
        sample_df = create_sample_dataframe(spark)
        sample_df.show()
        write_parquet(sample_df, PARQUET_PATH)
        
        # Example 2: Read from Parquet
        print("\n=== Example 2: Read from Parquet ===")
        parquet_df = read_parquet(spark, PARQUET_PATH)
        parquet_df.show()
        
        # Example 3: Write to Delta table
        print("\n=== Example 3: Write to Delta table ===")
        write_delta_table(sample_df, DELTA_TABLE_PATH)
        
        # Example 4: Read from Delta table
        print("\n=== Example 4: Read from Delta table ===")
        delta_df = read_delta_table(spark, DELTA_TABLE_PATH)
        delta_df.show()
        
        # Example 5: Append to Delta table
        print("\n=== Example 5: Append to Delta table ===")
        new_data_df = spark.createDataFrame([(6, "Frank", 600)], ["id", "name", "value"])
        write_delta_table(new_data_df, DELTA_TABLE_PATH, mode="append")
        
        # Read again to verify append
        updated_delta_df = read_delta_table(spark, DELTA_TABLE_PATH)
        updated_delta_df.show()
        
        print("\n=== All operations completed successfully! ===")
        
    except Exception as e:
        print(f"\nError occurred: {str(e)}")
        raise
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
