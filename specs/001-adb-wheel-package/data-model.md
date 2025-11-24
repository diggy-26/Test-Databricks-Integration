# Data Model: Azure Databricks Wheel Package

**Feature**: 001-adb-wheel-package  
**Date**: 2025-11-24  
**Status**: N/A

## Overview

This feature does not involve complex data entities or schemas. It is a simple Python application for testing Databricks integration patterns with minimal business logic.

## Configuration Entities

The only "data" in this application are configuration structures:

### Environment Configuration

**Purpose**: Define runtime environment settings

**Attributes**:
- `environment`: String - "local" or "databricks"
- `data_source`: Object - Data source configuration
  - `type`: String - "local" or "delta"
  - `path`: String - File path or Delta table path
- `cluster`: Object (optional, Databricks only) - Cluster settings
  - `spark_version`: String
  - `node_type_id`: String
  - `num_workers`: Integer

**Lifecycle**: Loaded at application startup from YAML files in `config/` directory

**Validation**: Schema validation on load to ensure required fields present

## No Persistent Storage

This application does not persist data or maintain state. All processing is ephemeral for testing purposes.
