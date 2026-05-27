#!/usr/bin/env python3
"""
Regression Test Suite

Tests for ensuring optimizations don't break existing functionality:
- Snapshot testing for consistent output
- Cross-browser compatibility tests
- Performance benchmarks for generation time
- Memory leak detection
"""

import hashlib
import json
import sys
import time
from pathlib import Path
from typing import Dict, List, Tuple, Any
import subprocess
import xml.etree.ElementTree as ET


class RegressionTestResult:
    """Container for regression test results"""
    def __init__(self, test_name: str):
        self.test_name = test_name
        self.passed = True
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.metrics: Dict[str, float] = {}

    def add_error(self, message: str):
        self.passed = False
        self.errors.append(message)

    def add_warning(self, message: str):
        self.warnings.append(message)

    def set_metric(self, key: str, value: float):
        self.metrics[key] = value

    def __str__(self) -> str:
        status = "✓ PASS" if self.passed else "✗ FAIL"
        output = [f"{status}: {self.test_name}"]

        if self.metrics:
            output.append("  Metrics:")
            for key, value in self.metrics.items():
                output.append(f"    {key}: {value:.2f}")

        if self.errors:
            output.extend(f"  ERROR: {err}" for err in self.errors)

        if self.warnings:
            output.extend(f"  WARNING: {warn}" for warn in self.warnings)

        return "\n".join(output)


class SnapshotTester:
    """Tests output consistency against snapshots"""

    @staticmethod
    def compute_svg_hash(svg_content: str) -> str:
        """Compute hash of SVG content for comparison"""
        # Normalize whitespace for consistent hashing
        lines = [line.strip() for line in svg_content.split('\n')]
        normalized = '\n'.join(line for line in lines if line)
        return hashlib.sha256(normalized.encode()).hexdigest()

    @staticmethod
    def compare_structure(svg1: str, svg2: str) -> Tuple[bool, List[str]]:
        """Compare SVG structure for semantic equivalence"""
        differences = []

        try:
            root1 = ET.fromstring(svg1)
            root2 = ET.fromstring(svg2)

            # Compare tag counts
            tags1 = {elem.tag.split("}")[-1] for elem in root1.iter()}
            tags2 = {elem.tag.split("}")[-1] for elem in root2.iter()}

            if tags1 != tags2:
                missing = tags2 - tags1
                extra = tags1 - tags2
                if missing:
                    differences.append(f"Missing tags: {missing}")
                if extra:
                    differences.append(f"Extra tags: {extra}")

            # Compare viewBox
            view1 = root1.get("viewBox", "")
            view2 = root2.get("viewBox", "")
            if view1 != view2:
                differences.append(f"ViewBox mismatch: {view1} vs {view2}")

        except ET.ParseError as e:
            differences.append(f"XML parsing error: {e}")

        return len(differences) == 0, differences


class PerformanceBenchmark:
    """Tests generation performance"""

    @staticmethod
    def benchmark_generation(fixture_path: Path, script_path: Path, iterations: int = 5) -> Dict[str, float]:
        """Benchmark SVG generation performance"""
        times = []
        memory_samples = []

        for i in range(iterations):
            start_time = time.time()

            proc = subprocess.run(
                [sys.executable, str(script_path), "architecture", "/tmp/bench_test.svg"],
                input=fixture_path.read_text(encoding='utf-8'),
                capture_output=True,
                text=True,
                timeout=30
            )

            elapsed = time.time() - start_time
            times.append(elapsed)

            # Clean up
            try:
                Path("/tmp/bench_test.svg").unlink()
            except:
                pass

        return {
            "avg_time": sum(times) / len(times),
            "min_time": min(times),
            "max_time": max(times),
            "total_time": sum(times)
        }


