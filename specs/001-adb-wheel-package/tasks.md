# Tasks: Azure Databricks Wheel Package

**Branch**: `001-adb-wheel-package` | **Feature**: Azure Databricks Wheel Package  
**Input**: Design documents from `specs/001-adb-wheel-package/`  
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: No test tasks included per specification requirements (feasibility testing only).

**Organization**: Tasks grouped by user story to enable independent implementation and testing.

## Format: `- [ ] [ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

Repository uses single project structure: `src/`, `config/` at root.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and dependency management

- [X] T001 Create `.python-version` file with Python 3.11 specification
- [X] T002 Create `pyproject.toml` with project metadata (name: oos-workflow, version: 0.1.0, requires-python >=3.11)
- [X] T003 [P] Add build-system configuration to `pyproject.toml` (setuptools>=68.0 backend)
- [X] T004 [P] Create `.gitignore` excluding dist/, .venv/, __pycache__, *.pyc, uv.lock or poetry.lock (keep in VCS)
- [X] T005 Initialize uv project with `uv init` and install base dependencies
- [X] T006 [P] Create `src/oos_workflow/__init__.py` with package version metadata
- [X] T007 [P] Create `config/` directory for environment configurations

**Checkpoint**: Basic project structure ready - user story implementation can begin

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core adapter framework that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until adapters are defined

- [X] T008 Create abstract adapter interface in `src/oos_workflow/adapters/base.py` with DataSourceAdapter class
- [X] T009 [P] Create `src/oos_workflow/adapters/__init__.py` exporting base adapters
- [X] T010 [P] Create `src/oos_workflow/core/__init__.py` for business logic module
- [X] T011 Create configuration loader utility in `src/oos_workflow/core/config.py` (reads YAML, validates schema)

**Checkpoint**: Foundation ready - user story implementation can now proceed in parallel

---

## Phase 3: User Story 1 - Package Application as Wheel (Priority: P1) 🎯 MVP

**Goal**: Build distributable Python wheel with all package metadata and source files

**Independent Test**: Run `uv build`, verify `.whl` file created in `dist/`, install locally with `pip install dist/*.whl`, import package successfully

### Implementation for User Story 1

- [X] T012 [P] [US1] Create local adapter implementation in `src/oos_workflow/adapters/local.py` (mock DataSourceAdapter using pandas)
- [X] T013 [P] [US1] Create `config/local.yaml` with environment: local, data_source config (type: local, path: ./data/sample.csv)
- [X] T014 [US1] Implement core workflow logic in `src/oos_workflow/core/workflow.py` (uses adapter pattern, env-agnostic)
- [X] T015 [US1] Create CLI entry point in `src/oos_workflow/main.py` with --env argument, loads config, initializes adapters
- [X] T016 [US1] Add pyspark dependency to `pyproject.toml` dependencies list with pinned version
- [X] T017 [US1] Run `uv sync` to generate `uv.lock` lockfile with pinned dependencies
- [X] T018 [US1] Build wheel package with `uv build` command
- [X] T019 [US1] Validate wheel contents (check dist/oos_workflow-0.1.0-py3-none-any.whl exists and contains src files)
- [X] T020 [US1] Test local installation: `pip install dist/oos_workflow-0.1.0-py3-none-any.whl` and verify importable

**Checkpoint**: User Story 1 complete - wheel package builds successfully and installs locally

---

## Phase 4: User Story 2 - Deploy and Run on Azure Databricks (Priority: P1) 🎯 MVP

**Goal**: Deploy wheel to ADB workspace using DAB and execute on ephemeral cluster

**Independent Test**: Run `databricks bundle deploy --target dev`, execute job, verify successful output in ADB UI

### Implementation for User Story 2

- [X] T021 [P] [US2] Create Databricks adapter implementation in `src/oos_workflow/adapters/databricks.py` (real Spark APIs)
- [X] T022 [P] [US2] Create `config/databricks.yaml` with environment: databricks, data_source config (type: delta, path placeholder)
- [X] T023 [P] [US2] Create `databricks.yml` at repository root with bundle name and artifacts configuration
- [X] T024 [US2] Add job definition to `databricks.yml` (oos_workflow_job with python_wheel_task entry point)
- [X] T025 [US2] Configure job cluster in `databricks.yml` (spark_version: 13.3.x, node_type_id: Standard_DS3_v2, num_workers: 1)
- [X] T026 [US2] Add wheel library reference to job tasks in `databricks.yml` pointing to artifacts path
- [X] T027 [US2] Create dev target in `databricks.yml` with workspace host placeholder
- [X] T028 [US2] Validate DAB bundle configuration with `databricks bundle validate` (requires databricks-cli)
- [X] T029 [US2] Update main.py to detect ADB environment and load databricks.yaml config
- [X] T030 [US2] Deploy bundle to ADB workspace with `databricks bundle deploy --target dev` (requires ADB access)
- [X] T031 [US2] Execute job on ADB cluster with `databricks bundle run oos_workflow_job --target dev` (requires ADB access)
- [X] T032 [US2] Verify job execution in Databricks UI and check logs for successful completion (requires ADB access)

