# Quick Start: Azure Databricks Wheel Package

**Feature**: 001-adb-wheel-package  
**Date**: 2025-11-24

## Prerequisites

- Python 3.11+ installed
- uv or poetry installed (`pip install uv`)
- Azure Databricks workspace access (for deployment)
- Databricks CLI installed and configured

## Local Development Setup

### 1. Install Dependencies

```bash
# Clone repository
git clone <repository-url>
cd Test-Databricks-Integration

# Checkout feature branch
git checkout 001-adb-wheel-package

# Install dependencies with uv
uv sync

# Or with poetry
poetry install
```

### 2. Run Locally

```bash
# Run with mock data sources
uv run python -m oos_workflow.main --env local

# Or with poetry
poetry run python -m oos_workflow.main --env local
```

**Expected Output**: Workflow executes using local mock adapters, processing sample data from `config/local.yaml`.

## Building the Wheel

```bash
# Build wheel package
uv build

# Or with poetry
poetry build

# Output: dist/oos_workflow-0.1.0-py3-none-any.whl
```

**Verification**:
```bash
# Install wheel locally to test
pip install dist/oos_workflow-0.1.0-py3-none-any.whl

# Run installed package
python -m oos_workflow.main --env local
```

## Deploying to Azure Databricks

### 1. Configure Databricks CLI

```bash
# Authenticate to Azure Databricks workspace
databricks configure --token

# Enter workspace URL: https://adb-<workspace-id>.azuredatabricks.net
# Enter personal access token: <your-token>
```

### 2. Validate DAB Bundle

```bash
# Validate databricks.yml configuration
databricks bundle validate
```

### 3. Deploy to Databricks

```bash
# Deploy bundle to dev environment
databricks bundle deploy --target dev

# This uploads:
# - Wheel artifact to workspace
# - Job configuration
# - Cluster specification
```

### 4. Run Workflow on Databricks

```bash
# Execute job on ephemeral cluster
databricks bundle run oos_workflow_job --target dev

# Or via Databricks UI:
# Navigate to Workflows → oos_workflow_job → Run Now
```

### 5. Monitor Execution

```bash
# View job runs
databricks jobs runs list --job-id <job-id>

# View logs for specific run
databricks runs get-output --run-id <run-id>
```

## Project Structure Overview

```
src/oos_workflow/         # Main package
├── main.py               # CLI entry point
├── core/workflow.py      # Business logic
└── adapters/             # Environment adapters
    ├── local.py          # Local mock implementation
    └── databricks.py     # ADB implementation

config/
├── local.yaml            # Local dev config
└── databricks.yaml       # ADB config

pyproject.toml            # Dependencies and metadata
uv.lock                   # Locked dependencies
databricks.yml            # DAB deployment config
```

## Common Commands Reference

```bash
# Development
uv sync                   # Install/update dependencies
uv run python -m oos_workflow.main --env local  # Run locally

# Building
uv build                  # Create wheel package

# Deployment
databricks bundle validate       # Check DAB config
databricks bundle deploy --target dev    # Deploy to dev
databricks bundle run oos_workflow_job --target dev  # Run job

# Troubleshooting
databricks workspace list /Workspace/   # List workspace files
databricks fs ls dbfs:/               # List DBFS files
```

## Troubleshooting

### Wheel Build Fails
- Ensure `pyproject.toml` is valid: `uv sync` should complete without errors
- Check Python version matches `.python-version` file

### Deployment Fails
- Verify Databricks CLI authentication: `databricks workspace list`
- Check `databricks.yml` syntax: `databricks bundle validate`
- Ensure wheel path in `databricks.yml` matches build output

### Job Execution Fails
- Review job logs in Databricks UI: Workflows → Job → Run → Logs
- Verify cluster configuration supports Python 3.11+
- Check `config/databricks.yaml` paths are accessible

## Next Steps

After successful deployment:

1. **Customize Workflow**: Edit `src/oos_workflow/core/workflow.py` with actual business logic
2. **Add Dependencies**: Update `pyproject.toml` and run `uv sync` to lock
3. **Configure Environments**: Add production target in `databricks.yml`
4. **CI/CD Integration**: Set up automated wheel building and deployment

## Resources

- [uv Documentation](https://github.com/astral-sh/uv)
- [Databricks Asset Bundles](https://docs.databricks.com/en/dev-tools/bundles/)
- [Python Packaging](https://packaging.python.org/)