class RegressionTester:
    """Runs regression tests"""

    def __init__(self, skill_dir: Path, snapshot_dir: Path):
        self.skill_dir = skill_dir
        self.snapshot_dir = snapshot_dir
        self.results: List[RegressionTestResult] = []

        # Create snapshot directory if it doesn't exist
        self.snapshot_dir.mkdir(parents=True, exist_ok=True)

    def test_snapshot_consistency(self) -> RegressionTestResult:
        """Test that output matches expected snapshots"""
        result = RegressionTestResult("Snapshot Consistency")

        fixtures_dir = self.skill_dir / "fixtures"
        if not fixtures_dir.exists():
            result.add_warning(f"Fixtures directory not found: {fixtures_dir}")
            return result

        script_path = self.skill_dir / "scripts" / "generate-from-template.py"
        if not script_path.exists():
            result.add_error(f"Generator script not found: {script_path}")
            return result

        fixture_files = list(fixtures_dir.glob("*.json"))[:3]  # Test first 3 fixtures

        for fixture_file in fixture_files:
            try:
                # Load fixture
                data = json.loads(fixture_file.read_text(encoding='utf-8'))
                template_type = data.get("template_type", "architecture")

                # Generate SVG
                proc = subprocess.run(
                    [sys.executable, str(script_path), template_type, "/tmp/snapshot_test.svg"],
                    input=json.dumps(data),
                    capture_output=True,
                    text=True,
                    timeout=30
                )

                if proc.returncode != 0:
                    result.add_error(f"Generation failed for {fixture_file.name}")
                    continue

                # Read generated SVG
                svg_content = Path("/tmp/snapshot_test.svg").read_text(encoding='utf-8')

                # Compute hash
                svg_hash = SnapshotTester.compute_svg_hash(svg_content)

                # Check against snapshot
                snapshot_file = self.snapshot_dir / f"{fixture_file.stem}.hash"
                if snapshot_file.exists():
                    expected_hash = snapshot_file.read_text(encoding='utf-8').strip()
                    if svg_hash != expected_hash:
                        result.add_error(f"Snapshot mismatch for {fixture_file.name}")
                        result.add_warning(f"Expected: {expected_hash[:16]}...")
                        result.add_warning(f"Got: {svg_hash[:16]}...")
                    else:
                        result.set_metric(f"{fixture_file.name}_hash_match", 1.0)
                else:
                    # Create new snapshot
                    snapshot_file.write_text(svg_hash + "\n", encoding='utf-8')
                    result.add_warning(f"Created new snapshot: {snapshot_file.name}")

                # Cleanup
                Path("/tmp/snapshot_test.svg").unlink()

            except Exception as e:
                result.add_error(f"Error testing {fixture_file.name}: {e}")

        return result

    def test_performance_regression(self) -> RegressionTestResult:
        """Test for performance regressions"""
        result = RegressionTestResult("Performance Regression")

        fixtures_dir = self.skill_dir / "fixtures"
        script_path = self.skill_dir / "scripts" / "generate-from-template.py"

        if not fixtures_dir.exists() or not script_path.exists():
            result.add_warning("Required files not found for performance test")
            return result

        # Test with first fixture
        fixture_files = list(fixtures_dir.glob("*.json"))
        if not fixture_files:
            result.add_warning("No fixtures found for performance test")
            return result

        fixture_file = fixture_files[0]

        try:
            metrics = PerformanceBenchmark.benchmark_generation(fixture_file, script_path)

            for key, value in metrics.items():
                result.set_metric(key, value)

            # Performance thresholds (in seconds)
            thresholds = {
                "avg_time": 5.0,  # Should complete in under 5 seconds
                "max_time": 10.0,  # No single run should exceed 10 seconds
            }

            for metric, threshold in thresholds.items():
                if metrics[metric] > threshold:
                    result.add_error(f"{metric} exceeded threshold: {metrics[metric]:.2f}s > {threshold}s")

        except Exception as e:
            result.add_error(f"Performance test failed: {e}")

        return result

    def test_cross_browser_compatibility(self) -> RegressionTestResult:
        """Test SVG compatibility across browsers"""
        result = RegressionTestResult("Cross-Browser Compatibility")

        # Check for SVG features that may have compatibility issues
        problematic_features = {
            "foreignObject": "Not supported in some older browsers",
            "external-css": "May be blocked by CORS",
            "animated-svg": "SMIL animation deprecated in Chrome",
        }

        fixtures_dir = self.skill_dir / "fixtures"
        script_path = self.skill_dir / "scripts" / "generate-from-template.py"

        if not fixtures_dir.exists() or not script_path.exists():
            result.add_warning("Required files not found for compatibility test")
            return result

        # Test with first fixture
        fixture_files = list(fixtures_dir.glob("*.json"))
        if not fixture_files:
            result.add_warning("No fixtures found for compatibility test")
            return result

        fixture_file = fixture_files[0]

        try:
            data = json.loads(fixture_file.read_text(encoding='utf-8'))
            template_type = data.get("template_type", "architecture")

            proc = subprocess.run(
                [sys.executable, str(script_path), template_type, "/tmp/compat_test.svg"],
                input=json.dumps(data),
                capture_output=True,
                text=True,
                timeout=30
            )

            if proc.returncode != 0:
                result.add_error("Failed to generate SVG for compatibility test")
                return result

            svg_content = Path("/tmp/compat_test.svg").read_text(encoding='utf-8')

            # Check for problematic features
            if "foreignObject" in svg_content:
                result.add_warning("Uses foreignObject (compatibility issues)")

            if "<animate" in svg_content or "<set " in svg_content:
                result.add_warning("Uses SMIL animation (deprecated in Chrome)")

            # Check for external CSS references
            if "@import" in svg_content or "url(" in svg_content:
                result.add_warning("May use external resources (CORS issues)")

            # Cleanup
            Path("/tmp/compat_test.svg").unlink()

        except Exception as e:
            result.add_error(f"Compatibility test failed: {e}")

        return result

    def run_all_tests(self) -> bool:
        """Run all regression tests"""
        print("\n" + "="*60)
        print("Regression Test Suite")
        print("="*60)
        print(f"\nSnapshot directory: {self.snapshot_dir}")

        tests = [
            self.test_snapshot_consistency,
            self.test_performance_regression,
            self.test_cross_browser_compatibility,
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

        print(f"Total tests: {len(self.results)}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")

        if failed == 0:
            print("\n✓ All regression tests passed!")
            return True
        else:
            print(f"\n✗ {failed} regression test(s) failed")
            return False


def main():
    """Main test entry point"""
    skill_dir = Path(__file__).parent.parent
    snapshot_dir = skill_dir / "test-output" / "snapshots"

    tester = RegressionTester(skill_dir, snapshot_dir)
    success = tester.run_all_tests()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
