"""
Core workflow logic - environment-agnostic business logic.

This module contains the main workflow implementation that works with
any DataSourceAdapter (local or Databricks).
"""

from typing import Any

from oos_workflow.adapters.base import DataSourceAdapter


class Workflow:
    """Main workflow implementation using adapter pattern."""
    
    def __init__(self, adapter: DataSourceAdapter):
        """
        Initialize workflow with data source adapter.
        
        Args:
            adapter: DataSourceAdapter implementation (local or Databricks)
        """
        self.adapter = adapter
        self.environment = adapter.get_environment()
    
    def run(self, config: dict) -> dict:
        """
        Execute the workflow.
        
        Args:
            config: Configuration dictionary from YAML file
            
        Returns:
            Workflow execution results
        """
        print(f"🚀 Starting workflow in {self.environment} environment")
        
        # Extract data source configuration
        data_source_config = config.get("data_source", {})
        data_path = data_source_config.get("path")
        
        if not data_path:
            raise ValueError("Data source path not specified in configuration")
        
        # Read data using adapter
        print(f"📖 Reading data from: {data_path}")
        try:
            data = self.adapter.read_data(data_path)
            print(f"✅ Successfully loaded data")
            
            # Simple processing: count records
            if hasattr(data, '__len__'):
                record_count = len(data)
            else:
                record_count = data.count() if hasattr(data, 'count') else 0
            
            print(f"📊 Processed {record_count} records")
            
            result = {
                "status": "success",
                "environment": self.environment,
                "records_processed": record_count,
                "data_source": data_path
            }
            
            print(f"✨ Workflow completed successfully")
            return result
            
        except Exception as e:
            print(f"❌ Workflow failed: {e}")
            return {
                "status": "error",
                "environment": self.environment,
                "error": str(e)
            }
