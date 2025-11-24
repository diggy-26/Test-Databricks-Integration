"""
CLI entry point for oos-workflow package.

This module provides the command-line interface for running workflows
in different environments (local or Azure Databricks).
"""

import argparse
import sys
from pathlib import Path

from oos_workflow.core.config import load_config
from oos_workflow.core.workflow import Workflow


def create_adapter(environment: str, config: dict):
    """
    Create appropriate adapter based on environment.
    
    Args:
        environment: Environment name ("local" or "databricks")
        config: Configuration dictionary
        
    Returns:
        DataSourceAdapter instance
    """
    if environment == "local":
        from oos_workflow.adapters.local import LocalDataSource
        return LocalDataSource()
    elif environment == "databricks":
        from oos_workflow.adapters.databricks import DatabricksDataSource
        return DatabricksDataSource()
    else:
        raise ValueError(f"Unknown environment: {environment}")


def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="Run oos-workflow in specified environment"
    )
    parser.add_argument(
        "--env",
        choices=["local", "databricks"],
        default="local",
        help="Execution environment (default: local)"
    )
    parser.add_argument(
        "--config",
        type=str,
        help="Path to configuration file (optional, defaults to config/{env}.yaml)"
    )
    
    args = parser.parse_args()
    
    try:
        # Load configuration
        print(f"Loading configuration for {args.env} environment...")
        config = load_config(args.env)
        
        # Create adapter
        adapter = create_adapter(args.env, config)
        
        # Initialize and run workflow
        workflow = Workflow(adapter)
        result = workflow.run(config)
        
        # Print results
        print("\n" + "="*50)
        print("Workflow Results:")
        for key, value in result.items():
            print(f"  {key}: {value}")
        print("="*50)
        
        # Exit with appropriate code
        sys.exit(0 if result.get("status") == "success" else 1)
        
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