**Checkpoint**: User Story 2 complete - application deploys to ADB and runs successfully on ephemeral cluster

---

## Phase 5: User Story 3 - Developer Onboarding Documentation (Priority: P2)

**Goal**: Comprehensive README enabling new developers to build, package, and deploy without assistance

**Independent Test**: New team member follows README and completes full workflow (setup → build → deploy → run) within 15 minutes

### Implementation for User Story 3

- [X] T033 [P] [US3] Update README.md with Prerequisites section (Python 3.11+, uv, ADB workspace, databricks-cli)
- [X] T034 [P] [US3] Add Local Development Setup section to README.md (uv sync, uv run commands)
- [X] T035 [P] [US3] Add Building the Wheel section to README.md (uv build command, verification steps)
- [X] T036 [P] [US3] Add Deploying to Azure Databricks section to README.md (databricks configure, bundle validate/deploy/run)
- [X] T037 [P] [US3] Add Project Structure Overview to README.md (directory tree with explanations)
- [X] T038 [P] [US3] Add Common Commands Reference to README.md (quick command cheatsheet)
- [X] T039 [P] [US3] Add Troubleshooting section to README.md (common errors and solutions)
- [X] T040 [US3] Add Architecture Overview to README.md explaining adapter pattern and environment switching
- [X] T041 [US3] Validate README completeness by simulating new developer onboarding flow

**Checkpoint**: User Story 3 complete - README provides complete developer onboarding guide

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Repository hygiene and final validation

- [X] T042 [P] Add docstrings to all public classes and methods in src/oos_workflow/
- [X] T043 [P] Create sample data file in config/data/sample.csv for local testing (if not using real data)
- [X] T044 Validate constitutional compliance: local execution works without ADB, dependencies locked, structure clean
- [X] T045 Final smoke test: clean build from scratch (rm -rf dist/ .venv/, uv sync, uv build, test install)

---

## Dependencies & Execution Strategy

### User Story Completion Order

```
Setup (Phase 1)
    ↓
Foundational (Phase 2) ← BLOCKING for all user stories
    ↓
    ├─→ US1: Package as Wheel (P1) ← MVP Foundation
    │       ↓
    ├─→ US2: Deploy to ADB (P1) ← Depends on US1 wheel artifact
    │       ↓
    └─→ US3: Documentation (P2) ← Can reference completed US1 & US2
            ↓
        Polish (Phase 6)
```

### Parallel Execution Opportunities

**Phase 1 (Setup)**: Tasks T003, T004, T006, T007 can run in parallel after T001-T002 complete

**Phase 2 (Foundational)**: Tasks T009, T010 can run in parallel after T008 completes

**Phase 3 (US1)**: Tasks T012, T013 can run in parallel; T016-T017 can overlap

**Phase 4 (US2)**: Tasks T021, T022, T023 can run in parallel; T024-T027 are sequential DAB config

**Phase 5 (US3)**: Tasks T033-T039 are all parallelizable (different README sections)

**Phase 6 (Polish)**: Tasks T042, T043 can run in parallel

### MVP Scope Recommendation

**Minimum Viable Product = User Story 1 + User Story 2**

This delivers:
- ✅ Packaged wheel artifact
- ✅ DAB deployment configuration
- ✅ Working application on ADB
- ✅ Constitutional compliance (local + ADB execution)

User Story 3 (documentation) can be added incrementally after validating core functionality.

---

## Task Summary

**Total Tasks**: 45  
**Setup Phase**: 7 tasks  
**Foundational Phase**: 4 tasks  
**User Story 1 (Package as Wheel)**: 9 tasks  
**User Story 2 (Deploy to ADB)**: 12 tasks  
**User Story 3 (Documentation)**: 9 tasks  
**Polish Phase**: 4 tasks

**Parallelizable Tasks**: 18 tasks marked with [P]  
**Sequential Tasks**: 27 tasks (dependencies on prior work)

**Estimated Completion**:
- MVP (US1 + US2): ~20 tasks (T001-T032 minus some parallel execution)
- Full Feature: All 45 tasks
- Suggested first milestone: Complete through Phase 4 (T001-T032)

---

## Format Validation ✅

All tasks follow required checklist format:
- ✅ Checkbox present: `- [ ]`
- ✅ Task IDs sequential: T001-T045
- ✅ [P] markers on parallelizable tasks
- ✅ [US1], [US2], [US3] story labels on user story tasks
- ✅ Exact file paths included in descriptions
- ✅ Organized by user story for independent implementation
