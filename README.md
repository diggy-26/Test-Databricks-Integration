# Test-Databricks-Integration

This repository provides minimal Python executable code to read and write data from Delta tables and Parquet files for Azure Databricks integration testing.

## Overview

The `databricks_io.py` script contains functions to:
- Read and write Parquet files
- Read and write Delta tables
- Create sample data for testing

## Prerequisites

### On Azure Databricks
Azure Databricks clusters typically come pre-installed with:
- PySpark
- Delta Lake

No additional installation is required when running on Databricks.

### For Local Development
If running locally, install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### 1. Update Paths

Before running the script, update the paths in `databricks_io.py` to match your Azure Databricks environment:

```python
PARQUET_PATH = "/dbfs/mnt/data/parquet_data"  # Update this path
DELTA_TABLE_PATH = "/dbfs/mnt/data/delta_table"  # Update this path
```

Common path formats in Azure Databricks:
- **DBFS paths**: `/dbfs/mnt/data/your_file`
- **Unity Catalog**: `catalog.schema.table_name`
- **Azure Storage**: `abfss://<container>@<storage-account>.dfs.core.windows.net/path`

### 2. Run the Script

On Azure Databricks:
```bash
python databricks_io.py
```

Or in a Databricks notebook:
```python
%run /path/to/databricks_io.py
```

### 3. Use Individual Functions

You can also import and use individual functions:

```python
from databricks_io import (
    create_spark_session,
    read_parquet,
    write_parquet,
    read_delta_table,
    write_delta_table
)

# Create Spark session
spark = create_spark_session()

# Read Parquet file
df = read_parquet(spark, "/path/to/parquet/file")
df.show()

# Write Delta table
write_delta_table(df, "/path/to/delta/table", mode="overwrite")

# Read Delta table
delta_df = read_delta_table(spark, "/path/to/delta/table")
delta_df.show()
```

## Functions

### `create_spark_session()`
Creates a Spark session with Delta Lake support.

### `read_parquet(spark, parquet_path)`
Reads data from a Parquet file.
- **spark**: SparkSession object
- **parquet_path**: Path to the Parquet file or directory

### `write_parquet(df, parquet_path, mode="overwrite")`
Writes DataFrame to a Parquet file.
- **df**: Spark DataFrame to write
- **parquet_path**: Destination path
- **mode**: Write mode (`overwrite`, `append`, `ignore`, `error`)

### `read_delta_table(spark, delta_path)`
Reads data from a Delta table.
- **spark**: SparkSession object
- **delta_path**: Path to the Delta table

### `write_delta_table(df, delta_path, mode="overwrite")`
Writes DataFrame to a Delta table.
- **df**: Spark DataFrame to write
- **delta_path**: Destination path
- **mode**: Write mode (`overwrite`, `append`, `ignore`, `error`)

### `create_sample_dataframe(spark)`
Creates a sample DataFrame for testing purposes.

## Examples

The `main()` function in `databricks_io.py` demonstrates:
1. Creating sample data
2. Writing to Parquet format
3. Reading from Parquet format
4. Writing to Delta table format
5. Reading from Delta table format
6. Appending data to an existing Delta table

## Notes

- Ensure you have proper permissions to read/write to the specified paths in your Azure Databricks environment
- Delta tables support ACID transactions and time travel features
- Parquet is a columnar storage format optimized for analytics workloads
- The script includes error handling and informative print statements for debugging

## License

This is a test repository for integration testing purposes.
