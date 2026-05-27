#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for HTML Template Renderer

Validates the HTML template system by generating sample HTML files
from existing fixture data.
"""

import sys
import json
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from templates.html.renderer import HTMLRenderer, StandaloneHTMLRenderer


def load_fixture(fixture_path: str) -> dict:
    """Load a JSON fixture file."""
    with open(fixture_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def create_sample_svg(width: int = 800, height: int = 600) -> str:
    """Create a simple sample SVG for testing."""
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0d1117"/>
      <stop offset="100%" style="stop-color:#161b22"/>
    </linearGradient>
  </defs>

  <!-- Background -->
  <rect width="{width}" height="{height}" fill="url(#bg)"/>

  <!-- Simple diagram elements -->
  <rect x="50" y="50" width="200" height="100" rx="8"
        fill="rgba(255,255,255,0.05)"
        stroke="rgba(255,255,255,0.15)"
        stroke-width="1"/>

  <text x="150" y="100" text-anchor="middle"
        font-family="Arial, sans-serif"
        font-size="16"
        font-weight="600"
        fill="#f0f6fc">Component A</text>

  <rect x="350" y="50" width="200" height="100" rx="8"
        fill="rgba(255,255,255,0.05)"
        stroke="rgba(255,255,255,0.15)"
        stroke-width="1"/>

  <text x="450" y="100" text-anchor="middle"
        font-family="Arial, sans-serif"
        font-size="16"
        font-weight="600"
        fill="#f0f6fc">Component B</text>

  <!-- Arrow -->
  <path d="M 250 100 L 350 100"
        stroke="#58a6ff"
        stroke-width="2"
        fill="none"
        marker-end="url(#arrow)"/>

  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="7"
            refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#58a6ff"/>
    </marker>
  </defs>
</svg>'''


def test_basic_rendering():
    """Test basic HTML rendering."""
    print("Testing basic HTML rendering...")

    renderer = HTMLRenderer()
    svg_content = create_sample_svg()

    html = renderer.render(
        svg_content=svg_content,
        title='Test Diagram',
        subtitle='Basic rendering test',
        description='This is a test diagram to validate the HTML template system.',
        style=5
    )

    # Validate HTML contains expected elements
    assert '<title>Test Diagram - Tech Diagram</title>' in html
    assert 'Test Diagram' in html
    assert 'Basic rendering test' in html
    assert 'svg-container' in html

    # Save sample output
    output_dir = Path(__file__).parent.parent.parent / 'test_output'
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / 'test_basic.html'
    renderer.save(html, output_file)

    print(f"[PASS] Basic rendering test passed. Output saved to {output_file}")
    return True


def test_all_styles():
    """Test rendering with all available styles."""
    print("\nTesting all styles...")

    renderer = HTMLRenderer()
    svg_content = create_sample_svg()

    output_dir = Path(__file__).parent.parent.parent / 'test_output'
    output_dir.mkdir(exist_ok=True)

    for style_num in range(1, 8):
        style_names = {
            1: 'flat',
            2: 'terminal',
            3: 'blueprint',
            4: 'notion',
            5: 'glass',
            6: 'claude',
            7: 'openai'
        }

        html = renderer.render(
            svg_content=svg_content,
            title=f'Style {style_num} - {style_names[style_num].title()}',
            subtitle=f'Testing {style_names[style_num]} style',
            style=style_num
        )

        output_file = output_dir / f'test_style_{style_num}.html'
        renderer.save(html, output_file)

        print(f"[PASS] Style {style_num} ({style_names[style_num]}) rendered to {output_file}")

    return True


def test_with_legend():
    """Test rendering with legend items."""
    print("\nTesting with legend...")

    renderer = HTMLRenderer()
    svg_content = create_sample_svg()

    legend_items = [
        {'color': '#58a6ff', 'label': 'API Request'},
        {'color': '#3fb950', 'label': 'Database'},
        {'color': '#f78166', 'label': 'External Service'}
    ]

    html = renderer.render(
        svg_content=svg_content,
        title='Diagram with Legend',
        legend_items=legend_items,
        style=5
    )

    # Validate legend is present
    assert 'legend-item' in html
    assert 'API Request' in html
    assert 'Database' in html
    assert 'External Service' in html

    # Save output
    output_dir = Path(__file__).parent.parent.parent / 'test_output'
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / 'test_legend.html'
    renderer.save(html, output_file)

    print(f"[PASS] Legend test passed. Output saved to {output_file}")
    return True


def test_from_fixture():
    """Test rendering from a JSON fixture."""
    print("\nTesting from fixture...")

    # Find a fixture file
    fixtures_dir = Path(__file__).parent.parent.parent / 'fixtures'
    fixture_files = list(fixtures_dir.glob('*.json'))

    if not fixture_files:
        print("[WARN] No fixture files found, skipping fixture test")
        return True

    # Use the first fixture found
    fixture_path = fixture_files[0]
    fixture_data = load_fixture(fixture_path)

    renderer = HTMLRenderer()
    svg_content = create_sample_svg(
        width=fixture_data.get('width', 800),
        height=fixture_data.get('height', 600)
    )

    html = renderer.render_from_json(
        json_path=str(fixture_path),
        svg_content=svg_content
    )

    # Validate
    assert fixture_data.get('title', '') in html or 'Technical Diagram' in html

    # Save output
    output_dir = Path(__file__).parent.parent.parent / 'test_output'
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / f'test_fixture_{fixture_path.stem}.html'
    renderer.save(html, output_file)

    print(f"[PASS] Fixture test passed using {fixture_path.name}. Output saved to {output_file}")
    return True


def test_standalone():
    """Test standalone HTML generation."""
    print("\nTesting standalone HTML...")

    renderer = StandaloneHTMLRenderer()
    svg_content = create_sample_svg()

    html = renderer.render_standalone(
        svg_content=svg_content,
        title='Standalone Diagram'
    )

    # Validate JavaScript is embedded
    assert 'class DiagramCore' in html or 'DiagramCore' in html
    assert 'class DiagramExporter' in html or 'DiagramExporter' in html

    # Save output
    output_dir = Path(__file__).parent.parent.parent / 'test_output'
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / 'test_standalone.html'
    renderer.save(html, output_file)

    print(f"[PASS] Standalone test passed. Output saved to {output_file}")
    return True


def main():
    """Run all tests."""
    print("=" * 60)
    print("HTML Template Renderer Test Suite")
    print("=" * 60)

    tests = [
        test_basic_rendering,
        test_all_styles,
        test_with_legend,
        test_from_fixture,
        test_standalone
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"[FAIL] Test failed: {e}")
            failed += 1
            import traceback
            traceback.print_exc()

    print("\n" + "=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 60)

    if failed > 0:
        sys.exit(1)


if __name__ == '__main__':
    main()
