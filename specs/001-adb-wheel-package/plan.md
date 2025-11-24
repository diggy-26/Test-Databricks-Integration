# Implementation Plan: Azure Databricks Wheel Package

**Branch**: `001-adb-wheel-package` | **Date**: 2025-11-24 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-adb-wheel-package/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build a simple Python application packaged as a wheel and deployable to Azure Databricks using Databricks Asset Bundles (DAB). The solution uses uv/poetry for deterministic dependency locking, generates wheel artifacts in CI, and deploys to ADB with DAB configuration defining job specs, cluster configuration, and dependency installation. Local development is supported with mocks, while production runs execute on ephemeral dedicated ADB clusters.

## Technical Context

**Language/Version**: Python 3.11+ (pinned in pyproject.toml)  
**Primary Dependencies**: 
  - uv or poetry (dependency management and locking)
  - setuptools/wheel (Python packaging)
  - databricks-cli (DAB deployment)
  - pyspark (runtime on ADB, dev mocks locally)
**Storage**: N/A (simple feasibility test application)  
**Testing**: Not required per specification (feasibility testing only)  
**Target Platform**: Azure Databricks clusters (ephemeral, DAB-managed)
**Project Type**: Single Python package  
**Performance Goals**: N/A (simple test application)  
**Constraints**: 
  - Must support local development without ADB connectivity
  - Wheel must be buildable in CI/CD pipelines
  - DAB bundle must be deployable to ADB workspace
  - Compatible with ADB cluster Python runtime (3.8+)
**Scale/Scope**: Minimal viable package for testing ADB integration patterns

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **Local Development**: ✅ PASS - Adapter pattern enables local execution with mock implementations of Spark/dbutils. Configuration yaml files switch between local and ADB contexts. Developers can run `uv run python -m oos_workflow.main --env local` without ADB access.

- [x] **Pluggable Execution**: ✅ PASS - Core workflow logic is isolated from infrastructure. Adapters (local.py vs databricks.py) provide pluggable data source implementations. Single codebase deploys to both environments via configuration, not code changes.

- [x] **Deterministic Dev & Prod**: ✅ PASS - Python 3.11 pinned in `.python-version` and `pyproject.toml`. Dependencies locked via `uv.lock` or `poetry.lock`. DAB configuration (`databricks.yml`) version-controlled with git commit reference. Wheel artifact built from locked dependencies ensures identical libraries.

- [⚠️] **Code Quality & Structure**: ⚠️ PARTIAL - Follows `src/`, `config/` hierarchy. No `tests/` directory per specification (feasibility testing only). Dependencies pinned in lock file. README will document setup/build/deploy. **Justification**: Test exclusion explicitly requested in spec for minimal feasibility validation.

*Note: Test directory omission documented as intentional scope reduction for feasibility testing phase.*

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
src/
└── oos_workflow/         # Main package (example name: out-of-scope workflow)
    ├── __init__.py       # Package initialization
    ├── main.py           # Entry point for workflow
    ├── core/             # Core business logic
    │   ├── __init__.py
    │   └── workflow.py   # Workflow implementation
    └── adapters/         # Environment adapters (local vs ADB)
        ├── __init__.py
        ├── base.py       # Abstract interfaces
        ├── local.py      # Local mock implementations
        └── databricks.py # ADB-specific implementations

config/
├── local.yaml            # Local development config
└── databricks.yaml       # ADB-specific config

pyproject.toml            # Project metadata + dependencies (uv/poetry)
uv.lock or poetry.lock    # Locked dependencies
.python-version           # Python version pinning
databricks.yml            # Databricks Asset Bundle configuration
.gitignore                # Exclude dist/, .venv/, etc.
README.md                 # Setup, build, deploy instructions

dist/                     # Generated wheel files (gitignored)
.venv/                    # Virtual environment (gitignored)
```

**Structure Decision**: Single Python package layout following constitutional requirements. The `src/` directory contains the main package with clear separation between core logic and environment-specific adapters. DAB configuration (`databricks.yml`) defines deployment infrastructure. No tests directory per specification requirements.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| No tests directory | Feasibility testing phase - explicit requirement in spec | Full test suite would delay validation of core packaging/deployment workflow |

**Note**: Single documented deviation (test directory omission) is intentional for rapid feasibility validation. Future iterations should add comprehensive test coverage per constitutional requirement IV.

## Post-Design Constitution Re-evaluation

After completing Phase 0 (Research) and Phase 1 (Design):

- ✅ **Local Development**: Design confirms adapter pattern with local/databricks implementations. Mock adapters enable full local workflow execution.
- ✅ **Pluggable Execution**: Architecture separates core logic from infrastructure. Configuration-driven adapter selection at runtime.
- ✅ **Deterministic Dev & Prod**: uv.lock/poetry.lock ensures exact dependency matching. DAB bundle references git commits for traceability.
- ⚠️ **Code Quality & Structure**: Clean hierarchy maintained. Test omission remains documented exception.

**Final Status**: Ready for implementation (Phase 2: Tasks generation via `/speckit.tasks`)

## Implementation Notes

### Key Technology Decisions
1. **uv** for dependency management (fast, modern, lockfile support)
2. **setuptools** for wheel building (standard, compatible)
3. **Databricks Asset Bundles** for deployment orchestration
4. **Adapter pattern** for environment abstraction
5. **YAML** for configuration management

### Critical Path
1. Setup project structure with `src/oos_workflow/` package
2. Implement adapter base classes and local/databricks implementations
3. Create configuration files for local and ADB environments
4. Configure `pyproject.toml` and pin dependencies
5. Define `databricks.yml` with job and cluster specs
6. Test local wheel build and installation
7. Validate DAB bundle configuration
8. Deploy to Azure Databricks dev environment
9. Document build/deploy process in README

### Risks & Mitigations
- **Risk**: DAB configuration complexity → **Mitigation**: Start with minimal job config from research examples
- **Risk**: Dependency conflicts on ADB cluster → **Mitigation**: Pin exact versions, test wheel install locally first
- **Risk**: Mock adapters don't accurately reflect ADB behavior → **Mitigation**: Keep business logic simple, document adapter limitations

---

**Plan Status**: ✅ COMPLETE - Ready for `/speckit.tasks` command to generate implementation tasks
