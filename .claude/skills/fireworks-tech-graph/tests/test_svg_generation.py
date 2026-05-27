#!/usr/bin/env python3
"""
SVG Generation Test Suite

Tests SVG generation functionality including:
- Syntax validation
- Tag balance
- Attribute completeness
- Marker references
- Path data validation
"""

import json
import os
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Tuple, Any

# Add parent directory to path to import the generator
SCRIPT_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

try:
    from generate_from_template import build_svg, parse_style, STYLE_PROFILES
except ImportError:
    print("Error: Could not import generate_from_template module")
    sys.exit(1)


class SVGTestResult:
    """Container for test results"""
    def __init__(self, test_name: str):
        self.test_name = test_name
        self.passed = True
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def add_error(self, message: str):
        self.passed = False
        self.errors.append(message)

    def add_warning(self, message: str):
        self.warnings.append(message)

    def __str__(self) -> str:
        status = "✓ PASS" if self.passed else "✗ FAIL"
        output = [f"{status}: {self.test_name}"]

        if self.errors:
            output.extend(f"  ERROR: {err}" for err in self.errors)

        if self.warnings:
            output.extend(f"  WARNING: {warn}" for warn in self.warnings)

        return "\n".join(output)


class SVGValidator:
    """Validates SVG structure and content"""

    @staticmethod
    def validate_xml_structure(svg_content: str) -> SVGTestResult:
        """Validate basic XML structure"""
        result = SVGTestResult("XML Structure Validation")

        try:
            root = ET.fromstring(svg_content)

            # Check root element
            if root.tag != "{http://www.w3.org/2000/svg}svg":
                result.add_error(f"Root element is not svg: {root.tag}")

            # Check for required namespaces
            if "xmlns" not in root.attrib:
                result.add_warning("Missing default xmlns attribute")

            # Check viewBox
            if "viewBox" not in root.attrib:
                result.add_warning("Missing viewBox attribute")

        except ET.ParseError as e:
            result.add_error(f"XML parsing failed: {e}")

        return result

    @staticmethod
    def validate_tag_balance(svg_content: str) -> SVGTestResult:
        """Check if all tags are properly closed"""
        result = SVGTestResult("Tag Balance Validation")

        try:
            root = ET.fromstring(svg_content)

            # If we got here, XML is well-formed (tags are balanced)
            # Additional check for specific SVG tags
            svg_tags = {
                "svg", "defs", "style", "rect", "circle", "ellipse",
                "path", "line", "polygon", "polyline", "text", "g",
                "marker", "filter", "pattern", "clipPath", "use"
            }

            for elem in root.iter():
                tag = elem.tag.split("}")[-1]  # Remove namespace
                if tag in svg_tags or tag.startswith("svg-"):
                    continue  # Valid SVG tag

        except ET.ParseError as e:
            result.add_error(f"Tag balance check failed: {e}")

        return result

    @staticmethod
    def validate_marker_references(svg_content: str) -> SVGTestResult:
        """Validate that all marker references have definitions"""
        result = SVGTestResult("Marker References Validation")

        try:
            root = ET.fromstring(svg_content)

            # Find all marker references
            marker_refs = set()
            for elem in root.iter():
                marker_end = elem.get("marker-end", "")
                if "url(#" in marker_end:
                    ref_id = marker_end.split("url(#")[1].rstrip(")")
                    marker_refs.add(ref_id)

            # Find all marker definitions
            marker_defs = set()
            for elem in root.iter():
                if elem.tag.split("}")[-1] == "marker":
                    marker_id = elem.get("id")
                    if marker_id:
                        marker_defs.add(marker_id)

            # Check for missing markers
            missing = marker_refs - marker_defs
            if missing:
                result.add_error(f"Missing marker definitions: {missing}")

            if not marker_refs and marker_defs:
                result.add_warning(f"Unused marker definitions: {marker_defs}")

        except ET.ParseError as e:
            result.add_error(f"Marker validation failed: {e}")

        return result

    @staticmethod
    def validate_path_data(svg_content: str) -> SVGTestResult:
        """Validate path data syntax"""
        result = SVGTestResult("Path Data Validation")

        try:
            root = ET.fromstring(svg_content)

            for elem in root.iter():
                if elem.tag.split("}")[-1] == "path":
                    d = elem.get("d", "")
                    if not d:
                        result.add_warning("Path element has empty 'd' attribute")
                        continue

                    # Basic path syntax validation
                    # Path commands: M, L, H, V, C, S, Q, T, A, Z
                    import re
                    tokens = re.findall(r'[MLHVCSQTAmLhvcSqtaZ]|-?\d+\.?\d*', d)

                    if not tokens:
                        result.add_warning(f"Path has no valid tokens: {d[:50]}...")
                        continue

                    # Check if starts with a move command
                    if tokens[0].upper() not in {"M"}:
                        result.add_error(f"Path doesn't start with M command: {d[:50]}...")

        except ET.ParseError as e:
            result.add_error(f"Path validation failed: {e}")

        return result

    @staticmethod
    def validate_style_definitions(svg_content: str) -> SVGTestResult:
        """Validate CSS style definitions"""
        result = SVGTestResult("Style Definitions Validation")

        try:
            root = ET.fromstring(svg_content)

            # Find style elements
            styles = []
            for elem in root.iter():
                if elem.tag.split("}")[-1] == "style":
                    if elem.text:
                        styles.append(elem.text)

            if not styles:
                result.add_warning("No <style> element found")
            else:
                # Check for common CSS patterns
                for style in styles:
                    if "font-family" in style:
                        break
                else:
                    result.add_warning("Style definitions don't include font-family")

        except ET.ParseError as e:
            result.add_error(f"Style validation failed: {e}")

        return result


