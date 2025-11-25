"""
oos-workflow: Simple Python workflow package for Azure Databricks testing.

This package demonstrates packaging Python applications as wheels and deploying
to Azure Databricks using Databricks Asset Bundles (DAB).
"""

__version__ = "0.2.0"


def main():
    """Entry point wrapper for Databricks."""
    from .main import main as _main
    return _main()


__all__ = ["__version__", "main"]
