# Research: Azure Databricks Wheel Package

**Feature**: 001-adb-wheel-package  
**Date**: 2025-11-24  
**Status**: Complete

## Overview

This document consolidates research findings for building a Python wheel package deployable to Azure Databricks using Databricks Asset Bundles (DAB), with support for local development and deterministic dependency management.

## Research Areas

### 1. Python Dependency Management: uv vs Poetry

**Decision**: Use **uv** as primary tool (with poetry as fallback option)

**Rationale**:
- **uv**: Rust-based, extremely fast dependency resolution and locking. Native support for `pyproject.toml` standard. Lockfile (`uv.lock`) ensures reproducibility. Growing adoption in Python ecosystem.
- **poetry**: Mature, widely adopted, similar lockfile capabilities (`poetry.lock`). Slightly slower but proven in production.

**Best Practices**:
- Pin Python version in both `.python-version` (for tool detection) and `pyproject.toml` (for metadata)
- Use exact version pinning in `pyproject.toml` dependencies: `pyspark = "3.5.0"` not `pyspark = "^3.5"`
- Commit lock files to version control
- CI/CD should install from lock file: `uv sync` or `poetry install --sync`

**Implementation**:
```toml
# pyproject.toml
[project]
name = "oos-workflow"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "pyspark==3.5.0",
]

[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.build_meta"
```

### 2. Python Wheel Packaging

**Decision**: Use **setuptools** with `pyproject.toml` configuration

**Rationale**:
- Standard Python packaging tool, widely compatible
- No separate `setup.py` needed with modern `pyproject.toml`
- Wheels are platform-independent for pure Python packages
- Compatible with pip and Databricks cluster install mechanisms

**Best Practices**:
- Source layout: place package under `src/` directory
- Use `python -m build` or `uv build` to generate wheel
- Wheel naming: `{name}-{version}-py3-none-any.whl`
- Include package data via `MANIFEST.in` if needed

**Build Commands**:
```bash
# Using uv
uv build

# Using standard build tool
python -m build

# Result: dist/oos_workflow-0.1.0-py3-none-any.whl
```

### 3. Databricks Asset Bundles (DAB)

**Decision**: Use DAB for deployment orchestration

**Rationale**:
- Native Databricks deployment framework
- Declarative YAML configuration for jobs, clusters, artifacts
- Supports Git integration for versioning
- Handles dependency installation and artifact management
- Enables ephemeral cluster provisioning

**Best Practices**:
- Define `databricks.yml` at repository root
- Specify wheel artifact path and installation method
- Configure job clusters (ephemeral) not shared clusters
- Use Git commit references for traceability
- Separate environments (dev/prod) via targets

**DAB Configuration Structure**:
```yaml
# databricks.yml
bundle:
  name: oos-workflow

artifacts:
  default:
    type: whl
    path: dist/oos_workflow-0.1.0-py3-none-any.whl

resources:
  jobs:
    oos_workflow_job:
      name: "OOS Workflow Job"
      job_clusters:
        - job_cluster_key: "oos_cluster"
          new_cluster:
            spark_version: "13.3.x-scala2.12"
            node_type_id: "Standard_DS3_v2"
            num_workers: 1
            spark_conf:
              "spark.databricks.cluster.profile": "singleNode"
      tasks:
        - task_key: "run_workflow"
          job_cluster_key: "oos_cluster"
          python_wheel_task:
            package_name: "oos_workflow"
            entry_point: "main"
          libraries:
            - whl: "../artifacts/default/dist/oos_workflow-0.1.0-py3-none-any.whl"

targets:
  dev:
    workspace:
      host: https://adb-<workspace-id>.azuredatabricks.net
```

**Deployment Commands**:
```bash
# Validate bundle
databricks bundle validate

# Deploy to dev environment
databricks bundle deploy --target dev

# Run job
databricks bundle run oos_workflow_job --target dev
```

### 4. Local Development with Mocks

**Decision**: Adapter pattern for environment abstraction

