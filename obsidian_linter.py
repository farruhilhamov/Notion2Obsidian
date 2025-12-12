#!/usr/bin/env python3
"""
Obsidian Linter
Fixes syntax mistakes and ensures proper Obsidian markdown formatting.
"""

import re
from typing import List, Tuple


class ObsidianLinter:
    """Linter for Obsidian markdown files."""

    def __init__(self, config: dict = None):
        """
        Initialize the linter with optional configuration.

        Args:
            config: Dictionary of linting rules and settings
        """
        self.config = config or self._default_config()

    def _default_config(self) -> dict:
        """Return default linting configuration."""
        return {
            'max_blank_lines': 2,
            'ensure_final_newline': True,
            'trim_trailing_whitespace': True,
            'space_after_list_marker': True,
            'space_after_heading': True,
            'consistent_list_style': True,  # Use '-' for bullets
            'ensure_list_spacing': True,
            'fix_table_formatting': True,
            'fix_link_spacing': True,
            'remove_multiple_spaces': True,
            'fix_emphasis': True,
            'standardize_yaml_frontmatter': True,
        }

    def lint(self, content: str) -> str:
        """
        Apply all linting rules to the content.

        Args:
            content: Markdown content to lint

        Returns:
            Linted markdown content
        """
        if not content:
            return content

        # Apply linting rules in order
        content = self._standardize_line_endings(content)

        if self.config.get('standardize_yaml_frontmatter'):
            content = self._fix_yaml_frontmatter(content)

        if self.config.get('space_after_heading'):
            content = self._ensure_space_after_heading(content)

        if self.config.get('space_after_list_marker'):
            content = self._ensure_space_after_list_marker(content)

        if self.config.get('consistent_list_style'):
            content = self._ensure_consistent_list_style(content)

        if self.config.get('ensure_list_spacing'):
            content = self._fix_list_spacing(content)

        if self.config.get('fix_table_formatting'):
            content = self._fix_table_formatting(content)

        if self.config.get('fix_link_spacing'):
            content = self._fix_link_spacing(content)

        if self.config.get('fix_emphasis'):
            content = self._fix_emphasis(content)

        if self.config.get('remove_multiple_spaces'):
            content = self._remove_multiple_spaces(content)

        if self.config.get('trim_trailing_whitespace'):
            content = self._trim_trailing_whitespace(content)

        if self.config.get('max_blank_lines'):
            content = self._limit_blank_lines(content)

        if self.config.get('ensure_final_newline'):
            content = self._ensure_final_newline(content)

        return content

    def _standardize_line_endings(self, content: str) -> str:
        """Convert all line endings to LF."""
        content = content.replace('\r\n', '\n')
        content = content.replace('\r', '\n')
        return content

    def _fix_yaml_frontmatter(self, content: str) -> str:
        """Ensure YAML frontmatter is properly formatted."""
        # Check if content starts with frontmatter
        if not content.startswith('---'):
            return content

        # Find the closing ---
        lines = content.split('\n')
        frontmatter_end = -1

        for i in range(1, len(lines)):
            if lines[i].strip() == '---':
                frontmatter_end = i
                break

        if frontmatter_end == -1:
            return content

        # Extract frontmatter
        frontmatter_lines = lines[1:frontmatter_end]
        body_lines = lines[frontmatter_end + 1:]

        # Fix frontmatter formatting
        fixed_frontmatter = ['---']

        for line in frontmatter_lines:
            line = line.rstrip()

            # Skip empty lines in frontmatter
            if not line:
                continue

            # Ensure proper key: value spacing
            if ':' in line and not line.strip().startswith('#'):
                # Handle list items
                if line.strip().startswith('-'):
                    fixed_frontmatter.append(line)
                else:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()

                    # Ensure single space after colon
                    if value:
                        fixed_frontmatter.append(f'{key}: {value}')
                    else:
                        fixed_frontmatter.append(f'{key}:')
            else:
                fixed_frontmatter.append(line)

        fixed_frontmatter.append('---')

        # Ensure blank line after frontmatter
        if body_lines and body_lines[0].strip():
            fixed_frontmatter.append('')

        return '\n'.join(fixed_frontmatter + body_lines)

    def _ensure_space_after_heading(self, content: str) -> str:
        """Ensure headings have a space after the # symbols."""
        # Match headings without space: ##Text or ## Text (keep the space)
        content = re.sub(
            r'^(#{1,6})([^# \n])',
            r'\1 \2',
            content,
            flags=re.MULTILINE
        )
        return content

    def _ensure_space_after_list_marker(self, content: str) -> str:
        """Ensure list items have space after marker."""
        lines = content.split('\n')
        fixed_lines = []

        for line in lines:
            # Bullet lists
            if re.match(r'^\s*[-*+]([^ \n\t])', line):
                line = re.sub(r'^(\s*[-*+])([^ \n\t])', r'\1 \2', line)

            # Numbered lists
            if re.match(r'^\s*\d+\.([^ \n\t])', line):
                line = re.sub(r'^(\s*\d+\.)([^ \n\t])', r'\1 \2', line)

            # Task lists
            if re.match(r'^\s*[-*+]\s*\[[ xX]\]([^ \n\t])', line):
                line = re.sub(r'^(\s*[-*+]\s*\[[ xX]\])([^ \n\t])', r'\1 \2', line)

            fixed_lines.append(line)

        return '\n'.join(fixed_lines)

    def _ensure_consistent_list_style(self, content: str) -> str:
        """Ensure consistent list marker style (use - for bullets)."""
        lines = content.split('\n')
        fixed_lines = []

        for line in lines:
            # Convert * and + to -
            if re.match(r'^\s*[*+]\s', line):
                line = re.sub(r'^(\s*)[*+](\s)', r'\1-\2', line)

            fixed_lines.append(line)

        return '\n'.join(fixed_lines)

    def _fix_list_spacing(self, content: str) -> str:
        """Ensure proper spacing around lists."""
        lines = content.split('\n')
        fixed_lines = []

        for i, line in enumerate(lines):
            is_list_item = bool(re.match(r'^\s*[-*+]\s', line) or
                              re.match(r'^\s*\d+\.\s', line))
            prev_line = lines[i - 1] if i > 0 else ''
            next_line = lines[i + 1] if i < len(lines) - 1 else ''

            prev_is_list = bool(re.match(r'^\s*[-*+]\s', prev_line) or
                              re.match(r'^\s*\d+\.\s', prev_line))
            next_is_list = bool(re.match(r'^\s*[-*+]\s', next_line) or
                              re.match(r'^\s*\d+\.\s', next_line))

            # Add blank line before list if previous line is not list and not empty
            if is_list_item and not prev_is_list and prev_line.strip() and \
               i > 0 and not fixed_lines[-1].strip() == '':
                # Check if we're not already after a blank line
                if not (len(fixed_lines) > 0 and fixed_lines[-1].strip() == ''):
                    fixed_lines.append('')

            fixed_lines.append(line)

            # Add blank line after list if next line is not list and not empty
            if is_list_item and not next_is_list and next_line.strip() and \
               not next_line.strip() == '':
                # Check if next line isn't already blank
                if i + 1 < len(lines) and lines[i + 1].strip():
                    fixed_lines.append('')

        return '\n'.join(fixed_lines)

    def _fix_table_formatting(self, content: str) -> str:
        """Fix table formatting issues."""
        lines = content.split('\n')
        fixed_lines = []

        in_table = False

        for i, line in enumerate(lines):
            # Detect table line
            if '|' in line and line.strip().startswith('|'):
                in_table = True

                # Split by pipe and clean up
                cells = line.split('|')

                # Remove first and last empty elements
                if cells[0].strip() == '':
                    cells = cells[1:]
                if cells and cells[-1].strip() == '':
                    cells = cells[:-1]

                # Clean and pad cells
                cleaned_cells = [cell.strip() for cell in cells]

                # Check if this is a separator row
                is_separator = all(
                    re.match(r'^:?-+:?$', cell.strip())
                    for cell in cleaned_cells if cell.strip()
                )

                if is_separator:
                    # Ensure proper separator format
                    cleaned_cells = [
                        re.sub(r'^:?-+:?$', lambda m: '-' * max(3, len(m.group())), cell)
                        for cell in cleaned_cells
                    ]

                # Reconstruct line
                line = '| ' + ' | '.join(cleaned_cells) + ' |'

            else:
                if in_table:
                    # Just exited table, ensure blank line after
                    in_table = False
                    if line.strip() and i > 0:
                        fixed_lines.append('')

            fixed_lines.append(line)

        return '\n'.join(fixed_lines)

    def _fix_link_spacing(self, content: str) -> str:
        """Fix spacing issues in links."""
        # Remove spaces inside link brackets
        content = re.sub(r'\[\s+', '[', content)
        content = re.sub(r'\s+\]', ']', content)

        # Remove spaces inside parentheses for links
        content = re.sub(r'\]\(\s+', '](', content)
        content = re.sub(r'\s+\)', ')', content)

        return content

    def _fix_emphasis(self, content: str) -> str:
        """Fix emphasis (bold/italic) formatting."""
        # Remove spaces inside emphasis markers
        # Bold: **text** or __text__
        content = re.sub(r'\*\*\s+', '**', content)
        content = re.sub(r'\s+\*\*', '**', content)
        content = re.sub(r'__\s+', '__', content)
        content = re.sub(r'\s+__', '__', content)

        # Italic: *text* or _text_
        content = re.sub(r'(?<!\*)\*\s+', '*', content)
        content = re.sub(r'\s+\*(?!\*)', '*', content)
        content = re.sub(r'(?<!_)_\s+', '_', content)
        content = re.sub(r'\s+_(?!_)', '_', content)

        return content

    def _remove_multiple_spaces(self, content: str) -> str:
        """Remove multiple consecutive spaces (except in code blocks)."""
        lines = content.split('\n')
        fixed_lines = []
        in_code_block = False

        for line in lines:
            # Check for code block markers
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                fixed_lines.append(line)
                continue

            # Don't modify lines in code blocks
            if in_code_block:
                fixed_lines.append(line)
                continue

            # Replace multiple spaces with single space (preserve leading spaces)
            leading_spaces = len(line) - len(line.lstrip(' '))
            content_part = line[leading_spaces:]

            # Don't touch table separators
            if not re.match(r'^[\s|:-]+$', content_part):
                content_part = re.sub(r'  +', ' ', content_part)

            line = ' ' * leading_spaces + content_part
            fixed_lines.append(line)

        return '\n'.join(fixed_lines)

    def _trim_trailing_whitespace(self, content: str) -> str:
        """Remove trailing whitespace from lines."""
        lines = content.split('\n')
        return '\n'.join(line.rstrip() for line in lines)

    def _limit_blank_lines(self, content: str) -> str:
        """Limit consecutive blank lines."""
        max_blanks = self.config.get('max_blank_lines', 2)

        # Replace 3+ consecutive newlines with max allowed
        pattern = r'\n{' + str(max_blanks + 2) + r',}'
        replacement = '\n' * (max_blanks + 1)

        content = re.sub(pattern, replacement, content)
        return content

    def _ensure_final_newline(self, content: str) -> str:
        """Ensure file ends with a single newline."""
        content = content.rstrip('\n')
        content += '\n'
        return content

    def validate(self, content: str) -> List[Tuple[int, str]]:
        """
        Validate content and return list of issues.

        Args:
            content: Markdown content to validate

        Returns:
            List of (line_number, issue_description) tuples
        """
        issues = []
        lines = content.split('\n')

        for i, line in enumerate(lines, 1):
            # Check for trailing whitespace
            if line.rstrip() != line:
                issues.append((i, 'Trailing whitespace'))

            # Check for tabs (should use spaces)
            if '\t' in line and not line.strip().startswith('```'):
                issues.append((i, 'Tab character found (use spaces)'))

            # Check heading format
            if line.startswith('#'):
                if not re.match(r'^#{1,6} ', line):
                    issues.append((i, 'Heading missing space after #'))

            # Check list format
            if re.match(r'^\s*[-*+]', line):
                if not re.match(r'^\s*[-*+] ', line):
                    issues.append((i, 'List item missing space after marker'))

        return issues


def main():
    """CLI entry point for the linter."""
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description='Lint Obsidian markdown files'
    )
    parser.add_argument('file', help='File to lint')
    parser.add_argument('--check', action='store_true',
                       help='Only check for issues, do not fix')
    parser.add_argument('--validate', action='store_true',
                       help='Validate and report issues')

    args = parser.parse_args()

    try:
        with open(args.file, 'r', encoding='utf-8') as f:
            content = f.read()

        linter = ObsidianLinter()

        if args.validate:
            issues = linter.validate(content)
            if issues:
                print(f'Found {len(issues)} issues:')
                for line_num, issue in issues:
                    print(f'  Line {line_num}: {issue}')
                return 1
            else:
                print('No issues found!')
                return 0

        linted = linter.lint(content)

        if args.check:
            if linted == content:
                print('File is already properly formatted!')
                return 0
            else:
                print('File needs formatting')
                return 1

        # Write linted content back
        with open(args.file, 'w', encoding='utf-8') as f:
            f.write(linted)

        print(f'Successfully linted {args.file}')
        return 0

    except Exception as e:
        print(f'Error: {e}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    exit(main())
