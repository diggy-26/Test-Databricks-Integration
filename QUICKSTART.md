# Quick Start Guide

This is a quick reference for using the Delta table and Parquet file operations.

## TL;DR - Minimal Example

```python
from databricks_io import *

# Create Spark session
spark = create_spark_session()

# Read Parquet
df = read_parquet(spark, "/path/to/parquet")

# Write Parquet
write_parquet(df, "/path/to/output/parquet")

# Read Delta table
delta_df = read_delta_table(spark, "/path/to/delta")

# Write Delta table
write_delta_table(df, "/path/to/output/delta")
```

## Update Paths

Before running, update these paths in `databricks_io.py`:

```python
PARQUET_PATH = "/dbfs/mnt/data/parquet_data"      # Your Parquet path
DELTA_TABLE_PATH = "/dbfs/mnt/data/delta_table"   # Your Delta table path
```

## Common Azure Databricks Path Formats

| Type | Format | Example |
|------|--------|---------|
| DBFS | `/dbfs/mnt/...` | `/dbfs/mnt/data/myfile.parquet` |
| Azure Storage | `abfss://...` | `abfss://container@account.dfs.core.windows.net/path` |
| Unity Catalog | `catalog.schema.table` | `main.default.my_table` |

## Run Options

### Option 1: Run the complete example
```bash
python databricks_io.py
```

### Option 2: Run individual examples
```bash
python example_usage.py
```

### Option 3: Use in a notebook
```python
%run /path/to/databricks_io.py
```

### Option 4: Import functions
```python
from databricks_io import read_delta_table, write_delta_table
```

## Write Modes

- `overwrite` - Replace existing data (default)
- `append` - Add to existing data
- `ignore` - Skip if data exists
- `error` - Fail if data exists

Example:
```python
write_delta_table(df, path, mode="append")
```

## Tips

1. **Permissions**: Ensure you have read/write access to the specified paths
2. **Delta vs Parquet**: Delta tables support ACID transactions and time travel
3. **Large files**: Use partitioning for better performance with large datasets
4. **Testing**: Use `/tmp/` paths for testing before using production paths

## Troubleshooting

### "Path not found"
- Verify the path exists in your Databricks environment
- Check DBFS mount points: `dbutils.fs.mounts()`

### "Permission denied"
- Ensure your cluster has access to the storage account
- Check Azure credentials and access policies

### "Delta table not found"
- Delta tables must be created before reading
- Use `write_delta_table()` to create a new table

## Next Steps

1. Update paths in `databricks_io.py`
2. Run `python databricks_io.py` to test
3. Import functions into your own scripts
4. Customize for your specific use case
