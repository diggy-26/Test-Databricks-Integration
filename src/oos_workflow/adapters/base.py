"""
Base adapter interfaces for environment-agnostic data access.

This module defines abstract base classes that enable the same workflow code
to run in both local (mocked) and Azure Databricks (production) environments.
"""

from abc import ABC, abstractmethod
from typing import Any


class DataSourceAdapter(ABC):
    """Abstract base class for data source adapters."""
    
    @abstractmethod
    def read_data(self, path: str) -> Any:
        """
        Read data from specified path.
        
        Args:
            path: Data source path (file path for local, Delta table for ADB)
            
        Returns:
            Data structure (pandas DataFrame for local, Spark DataFrame for ADB)
        """
        pass
    
    @abstractmethod
    def write_data(self, data: Any, path: str) -> None:
        """
        Write data to specified path.
        
        Args:
            data: Data to write
            path: Destination path
        """
        pass
    
    @abstractmethod
    def get_environment(self) -> str:
        """
        Get current execution environment.
        
        Returns:
            Environment name ("local" or "databricks")
        """
        pass
