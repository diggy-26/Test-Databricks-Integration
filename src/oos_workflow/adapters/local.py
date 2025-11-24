"""
Local adapter implementation using pandas for mock data sources.

This adapter enables local development and testing without Azure Databricks connectivity.
"""

import pandas as pd
from pathlib import Path
from typing import Any

from oos_workflow.adapters.base import DataSourceAdapter


class LocalDataSource(DataSourceAdapter):
    """Local data source adapter using pandas DataFrames."""
    
    def __init__(self):
        """Initialize local data source adapter."""
        self.environment = "local"
    
    def read_data(self, path: str) -> pd.DataFrame:
        """
        Read data from local file path.
        
        Args:
            path: Local file path (CSV, JSON, etc.)
            
        Returns:
            pandas DataFrame with loaded data
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format is unsupported
        """
        path_obj = Path(path)
        
        if not path_obj.exists():
            raise FileNotFoundError(f"Data file not found: {path}")
        
        # Determine file type and read accordingly
        if path_obj.suffix == '.csv':
            return pd.read_csv(path)
        elif path_obj.suffix == '.json':
            return pd.read_json(path)
        elif path_obj.suffix in ['.xlsx', '.xls']:
            return pd.read_excel(path)
        else:
            raise ValueError(f"Unsupported file format: {path_obj.suffix}")
    
    def write_data(self, data: pd.DataFrame, path: str) -> None:
        """
        Write data to local file path.
        
        Args:
            data: pandas DataFrame to write
            path: Destination file path
        """
        path_obj = Path(path)
        
        # Create parent directory if needed
        path_obj.parent.mkdir(parents=True, exist_ok=True)
        
        # Write based on file extension
        if path_obj.suffix == '.csv':
            data.to_csv(path, index=False)
        elif path_obj.suffix == '.json':
            data.to_json(path, orient='records', indent=2)
        elif path_obj.suffix in ['.xlsx', '.xls']:
            data.to_excel(path, index=False)
        else:
            # Default to CSV
            data.to_csv(path, index=False)
    
    def get_environment(self) -> str:
        """
        Get current execution environment.
        
        Returns:
            "local"
        """
        return self.environment
