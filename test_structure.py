#!/usr/bin/env python3
"""
Basic structure tests for databricks_io module.
These tests verify that functions are defined correctly without requiring Spark/Delta dependencies.
"""

import ast
import sys


def test_module_imports():
    """Test that the module can be parsed and has expected imports"""
    with open('databricks_io.py', 'r') as f:
        code = f.read()
    
    tree = ast.parse(code)
    
    # Check for expected imports
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            imports.append(node.module)
    
    assert 'pyspark.sql' in imports, "Missing pyspark.sql import"
    assert 'pyspark.sql.types' in imports, "Missing pyspark.sql.types import"
    assert 'delta' in imports, "Missing delta import"
    
    print("✓ Module imports are correct")


def test_function_definitions():
    """Test that all expected functions are defined"""
    with open('databricks_io.py', 'r') as f:
        code = f.read()
    
    tree = ast.parse(code)
    
    expected_functions = [
        'create_spark_session',
        'read_parquet',
        'write_parquet',
        'read_delta_table',
        'write_delta_table',
        'create_sample_dataframe',
        'main'
    ]
    
    defined_functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    
    for func in expected_functions:
        assert func in defined_functions, f"Missing function: {func}"
    
    print(f"✓ All {len(expected_functions)} expected functions are defined")


def test_function_signatures():
    """Test that functions have expected parameters"""
    with open('databricks_io.py', 'r') as f:
        code = f.read()
    
    tree = ast.parse(code)
    
    function_params = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            params = [arg.arg for arg in node.args.args]
            function_params[node.name] = params
    
    # Verify key function signatures
    assert 'spark' in function_params.get('read_parquet', []), "read_parquet should have 'spark' parameter"
    assert 'parquet_path' in function_params.get('read_parquet', []), "read_parquet should have 'parquet_path' parameter"
    
    assert 'spark' in function_params.get('read_delta_table', []), "read_delta_table should have 'spark' parameter"
    assert 'delta_path' in function_params.get('read_delta_table', []), "read_delta_table should have 'delta_path' parameter"
    
    assert 'df' in function_params.get('write_parquet', []), "write_parquet should have 'df' parameter"
    assert 'df' in function_params.get('write_delta_table', []), "write_delta_table should have 'df' parameter"
    
    print("✓ Function signatures are correct")


def test_docstrings():
    """Test that functions have docstrings"""
    with open('databricks_io.py', 'r') as f:
        code = f.read()
    
    tree = ast.parse(code)
    
    functions_with_docstrings = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            docstring = ast.get_docstring(node)
            if docstring:
                functions_with_docstrings.append(node.name)
    
    assert len(functions_with_docstrings) >= 6, "Most functions should have docstrings"
    print(f"✓ {len(functions_with_docstrings)} functions have docstrings")


def test_example_usage_structure():
    """Test that example_usage.py has expected structure"""
    with open('example_usage.py', 'r') as f:
        code = f.read()
    
    tree = ast.parse(code)
    
    # Check for expected functions
    expected_examples = [
        'example_parquet_operations',
        'example_delta_operations',
        'example_custom_paths'
    ]
    
    defined_functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    
    for func in expected_examples:
        assert func in defined_functions, f"Missing example function: {func}"
    
    print(f"✓ example_usage.py has all {len(expected_examples)} example functions")


def test_requirements_file():
    """Test that requirements.txt exists and has expected dependencies"""
    with open('requirements.txt', 'r') as f:
        requirements = f.read()
    
    assert 'pyspark' in requirements, "requirements.txt should include pyspark"
    assert 'delta-spark' in requirements, "requirements.txt should include delta-spark"
    
    print("✓ requirements.txt has required dependencies")


def main():
    """Run all tests"""
    print("Running structure tests...\n")
    
    tests = [
        test_module_imports,
        test_function_definitions,
        test_function_signatures,
        test_docstrings,
        test_example_usage_structure,
        test_requirements_file
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} error: {e}")
            failed += 1
    
    print(f"\n{'='*50}")
    print(f"Tests passed: {passed}/{len(tests)}")
    print(f"Tests failed: {failed}/{len(tests)}")
    
    if failed > 0:
        sys.exit(1)
    else:
        print("\n✓ All structure tests passed!")


if __name__ == "__main__":
    main()
