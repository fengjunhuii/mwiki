#!/usr/bin/env python3
"""
File Pollution Prevention Test Suite

Tests for file pollution prevention and cleanup:
- Pre-generation cleanup checks
- Post-generation validation
- Temporary file tracking and automatic cleanup
- Warning system for potential pollution issues
"""

import os
import sys
import tempfile
import time
from pathlib import Path
from typing import List, Set, Dict
import subprocess


class FilePollutionTestResult:
    """Container for file pollution test results"""
    def __init__(self, test_name: str):
        self.test_name = test_name
        self.passed = True
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.files_created: List[Path] = []
        self.files_left_behind: List[Path] = []

    def add_error(self, message: str):
        self.passed = False
        self.errors.append(message)

    def add_warning(self, message: str):
        self.warnings.append(message)

    def track_file(self, filepath: Path):
        self.files_created.append(filepath)

    def track_leftover(self, filepath: Path):
        self.files_left_behind.append(filepath)
        self.passed = False

    def __str__(self) -> str:
        status = "✓ PASS" if self.passed else "✗ FAIL"
        output = [f"{status}: {self.test_name}"]

        if self.files_created:
            output.append(f"  Files created: {len(self.files_created)}")

        if self.files_left_behind:
            output.append(f"  Files left behind: {len(self.files_left_behind)}")
            for f in self.files_left_behind:
                output.append(f"    - {f.name}")

        if self.errors:
            output.extend(f"  ERROR: {err}" for err in self.errors)

        if self.warnings:
            output.extend(f"  WARNING: {warn}" for warn in self.warnings)

        return "\n".join(output)


class FilePollutionDetector:
    """Detects and prevents file pollution"""

    # Temporary file patterns that should not remain after generation
    TEMP_PATTERNS = [
        "*_test.svg",
        "*_backup.svg",
        "*_temp.svg",
        "*~",
        "*.tmp",
        "*.bak",
        ".#*",
        "#*#",
    ]

    # Expected output patterns (legitimate files)
    OUTPUT_PATTERNS = [
        "*.svg",  # Main SVG output
        "*.png",  # Optional PNG export
        "*.html",  # Optional HTML viewer
    ]

    @staticmethod
    def scan_directory(directory: Path) -> Dict[str, List[Path]]:
        """Scan directory for temporary and output files"""
        temp_files = []
        output_files = []

        for pattern in FilePollutionDetector.TEMP_PATTERNS:
            temp_files.extend(directory.glob(pattern))

        for pattern in FilePollutionDetector.OUTPUT_PATTERNS:
            output_files.extend(directory.glob(pattern))

        return {
            "temp": temp_files,
            "output": output_files
        }

    @staticmethod
    def detect_pollution(directory: Path, baseline: Set[Path]) -> List[Path]:
        """Detect new files created during operation"""
        current_files = set(directory.glob("*"))
        new_files = current_files - baseline
        return list(new_files)


