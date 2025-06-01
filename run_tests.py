#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to run all tests.
"""

import unittest
import sys
import os
from pathlib import Path

def run_all_tests():
    """Runs all tests"""
    # Add project root to Python path
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root))
    
    # Discover and run all tests
    loader = unittest.TestLoader()
    start_dir = project_root / 'tests'
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return test results
    return result.wasSuccessful()

def run_specific_test(test_module):
    """Runs a specific test module"""
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root))
    
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromName(f'tests.{test_module}')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Run specific test
        test_module = sys.argv[1]
        print(f"Running test module: {test_module}")
        success = run_specific_test(test_module)
    else:
        # Run all tests
        print("Running all tests...")
        success = run_all_tests()
    
    if success:
        print("\n[SUCCESS] All tests passed!")
        sys.exit(0)
    else:
        print("\n[FAILED] Some tests failed!")
        sys.exit(1)