"""
Configuration loader utility for YAML-based environment configurations.
"""

import os
from pathlib import Path
from typing import Any, Dict
import yaml


class ConfigurationError(Exception):
    """Raised when configuration loading or validation fails."""
    pass


class ConfigLoader:
    """Loads and validates YAML configuration files."""
    
    def __init__(self, config_dir: str = "config", allow_missing: bool = False):
        """
        Initialize configuration loader.
        
        Args:
            config_dir: Directory containing configuration files
            allow_missing: If True, use default configs when directory is missing
        """
        self.config_dir = Path(config_dir)
        self.allow_missing = allow_missing
        if not self.config_dir.exists() and not allow_missing:
            raise ConfigurationError(f"Configuration directory not found: {config_dir}")
    
    def load(self, environment: str) -> Dict[str, Any]:
        """
        Load configuration for specified environment.
        
        Args:
            environment: Environment name (e.g., "local", "databricks")
            
        Returns:
            Configuration dictionary
            
        Raises:
            ConfigurationError: If configuration file not found or invalid
        """
        config_file = self.config_dir / f"{environment}.yaml"
        
        if not config_file.exists():
            if self.allow_missing:
                print(f"⚠️  Config file not found, using defaults for {environment}")
                return self._get_default_config(environment)
            raise ConfigurationError(f"Configuration file not found: {config_file}")
        
        try:
            with open(config_file, 'r') as f:
                config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ConfigurationError(f"Invalid YAML in {config_file}: {e}")
        
        # Validate required fields
        self._validate_config(config, environment)
        
        return config
    
    def _validate_config(self, config: Dict[str, Any], environment: str) -> None:
        """
        Validate configuration schema.
        
        Args:
            config: Configuration dictionary
            environment: Environment name
            
        Raises:
            ConfigurationError: If required fields are missing
        """
        if not isinstance(config, dict):
            raise ConfigurationError("Configuration must be a dictionary")
        
        # Check required top-level fields
        if "environment" not in config:
            raise ConfigurationError("Missing required field: environment")
        
        if config["environment"] != environment:
            raise ConfigurationError(
                f"Environment mismatch: expected '{environment}', got '{config['environment']}'"
            )
        
        if "data_source" not in config:
            raise ConfigurationError("Missing required field: data_source")
        
        # Validate data_source structure
        data_source = config["data_source"]
        if not isinstance(data_source, dict):
            raise ConfigurationError("data_source must be a dictionary")
        
        if "type" not in data_source:
            raise ConfigurationError("Missing required field: data_source.type")
        
        if "path" not in data_source:
            raise ConfigurationError("Missing required field: data_source.path")
    
    def _get_default_config(self, environment: str) -> Dict[str, Any]:
        """
        Generate default configuration for environment.
        
        Args:
            environment: Environment name
            
        Returns:
            Default configuration dictionary
        """
        if environment == "local":
            return {
                "environment": "local",
                "data_source": {
                    "type": "csv",
                    "path": "config/data/sample.csv"
                },
                "output": {
                    "display": True
                }
            }
        elif environment == "databricks":
            return {
                "environment": "databricks",
                "data_source": {
                    "type": "delta",
                    "path": "/tmp/sample_data"
                },
                "output": {
                    "display": True,
                    "save_to": "/tmp/workflow_output"
                }
            }
        else:
            raise ConfigurationError(f"No default config available for environment: {environment}")


def load_config(environment: str, config_dir: str = "config", allow_missing: bool = True) -> Dict[str, Any]:
    """
    Convenience function to load configuration.
    
    Args:
        environment: Environment name
        config_dir: Configuration directory path
        allow_missing: If True, use default configs when directory/files are missing
        
    Returns:
        Configuration dictionary
    """
    loader = ConfigLoader(config_dir, allow_missing=allow_missing)
    return loader.load(environment)
