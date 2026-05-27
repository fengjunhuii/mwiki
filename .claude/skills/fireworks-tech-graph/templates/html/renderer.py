#!/usr/bin/env python3
"""
HTML Template Renderer for Fireworks Tech Graph

This module provides functionality to render SVG diagrams into
interactive HTML templates with multiple styles and features.
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from string import Template


class HTMLRenderer:
    """Renders SVG diagrams into interactive HTML templates."""

    def __init__(self, template_dir: Optional[str] = None):
        """
        Initialize the HTML renderer.

        Args:
            template_dir: Directory containing HTML templates.
                        Defaults to templates/html/
        """
        if template_dir is None:
            # Default to the templates/html directory
            current_dir = Path(__file__).parent.parent
            template_dir = current_dir / 'html'

        self.template_dir = Path(template_dir)
        self.base_template = self.template_dir / 'template-base.html'

    def render(
        self,
        svg_content: str,
        title: str = 'Technical Diagram',
        subtitle: Optional[str] = None,
        description: Optional[str] = None,
        style: int = 5,
        legend_items: Optional[List[Dict[str, str]]] = None,
        footer: Optional[str] = None,
        custom_css: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Render SVG content into an HTML template.

        Args:
            svg_content: SVG diagram content
            title: Diagram title
            subtitle: Optional subtitle
            description: Optional description text
            style: Style number (1-7), default 5 (Glassmorphism)
            legend_items: List of legend items with 'color' and 'label' keys
            footer: Optional footer text
            custom_css: Additional CSS to include
            **kwargs: Additional template variables

        Returns:
            Rendered HTML string
        """
        # Read base template
        with open(self.base_template, 'r', encoding='utf-8') as f:
            template_content = f.read()

        # Create title slug for filenames
        title_slug = self.slugify(title)

        # Prepare template variables
        variables = {
            'TITLE': title,
            'TITLE_SLUG': title_slug,
            'SVG_CONTENT': svg_content,
            'SUBTITLE': subtitle or '',
            'DESCRIPTION': description or '',
            'STYLE': str(style),
            'FOOTER': footer or 'Generated with Fireworks Tech Graph',
            **kwargs
        }

        # Add legend if provided
        if legend_items:
            variables['LEGEND'] = 'true'
            variables['LEGEND_ITEMS'] = self._render_legend(legend_items)
        else:
            variables['LEGEND'] = ''
            variables['LEGEND_ITEMS'] = ''

        # Add custom CSS if provided
        if custom_css:
            variables['CUSTOM_CSS'] = f'<style>{custom_css}</style>'
        else:
            variables['CUSTOM_CSS'] = ''

        # Replace template variables
        html = self._replace_variables(template_content, variables)

        return html

    def render_from_json(
        self,
        json_path: str,
        svg_content: str,
        **kwargs
    ) -> str:
        """
        Render HTML from a JSON fixture file.

        Args:
            json_path: Path to JSON fixture file
            svg_content: SVG diagram content
            **kwargs: Additional template variables

        Returns:
            Rendered HTML string
        """
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Extract common fields from JSON
        return self.render(
            svg_content=svg_content,
            title=data.get('title', 'Technical Diagram'),
            subtitle=data.get('subtitle'),
            description=data.get('description'),
            style=data.get('style', 5),
            legend_items=data.get('legend'),
            **kwargs
        )

    def save(
        self,
        html_content: str,
        output_path: str,
        create_dirs: bool = True
    ) -> None:
        """
        Save rendered HTML to a file.

        Args:
            html_content: Rendered HTML content
            output_path: Path to save HTML file
            create_dirs: Create parent directories if they don't exist
        """
        output_path = Path(output_path)

        if create_dirs:
            output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

    def _render_legend(self, legend_items: List[Dict[str, str]]) -> str:
        """Render legend items as HTML."""
        items_html = []
        for item in legend_items:
            color = item.get('color', '#888888')
            label = item.get('label', 'Unknown')
            items_html.append(f'''
                <div class="legend-item">
                    <div class="legend-icon" style="background-color: {color};"></div>
                    <span class="legend-label">{label}</span>
                </div>
            ''')
        return '\n'.join(items_html)

    def _replace_variables(self, template: str, variables: Dict[str, Any]) -> str:
        """Replace template variables with values."""
        # Replace {{#if VAR}}...{{/if}} conditionals
        template = self._process_conditionals(template, variables)

        # Replace {{VAR}} variables
        for key, value in variables.items():
            placeholder = f'{{{{{key}}}}}'
            template = template.replace(placeholder, str(value))

        return template

    def _process_conditionals(
        self,
        template: str,
        variables: Dict[str, Any]
    ) -> str:
        """Process conditional blocks in template."""
        # Match {{#if VAR}}...{{/if}} blocks
        pattern = r'\{\{#if\s+(\w+)\}\}(.*?)\{\{/if\}\}'

        def replace_conditional(match):
            var_name = match.group(1)
            content = match.group(2)
            # Keep content if variable is truthy, remove otherwise
            if variables.get(var_name):
                return content
            return ''

        return re.sub(pattern, replace_conditional, template, flags=re.DOTALL)

    @staticmethod
    def slugify(text: str) -> str:
        """Convert text to URL-safe slug."""
        # Convert to lowercase and replace spaces with hyphens
        slug = text.lower().strip()
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug


