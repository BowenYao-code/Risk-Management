#!/usr/bin/env python
"""
Test runner for Black-Scholes Option Pricing Model

This script runs all tests and provides a summary of results.

Author: Bowen
Date: 2024
Purpose: Risk Analyst Portfolio Project
"""

import unittest
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def run_tests():
    """Run all tests and display results."""
    print("=" * 70)
    print("BLACK-SCHOLES OPTION PRICING MODEL - TEST SUITE")
    print("=" * 70)
    print("Running comprehensive tests for option pricing model...")
    print()
    
    # Discover and run all tests
    loader = unittest.TestLoader()
    start_dir = 'tests'
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2, buffer=True)
    result = runner.run(suite)
    
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    skipped = len(result.skipped) if hasattr(result, 'skipped') else 0
    
    print(f"Total Tests Run: {total_tests}")
    print(f"Passed: {total_tests - failures - errors - skipped}")
    print(f"Failed: {failures}")
    print(f"Errors: {errors}")
    print(f"Skipped: {skipped}")
    
    if failures > 0:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback.split('AssertionError: ')[-1].split('\\n')[0]}")
    
    if errors > 0:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback.split('\\n')[-2]}")
    
    print("\n" + "=" * 70)
    
    if failures == 0 and errors == 0:
        print("🎉 ALL TESTS PASSED! The Black-Scholes model is working correctly.")
        print("✅ Option pricing calculations are accurate")
        print("✅ Greeks calculations are validated")
        print("✅ Monte Carlo validation confirms results")
        print("✅ Implied volatility calculation converges properly")
        return True
    else:
        print("❌ SOME TESTS FAILED! Please review the implementation.")
        return False

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