class TestRunner:
    """Runs SVG generation tests"""

    def __init__(self, fixtures_dir: Path):
        self.fixtures_dir = fixtures_dir
        self.results: List[SVGTestResult] = []

    def run_test(self, fixture_file: Path) -> None:
        """Test a single fixture file"""
        print(f"\n{'='*60}")
        print(f"Testing: {fixture_file.name}")
        print(f"{'='*60}")

        # Load fixture data
        try:
            with open(fixture_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            result = SVGTestResult(f"Load fixture: {fixture_file.name}")
            result.add_error(f"Failed to load fixture: {e}")
            self.results.append(result)
            print(result)
            return

        # Determine template type
        template_type = data.get("template_type", "architecture")

        # Generate SVG
        try:
            svg_content = build_svg(template_type, data)
        except Exception as e:
            result = SVGTestResult(f"Generate SVG: {fixture_file.name}")
            result.add_error(f"Failed to generate SVG: {e}")
            self.results.append(result)
            print(result)
            return

        # Run validators
        validators = [
            SVGValidator.validate_xml_structure,
            SVGValidator.validate_tag_balance,
            SVGValidator.validate_marker_references,
            SVGValidator.validate_path_data,
            SVGValidator.validate_style_definitions,
        ]

        for validator in validators:
            test_result = validator(svg_content)
            self.results.append(test_result)
            print(test_result)

    def run_all_tests(self) -> bool:
        """Run tests on all fixture files"""
        print("\n" + "="*60)
        print("SVG Generation Test Suite")
        print("="*60)

        fixture_files = list(self.fixtures_dir.glob("*.json"))

        if not fixture_files:
            print("No fixture files found!")
            return False

        print(f"\nFound {len(fixture_files)} fixture files")

        for fixture_file in sorted(fixture_files):
            self.run_test(fixture_file)

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
            print("\n✓ All tests passed!")
            return True
        else:
            print(f"\n✗ {failed} test(s) failed")
            return False


def main():
    """Main test entry point"""
    skill_dir = Path(__file__).parent.parent
    fixtures_dir = skill_dir / "fixtures"

    if not fixtures_dir.exists():
        print(f"Error: Fixtures directory not found: {fixtures_dir}")
        sys.exit(1)

    runner = TestRunner(fixtures_dir)
    success = runner.run_all_tests()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
