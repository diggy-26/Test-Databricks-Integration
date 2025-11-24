# Databricks Integration Testing

A minimal Python application for testing Databricks workflows with local development support.

## Project Principles

This project follows four core constitutional principles:

1. **Local Development**: Develop, run, and test workflows locally without Databricks connectivity using mocked data sources
2. **Pluggable Execution**: Same codebase runs seamlessly in both local and Databricks environments via adapters
3. **Deterministic Dev & Prod**: Identical Python versions and locked dependencies ensure consistent behavior across environments
4. **Code Quality & Structure**: Clean repository hierarchy (`src/`, `tests/`, `config/`) with pinned dependencies

See [`.specify/memory/constitution.md`](.specify/memory/constitution.md) for complete details.

## Quick Start for Developers

### Prerequisites
- Python 3.11+ (version pinned in `.python-version`)
- uv or poetry for dependency management (`pip install uv`)
- Azure Databricks workspace access (for deployment)
- Databricks CLI installed and configured

### Local Development Setup

```bash
# Install dependencies
uv sync

# Run workflow locally with mocked data (no Databricks required)
uv run python -m oos_workflow.main --env local
```

### Package as Wheel

```bash
# Build Python wheel package
uv build

# Output: dist/oos_workflow-0.1.0-py3-none-any.whl
```

### Deploy to Azure Databricks

```bash
# Authenticate Databricks CLI
databricks configure --token

# Validate DAB bundle configuration
databricks bundle validate

# Deploy to Azure Databricks workspace
databricks bundle deploy --target dev

# Run workflow on ephemeral ADB cluster
databricks bundle run oos_workflow_job --target dev
```

## Project Structure
```
src/oos_workflow/         # Python package
├── main.py               # CLI entry point
├── core/                 # Business logic
└── adapters/             # Environment adapters (local/ADB)
config/                   # Environment configurations (local.yaml, databricks.yaml)
pyproject.toml            # Project metadata and dependencies
uv.lock                   # Locked dependencies for reproducibility
databricks.yml            # Databricks Asset Bundle configuration
.specify/                 # Project governance and specifications
specs/                    # Feature specifications and plans
```

## Development Guidelines

- All dependencies MUST be pinned with exact versions in `uv.lock` or `poetry.lock`
- Workflows MUST run locally without Databricks connectivity (use mock adapters)
- Configuration MUST be externalized in `config/` YAML files (no hardcoded values)
- Code MUST include docstrings and clear documentation
- Changes to dependencies require re-locking: `uv sync` or `poetry lock`

## Architecture Overview

This project uses an **adapter pattern** to enable the same codebase to run in both local and Databricks environments:

- **Core Business Logic** (`src/oos_workflow/core/`): Environment-agnostic workflow implementation
- **Adapters** (`src/oos_workflow/adapters/`): Pluggable implementations for local (mocks) vs. Databricks (real Spark APIs)
- **Configuration** (`config/*.yaml`): Environment-specific settings loaded at runtime
- **Databricks Asset Bundle** (`databricks.yml`): Declarative deployment configuration for jobs, clusters, and artifacts

## Detailed Documentation

- **Feature Specification**: See `specs/001-adb-wheel-package/spec.md` for requirements
- **Implementation Plan**: See `specs/001-adb-wheel-package/plan.md` for technical design
- **Quick Start Guide**: See `specs/001-adb-wheel-package/quickstart.md` for step-by-step setup
- **Research Findings**: See `specs/001-adb-wheel-package/research.md` for technology decisions

For feature development workflow, see `.specify/templates/` for specification, planning, and task templates.

## Troubleshooting

**Wheel build fails**: Ensure Python 3.11+ is active and dependencies are synced (`uv sync`)  
**Local run fails**: Check `config/local.yaml` paths and mock data availability  
**Deployment fails**: Verify Databricks CLI authentication (`databricks workspace list`)  
**Job execution fails**: Review logs in Databricks UI → Workflows → Job → Run → Logs