**Rationale**:
- Decouple business logic from Spark/Databricks APIs
- Enable local testing without cluster connectivity
- Maintain single codebase for all environments

**Best Practices**:
- Define abstract base interfaces in `adapters/base.py`
- Implement local mocks in `adapters/local.py` using in-memory data structures
- Implement ADB connectors in `adapters/databricks.py` using real Spark APIs
- Use configuration files to select adapter at runtime
- Document mock limitations (e.g., simplified data schemas)

**Adapter Pattern Example**:
```python
# adapters/base.py
from abc import ABC, abstractmethod

class DataSourceAdapter(ABC):
    @abstractmethod
    def read_data(self, path: str):
        pass

# adapters/local.py
class LocalDataSource(DataSourceAdapter):
    def read_data(self, path: str):
        # Return pandas DataFrame from CSV
        import pandas as pd
        return pd.read_csv(path)

# adapters/databricks.py
class DatabricksDataSource(DataSourceAdapter):
    def __init__(self, spark):
        self.spark = spark
    
    def read_data(self, path: str):
        # Return Spark DataFrame from Delta table
        return self.spark.read.format("delta").load(path)
```

### 5. Configuration Management

**Decision**: YAML configuration files per environment

**Rationale**:
- Human-readable format
- Standard in Python ecosystem
- Easy to version control and diff
- Supports complex nested structures

**Best Practices**:
- Store configs in `config/` directory
- Environment-specific files: `local.yaml`, `databricks.yaml`
- Never commit credentials (use environment variables or Azure Key Vault)
- Validate configuration schema on load

**Configuration Structure**:
```yaml
# config/local.yaml
environment: local
data_source:
  type: local
  path: ./data/sample.csv

# config/databricks.yaml
environment: databricks
data_source:
  type: delta
  path: /mnt/data/production/table
cluster:
  spark_version: "13.3.x-scala2.12"
```

### 6. CI/CD Integration

**Decision**: Standard Python build workflow

**Rationale**:
- Wheel building is deterministic with locked dependencies
- Can be integrated into any CI system (GitHub Actions, Azure DevOps)
- Artifact storage compatible with Databricks workspace uploads

**Best Practices**:
- Install dependencies from lock file
- Build wheel in CI pipeline
- Store wheel as build artifact
- Validate wheel installation in test stage
- Deploy via DAB CLI in release stage

**CI Workflow Outline**:
```yaml
# .github/workflows/build.yml (example)
jobs:
  build:
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install uv
      - run: uv sync
      - run: uv build
      - uses: actions/upload-artifact@v3
        with:
          name: wheel
          path: dist/*.whl
```

## Alternatives Considered

### Dependency Management
- **pip-tools**: Rejected - less modern than uv/poetry, manual compilation steps
- **conda**: Rejected - heavier than needed for simple package, less common in pure Python projects

### Packaging
- **flit**: Rejected - simpler but less flexible for complex builds
- **hatchling**: Rejected - newer, less mature ecosystem

### Deployment
- **Manual upload**: Rejected - no version control, no cluster management, error-prone
- **Terraform**: Rejected - overkill for simple job definitions, DAB is Databricks-native

## Implementation Checklist

- [ ] Initialize project with `uv init` or `poetry init`
- [ ] Create `src/oos_workflow/` package structure
- [ ] Implement adapter base classes and local/databricks implementations
- [ ] Create YAML configuration files for local and ADB environments
- [ ] Configure `pyproject.toml` with metadata and dependencies
- [ ] Pin Python version in `.python-version`
- [ ] Create `databricks.yml` with job and cluster definitions
- [ ] Test local wheel build with `uv build`
- [ ] Document build and deployment process in README
- [ ] Validate DAB bundle with `databricks bundle validate`

## References

- [uv documentation](https://github.com/astral-sh/uv)
- [Python Packaging Guide](https://packaging.python.org/)
- [Databricks Asset Bundles](https://docs.databricks.com/en/dev-tools/bundles/index.html)
- [PEP 621 - Project Metadata](https://peps.python.org/pep-0621/)
