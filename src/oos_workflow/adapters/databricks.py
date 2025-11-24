"""
Databricks adapter implementation using PySpark for real data sources.

This adapter enables production execution on Azure Databricks clusters
with real Spark DataFrames and Delta tables.
"""

from typing import Any

from oos_workflow.adapters.base import DataSourceAdapter


class DatabricksDataSource(DataSourceAdapter):
    """Databricks data source adapter using PySpark."""
    
    def __init__(self):
        """
        Initialize Databricks data source adapter.
        
        Automatically detects Spark session in Databricks environment.
        """
        self.environment = "databricks"
        self.spark = self._get_spark_session()
    
    def _get_spark_session(self):
        """
        Get or create Spark session.
        
        Returns:
            SparkSession instance
        """
        try:
            from pyspark.sql import SparkSession
            
            # In Databricks, spark session is pre-initialized
            # Try to get existing session first
            spark = SparkSession.builder.getOrCreate()
            return spark
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Spark session: {e}")
    
    def read_data(self, path: str) -> Any:
        """
        Read data from Databricks data source.
        
        Args:
            path: Data source path (Delta table path or DBFS path)
            
        Returns:
            Spark DataFrame with loaded data
        """
        # Check if path is a Delta table or regular file
        if path.startswith("/mnt/") or path.startswith("dbfs:/"):
            # DBFS path - try Delta format first, fall back to parquet
            try:
                return self.spark.read.format("delta").load(path)
            except:
                return self.spark.read.parquet(path)
        elif "." in path.split("/")[-1]:
            # File with extension
            ext = path.split(".")[-1].lower()
            if ext == "csv":
                return self.spark.read.csv(path, header=True, inferSchema=True)
            elif ext == "json":
                return self.spark.read.json(path)
            elif ext == "parquet":
                return self.spark.read.parquet(path)
            else:
                # Default to Delta
                return self.spark.read.format("delta").load(path)
        else:
            # Assume Delta table
            return self.spark.read.format("delta").load(path)
    
    def write_data(self, data: Any, path: str) -> None:
        """
        Write data to Databricks data source.
        
        Args:
            data: Spark DataFrame to write
            path: Destination path (Delta table or DBFS path)
        """
        # Default to Delta format for Databricks
        data.write.format("delta").mode("overwrite").save(path)
    
    def get_environment(self) -> str:
        """
        Get current execution environment.
        
        Returns:
            "databricks"
        """
        return self.environment
