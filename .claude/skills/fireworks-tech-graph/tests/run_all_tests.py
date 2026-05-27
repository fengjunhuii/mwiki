#!/usr/bin/env python3
"""
Master Test Runner

Runs all test suites for the fireworks-tech-graph skill:
- SVG generation tests
- File pollution prevention tests
- Regression tests
"""

import sys
import subprocess
from pathlib import Path
from typing import List, Tuple


class TestSuite:
    """Container for test suite information"""
    def __init__(self, name: str, script: Path, description: str):
        self.name = name
        self.script = script
        self.description = description
        self.passed = False
        self.output = ""
        self.error = ""


class MasterTestRunner:
    """Runs all test suites and aggregates results"""

    def __init__(self, tests_dir: Path):
        self.tests_dir = tests_dir
        self.suites: List[TestSuite] = []

    def discover_tests(self) -> None:
        """Discover all test scripts"""
        test_scripts = [
            ("SVG Generation Tests", "test_svg_generation.py",
             "Tests SVG syntax, tag balance, marker references, path data"),
            ("File Pollution Prevention", "test_file_pollution.py",
             "Tests file cleanup and pollution prevention"),
            ("Regression Tests", "test_regression.py",
             "Tests snapshot consistency, performance, compatibility"),
        ]

        for name, script, description in test_scripts:
            script_path = self.tests_dir / script
            if script_path.exists():
                self.suites.append(TestSuite(name, script_path, description))
            else:
                print(f"Warning: Test script not found: {script}")

    def run_suite(self, suite: TestSuite) -> None:
        """Run a single test suite"""
        print(f"\n{'='*70}")
        print(f"Running: {suite.name}")
        print(f"Description: {suite.description}")
        print(f"Script: {suite.script.name}")
        print('='*70)

        try:
            proc = subprocess.run(
                [sys.executable, str(suite.script)],
                capture_output=True,
                text=True,
                timeout=120,  # 2 minute timeout per suite
                cwd=self.tests_dir.parent
            )

            suite.output = proc.stdout
            suite.error = proc.stderr
            suite.passed = (proc.returncode == 0)

            # Print output
            if suite.output:
                print(suite.output)

            if suite.error:
                print("STDERR:", suite.error)

        except subprocess.TimeoutExpired:
            suite.passed = False
            suite.error = "Test suite timed out after 120 seconds"
            print(f"✗ FAIL: {suite.error}")

        except Exception as e:
            suite.passed = False
            suite.error = str(e)
            print(f"✗ FAIL: {suite.error}")

    def run_all_suites(self) -> bool:
        """Run all discovered test suites"""
        print("\n" + "="*70)
        print("FIREWORKS TECH GRAPH - MASTER TEST SUITE")
        print("="*70)
        print(f"\nTests directory: {self.tests_dir}")
        print(f"Test suites discovered: {len(self.suites)}")

        if not self.suites:
            print("\n✗ No test suites found!")
            return False

        for suite in self.suites:
            self.run_suite(suite)

        # Print summary
        self.print_summary()

        return all(suite.passed for suite in self.suites)

    def print_summary(self) -> None:
        """Print test summary"""
        print("\n" + "="*70)
        print("TEST SUMMARY")
        print("="*70)

        passed = sum(1 for s in self.suites if s.passed)
        failed = len(self.suites) - passed

        print(f"\nTotal suites: {len(self.suites)}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")

        print("\nDetailed Results:")
        print("-" * 70)

        for suite in self.suites:
            status = "✓ PASS" if suite.passed else "✗ FAIL"
            print(f"{status}: {suite.name}")

            if suite.error and not suite.passed:
                print(f"  Error: {suite.error[:100]}...")

        if failed == 0:
            print("\n" + "="*70)
            print("✓ ALL TEST SUITES PASSED!")
            print("="*70)
        else:
            print("\n" + "="*70)
            print(f"✗ {failed} TEST SUITE(S) FAILED")
            print("="*70)


def main():
    """Main entry point"""
    # Determine tests directory
    script_path = Path(__file__).resolve()
    tests_dir = script_path.parent

    if not tests_dir.exists():
        print(f"Error: Tests directory not found: {tests_dir}")
        sys.exit(1)

    # Run tests
    runner = MasterTestRunner(tests_dir)
    runner.discover_tests()

    if not runner.suites:
        print("Error: No test suites discovered")
        sys.exit(1)

    success = runner.run_all_suites()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
