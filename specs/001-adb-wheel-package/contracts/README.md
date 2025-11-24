# API Contracts

**Feature**: 001-adb-wheel-package  
**Date**: 2025-11-24  
**Status**: N/A

## Overview

This application does not expose REST APIs, GraphQL endpoints, or external interfaces. It is a standalone workflow package that executes within Azure Databricks clusters.

## Internal Module Contracts

### Adapter Interface

**Module**: `src/oos_workflow/adapters/base.py`

**Purpose**: Abstract interface for environment-specific implementations

```python
from abc import ABC, abstractmethod
from typing import Any

class DataSourceAdapter(ABC):
    """Abstract base class for data source adapters"""
    
    @abstractmethod
    def read_data(self, path: str) -> Any:
        """
        Read data from specified path
        
        Args:
            path: Data source path (file path or Delta table)
            
        Returns:
            Data structure (pandas DataFrame for local, Spark DataFrame for ADB)
        """
        pass
    
    @abstractmethod
    def write_data(self, data: Any, path: str) -> None:
        """
        Write data to specified path
        
        Args:
            data: Data to write
            path: Destination path
        """
        pass
```

### CLI Entry Point

**Module**: `src/oos_workflow/main.py`

**Purpose**: Command-line entry point for workflow execution

**Arguments**:
- `--env`: Environment name ("local" or "databricks")
- `--config`: Path to configuration file (optional, defaults based on env)

**Exit Codes**:
- `0`: Success
- `1`: Configuration error
- `2`: Execution error

**Example Usage**:
```bash
# Local execution
python -m oos_workflow.main --env local

# Databricks execution (invoked by DAB)
python -m oos_workflow.main --env databricks
```

## Configuration File Schema

### Local Configuration (`config/local.yaml`)

```yaml
environment: local
data_source:
  type: local
  path: ./data/sample.csv
```

### Databricks Configuration (`config/databricks.yaml`)

```yaml
environment: databricks
data_source:
  type: delta
  path: /mnt/data/table_name
```

## No External APIs

This application is self-contained and does not expose or consume external HTTP/REST APIs.