class StandaloneHTMLRenderer(HTMLRenderer):
    """Renderer for standalone HTML files with embedded resources."""

    def render_standalone(
        self,
        svg_content: str,
        title: str = 'Technical Diagram',
        **kwargs
    ) -> str:
        """
        Render a completely standalone HTML file with all resources embedded.

        Args:
            svg_content: SVG diagram content
            title: Diagram title
            **kwargs: Additional template variables

        Returns:
            Standalone HTML string
        """
        # Get base HTML
        html = super().render(svg_content, title, **kwargs)

        # Embed JavaScript files
        html = self._embed_scripts(html)

        # Embed CSS files
        html = self._embed_styles(html)

        return html

    def _embed_scripts(self, html: str) -> str:
        """Embed JavaScript files into HTML."""
        scripts_dir = self.template_dir / 'scripts'
        script_files = ['core.js', 'export.js', 'zoom.js']

        for script_file in script_files:
            script_path = scripts_dir / script_file
            if script_path.exists():
                with open(script_path, 'r', encoding='utf-8') as f:
                    script_content = f.read()
                # Wrap in script tags
                script_tag = f'\n<script>\n{script_content}\n</script>\n'
                html += script_tag

        return html

    def _embed_styles(self, html: str) -> str:
        """Embed CSS files into HTML."""
        styles_dir = self.template_dir / 'styles'
        if not styles_dir.exists():
            return html

        style_files = sorted(styles_dir.glob('*.css'))

        for style_path in style_files:
            with open(style_path, 'r', encoding='utf-8') as f:
                style_content = f.read()
            # Wrap in style tags
            style_tag = f'\n<style>\n/* {style_path.stem} */\n{style_content}\n</style>\n'
            html += style_tag

        return html


def main():
    """CLI entry point for HTML rendering."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Render SVG diagrams to interactive HTML'
    )
    parser.add_argument(
        'svg_file',
        help='Path to SVG file'
    )
    parser.add_argument(
        '-o', '--output',
        default='output.html',
        help='Output HTML file path'
    )
    parser.add_argument(
        '-t', '--title',
        default='Technical Diagram',
        help='Diagram title'
    )
    parser.add_argument(
        '-s', '--style',
        type=int,
        default=5,
        choices=range(1, 8),
        help='Style number (1-7)'
    )
    parser.add_argument(
        '--standalone',
        action='store_true',
        help='Generate standalone HTML with embedded resources'
    )

    args = parser.parse_args()

    # Read SVG content
    with open(args.svg_file, 'r', encoding='utf-8') as f:
        svg_content = f.read()

    # Render HTML
    if args.standalone:
        renderer = StandaloneHTMLRenderer()
        html = renderer.render_standalone(
            svg_content,
            title=args.title,
            style=args.style
        )
    else:
        renderer = HTMLRenderer()
        html = renderer.render(
            svg_content,
            title=args.title,
            style=args.style
        )

    # Save HTML
    renderer.save(html, args.output)
    print(f'HTML saved to {args.output}')


if __name__ == '__main__':
    main()