class FilePollutionTester:
    """Tests file pollution prevention mechanisms"""

    def __init__(self, test_dir: Path, skill_dir: Path):
        self.test_dir = test_dir
        self.skill_dir = skill_dir
        self.results: List[FilePollutionTestResult] = []

        # Create test directory
        self.test_dir.mkdir(parents=True, exist_ok=True)

    def test_no_temp_files_in_fixtures(self) -> FilePollutionTestResult:
        """Test that fixtures directory doesn't contain temporary files"""
        result = FilePollutionTestResult("Fixtures Directory Cleanliness")

        fixtures_dir = self.skill_dir / "fixtures"
        if not fixtures_dir.exists():
            result.add_warning(f"Fixtures directory not found: {fixtures_dir}")
            return result

        scan_result = FilePollutionDetector.scan_directory(fixtures_dir)

        if scan_result["temp"]:
            result.add_error(f"Found {len(scan_result['temp'])} temporary files in fixtures")
            for f in scan_result["temp"]:
                result.track_leftover(f)

        return result

    def test_generation_creates_only_output(self) -> FilePollutionTestResult:
        """Test that SVG generation only creates expected output files"""
        result = FilePollutionTestResult("Clean Generation Process")

        # Get baseline files
        baseline = set(self.test_dir.glob("*"))

        # Run a simple generation
        fixture_path = self.skill_dir / "fixtures" / "mem0-style1.json"

        if not fixture_path.exists():
            result.add_warning(f"Test fixture not found: {fixture_path}")
            return result

        # Generate SVG
        output_path = self.test_dir / "test_output.svg"

        try:
            script_path = self.skill_dir / "scripts" / "generate-from-template.py"

            proc = subprocess.run(
                [sys.executable, str(script_path), "memory", str(output_path)],
                input=fixture_path.read_text(encoding='utf-8'),
                capture_output=True,
                text=True,
                timeout=30
            )

            if proc.returncode != 0:
                result.add_error(f"Generation failed: {proc.stderr}")
                return result

        except Exception as e:
            result.add_error(f"Generation error: {e}")
            return result

        # Check for new files
        new_files = FilePollutionDetector.detect_pollution(self.test_dir, baseline)

        # Filter out expected output files
        temp_files = [f for f in new_files if not any(f.match(p) for p in FilePollutionDetector.OUTPUT_PATTERNS)]

        if temp_files:
            result.add_error(f"Unexpected temporary files created: {len(temp_files)}")
            for f in temp_files:
                result.track_leftover(f)

        result.files_created = new_files

        # Cleanup
        for f in new_files:
            try:
                f.unlink()
            except:
                pass

        return result

    def test_cleanup_script_functionality(self) -> FilePollutionTestResult:
        """Test that cleanup mechanisms work properly"""
        result = FilePollutionTestResult("Cleanup Mechanisms")

        # Create some test temporary files
        test_files = [
            self.test_dir / "test_temp.svg",
            self.test_dir / "test_backup.svg",
            self.test_dir / "legitimate_output.svg"
        ]

        for f in test_files:
            f.write_text("test content")

        # Check if cleanup script exists and works
        cleanup_script = self.skill_dir / "scripts" / "cleanup-temp-files.sh"

        if not cleanup_script.exists():
            result.add_warning("Cleanup script not found (not implemented)")
            # Manual cleanup
            for f in test_files:
                try:
                    f.unlink()
                except:
                    pass
            return result

        # Run cleanup script
        try:
            proc = subprocess.run(
                ["bash", str(cleanup_script), str(self.test_dir)],
                capture_output=True,
                text=True,
                timeout=30
            )

            if proc.returncode != 0:
                result.add_warning(f"Cleanup script failed: {proc.stderr}")

        except Exception as e:
            result.add_warning(f"Cleanup script error: {e}")

        # Check if temp files were cleaned
        remaining_temp = [f for f in test_files if "temp" in f.name or "backup" in f.name]

        if remaining_temp:
            result.add_error(f"Cleanup failed to remove {len(remaining_temp)} temp files")
            for f in remaining_temp:
                result.track_leftover(f)

        # Check if legitimate files remain
        remaining_legit = [f for f in test_files if f.exists() and "legitimate" in f.name]

        if not remaining_legit:
            result.add_warning("Cleanup may have removed legitimate files")

        # Final cleanup
        for f in test_files:
            try:
                f.unlink()
            except:
                pass

        return result

    def test_pollution_warning_system(self) -> FilePollutionTestResult:
        """Test pollution detection and warning system"""
        result = FilePollutionTestResult("Pollution Warning System")

        # Create a pollution scenario
        polluting_files = [
            self.test_dir / "test_temp.svg",
            self.test_dir / "test_backup.svg"
        ]

        for f in polluting_files:
            f.write_text("pollution test")

        # Run pollution detection
        scan_result = FilePollutionDetector.scan_directory(self.test_dir)

        if scan_result["temp"]:
            result.add_warning(f"Detected {len(scan_result['temp'])} polluting files (as expected)")
            for f in scan_result["temp"]:
                result.track_leftover(f)

        # Cleanup
        for f in polluting_files:
            try:
                f.unlink()
            except:
                pass

        return result

    def run_all_tests(self) -> bool:
        """Run all file pollution tests"""
        print("\n" + "="*60)
        print("File Pollution Prevention Test Suite")
        print("="*60)
        print(f"\nTest directory: {self.test_dir}")

        tests = [
            self.test_no_temp_files_in_fixtures,
            self.test_generation_creates_only_output,
            self.test_cleanup_script_functionality,
            self.test_pollution_warning_system,
        ]

        for test in tests:
            print(f"\n{'-'*60}")
            test_result = test()
            self.results.append(test_result)
            print(test_result)

        # Print summary
        print("\n" + "="*60)
        print("Test Summary")
        print("="*60)

        passed = sum(1 for r in self.results if r.passed)
        failed = len(self.results) - passed
        total_leftovers = sum(len(r.files_left_behind) for r in self.results)

        print(f"Total tests: {len(self.results)}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Files left behind: {total_leftovers}")

        if failed == 0 and total_leftovers == 0:
            print("\n✓ All tests passed! No file pollution detected.")
            return True
        else:
            print(f"\n✗ Tests failed or pollution detected")
            return False

    def cleanup(self):
        """Final cleanup of test directory"""
        try:
            for f in self.test_dir.glob("*"):
                if f.is_file():
                    f.unlink()
            self.test_dir.rmdir()
        except:
            pass


def main():
    """Main test entry point"""
    skill_dir = Path(__file__).parent.parent
    test_dir = skill_dir / "test-output" / "pollution-tests"

    tester = FilePollutionTester(test_dir, skill_dir)

    try:
        success = tester.run_all_tests()
        return 0 if success else 1
    finally:
        tester.cleanup()


if __name__ == "__main__":
    sys.exit(main())
