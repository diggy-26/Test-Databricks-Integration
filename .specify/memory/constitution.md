<!--
SYNC IMPACT REPORT - 2025-11-24
Version Change: NEW → 1.0.0 (Initial Constitution)
Modified Principles: N/A (Initial version)
Added Sections:
  - Core Principles (4 principles: Local Development, Pluggable Execution, Deterministic Dev & Prod, Code Quality & Structure)
  - Development Standards
  - Testing Requirements
  - Governance
Removed Sections: N/A
Templates Status:
  ✅ plan-template.md - validated for consistency
  ✅ spec-template.md - validated for consistency
  ✅ tasks-template.md - validated for consistency
Follow-up TODOs: None
-->

# Databricks Integration Testing Constitution

## Core Principles

### I. Local Development
Developers MUST be able to develop, run, and test workflows locally without requiring Databricks connectivity. All real data sources (Delta tables, cloud storage, APIs) MUST be mockable during local development.

**Rationale**: Local development enables fast iteration, reduces cloud costs, eliminates network dependencies, and allows developers to work offline. This principle prevents "works in Databricks only" situations and ensures developers can test logic independently.

**Implementation Requirements**:
- Mock implementations for all Databricks-specific APIs (Delta tables, dbutils, Spark)
- Local test data fixtures that simulate production data structures
- Environment-based configuration switching (local vs. Databricks)
- Clear documentation for local setup and running tests

### II. Pluggable Execution Inside Databricks
The workflow MUST be deployable and executable inside Databricks with minimal friction. The same codebase MUST run seamlessly in both local and Databricks environments through pluggable adapters or dependency injection.

**Rationale**: Production deployments require Databricks execution against real Delta tables. Pluggable design ensures the core business logic remains unchanged while execution context adapts to the environment.

**Implementation Requirements**:
- Clear separation between business logic and infrastructure/platform code
- Adapter pattern or dependency injection for data sources
- Configuration-driven environment switching (no code changes between environments)
- Single source of truth for workflow definitions

### III. Deterministic Dev & Prod
Local and production runs MUST behave consistently. This requires identical Python versions, locked dependencies, and version-controlled code. No "works on my machine" situations are acceptable.

**Rationale**: Environment parity eliminates bugs caused by version mismatches, ensures reproducible builds, and maintains confidence that local testing validates production behavior.

**Implementation Requirements**:
- Pinned Python version (specified in `.python-version`, `pyproject.toml`, or Databricks cluster config)
- Locked dependencies using `requirements.txt` with pinned versions or `poetry.lock`/`Pipfile.lock`
- Version control for all code, configuration, and infrastructure definitions
- Identical library versions between local and Databricks environments
- CI/CD validation that dependencies match across environments

### IV. Code Quality & Structure
The repository MUST maintain a clean, maintainable hierarchy with clear separation of concerns. Standard Python project structure with `src/`, `tests/`, lockfiles, and configuration files is mandatory.

**Rationale**: Consistent structure improves maintainability, onboarding, and long-term project health. Proper organization prevents technical debt and enables team scalability.

**Implementation Requirements**:
- Standard directory structure:
  ```
  src/           # Source code (business logic, workflows, utilities)
  tests/         # Test suites (unit, integration, contract)
  config/        # Configuration files (local, dev, prod)
  requirements.txt or pyproject.toml  # Dependency management
  .python-version  # Python version specification
  README.md      # Setup and usage documentation
  ```
- Clear module organization with descriptive naming
- Separation of business logic from infrastructure code
- No hardcoded credentials or environment-specific values in source code
- Comprehensive README with setup, testing, and deployment instructions

## Development Standards

### Dependency Management
- ALL dependencies MUST be pinned with exact versions (e.g., `pandas==2.1.3`, not `pandas>=2.0`)
- Dependency files MUST be version-controlled
- Any new dependency MUST be justified and approved

### Configuration Management
- Environment-specific configuration MUST be externalized (environment variables, config files)
- Local-only configuration files (e.g., `.env.local`) MUST NOT be committed to version control
- Configuration schema MUST be documented

### Documentation Requirements
- README MUST include:
  - Local setup instructions
  - How to run tests locally
  - How to deploy to Databricks
  - Architecture overview showing pluggable components
- Code MUST include docstrings for public functions and classes
- Any non-obvious design decisions MUST be documented

## Testing Requirements

### Test Coverage
- Core business logic MUST have unit tests
- Integration tests MUST validate local-to-Databricks consistency
- Mock implementations MUST be tested to ensure they simulate real behavior accurately

### Test Organization
```
tests/
├── unit/           # Fast, isolated tests (no external dependencies)
├── integration/    # Tests with mocked Databricks components
└── fixtures/       # Shared test data
```

### Test Execution
- Tests MUST run locally without Databricks connectivity
- CI/CD pipeline MUST run all tests on every commit
- Test failures block deployment

## Governance

### Amendment Process
1. Proposed amendments MUST be documented with rationale
2. Team review and approval required
3. Version increment according to semantic versioning:
   - **MAJOR**: Backward incompatible principle changes (e.g., removing a core principle)
   - **MINOR**: New principle additions or material expansions
   - **PATCH**: Clarifications, wording improvements, typo fixes

### Compliance Verification
- All pull requests MUST include a constitution compliance check
- Feature specifications MUST reference relevant constitutional principles
- Technical decisions that violate principles MUST be explicitly justified and documented

### Version Control
This constitution is version-controlled and follows semantic versioning. All changes are tracked in git history and in the Sync Impact Report HTML comment at the top of this file.

**Version**: 1.0.0 | **Ratified**: 2025-11-24 | **Last Amended**: 2025-11-24
