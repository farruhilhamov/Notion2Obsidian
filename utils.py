#!/usr/bin/env python3
"""
Utility functions for Notion to Obsidian conversion.
"""

import re
import csv
from pathlib import Path
from typing import Dict, Tuple, List, Optional
from datetime import datetime


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for use in filesystem.

    Args:
        filename: Original filename

    Returns:
        Sanitized filename safe for filesystem
    """
    # Remove or replace invalid characters
    invalid_chars = r'[<>:"/\\|?*]'
    filename = re.sub(invalid_chars, '-', filename)

    # Remove leading/trailing spaces and dots
    filename = filename.strip('. ')

    # Replace multiple spaces with single space
    filename = re.sub(r'\s+', ' ', filename)

    # Limit length (most filesystems support 255 chars)
    if len(filename) > 200:
        filename = filename[:200]

    # Ensure it's not empty
    if not filename:
        filename = 'untitled'

    return filename


def extract_frontmatter(content: str) -> Tuple[Optional[Dict], str]:
    """
    Extract YAML frontmatter from markdown content.

    Args:
        content: Markdown content

    Returns:
        Tuple of (frontmatter dict or None, body content)
    """
    if not content.startswith('---'):
        return None, content

    # Find the closing ---
    lines = content.split('\n')
    frontmatter_end = -1

    for i in range(1, len(lines)):
        if lines[i].strip() == '---':
            frontmatter_end = i
            break

    if frontmatter_end == -1:
        return None, content

    # Extract frontmatter
    frontmatter_lines = lines[1:frontmatter_end]
    body = '\n'.join(lines[frontmatter_end + 1:])

    # Parse frontmatter
    frontmatter = {}
    current_key = None
    current_list = []

    for line in frontmatter_lines:
        line = line.rstrip()

        if not line:
            continue

        # Check if it's a list item
        if line.strip().startswith('-'):
            if current_key:
                item = line.strip()[1:].strip()
                current_list.append(item)
            continue

        # Check if it's a key-value pair
        if ':' in line and not line.strip().startswith('#'):
            # Save previous list if any
            if current_key and current_list:
                frontmatter[current_key] = current_list
                current_list = []

            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()

            current_key = key

            if value:
                frontmatter[key] = value
            # else it's a list, wait for items

    # Save last list if any
    if current_key and current_list:
        frontmatter[current_key] = current_list

    return frontmatter, body


def parse_notion_csv(csv_path: Path) -> List[Dict]:
    """
    Parse Notion CSV export (database view).

    Args:
        csv_path: Path to CSV file

    Returns:
        List of dictionaries representing rows
    """
    rows = []

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            # Clean up the row data
            cleaned_row = {}
            for key, value in row.items():
                # Remove Notion's property type suffix (e.g., "Name (Text)")
                clean_key = re.sub(r'\s*\([^)]+\)$', '', key)
                cleaned_row[clean_key] = value

            rows.append(cleaned_row)

    return rows


def convert_notion_date(date_str: str) -> str:
    """
    Convert Notion date format to standard format.

    Args:
        date_str: Notion date string

    Returns:
        Standardized date string (YYYY-MM-DD)
    """
    if not date_str:
        return ''

    # Notion date formats can vary
    # Try common formats
    formats = [
        '%B %d, %Y',  # December 12, 2025
        '%Y-%m-%d',   # 2025-12-12
        '%d/%m/%Y',   # 12/12/2025
        '%m/%d/%Y',   # 12/12/2025
        '%Y/%m/%d',   # 2025/12/12
    ]

    for fmt in formats:
        try:
            dt = datetime.strptime(date_str.strip(), fmt)
            return dt.strftime('%Y-%m-%d')
        except ValueError:
            continue

    # If no format matches, return original
    return date_str


def convert_notion_checkbox(value: str) -> bool:
    """
    Convert Notion checkbox value to boolean.

    Args:
        value: Notion checkbox value

    Returns:
        Boolean value
    """
    if not value:
        return False

    value = value.lower().strip()
    return value in ['yes', 'true', '1', 'checked', 'x']


def create_obsidian_link(page_name: str, alias: Optional[str] = None) -> str:
    """
    Create Obsidian wikilink.

    Args:
        page_name: Name of the page to link to
        alias: Optional display text

    Returns:
        Obsidian wikilink string
    """
    if alias and alias != page_name:
        return f'[[{page_name}|{alias}]]'
    return f'[[{page_name}]]'


def create_obsidian_tag(tag: str) -> str:
    """
    Create Obsidian tag.

    Args:
        tag: Tag name

    Returns:
        Obsidian tag string
    """
    # Remove spaces and special characters
    tag = re.sub(r'[^\w-]', '', tag.replace(' ', '-'))

    # Ensure it starts with #
    if not tag.startswith('#'):
        tag = f'#{tag}'

    return tag


def markdown_table_to_dict(table_text: str) -> List[Dict]:
    """
    Parse markdown table to list of dictionaries.

    Args:
        table_text: Markdown table text

    Returns:
        List of dictionaries representing table rows
    """
    lines = [line.strip() for line in table_text.split('\n') if line.strip()]

    if len(lines) < 2:
        return []

    # Parse header
    header_line = lines[0]
    headers = [cell.strip() for cell in header_line.split('|') if cell.strip()]

    # Skip separator line (line 1)

    # Parse data rows
    rows = []
    for line in lines[2:]:
        cells = [cell.strip() for cell in line.split('|') if cell.strip()]

        if len(cells) == len(headers):
            row_dict = dict(zip(headers, cells))
            rows.append(row_dict)

    return rows


def dict_to_markdown_table(data: List[Dict]) -> str:
    """
    Convert list of dictionaries to markdown table.

    Args:
        data: List of dictionaries

    Returns:
        Markdown table string
    """
    if not data:
        return ''

    # Get headers from first row
    headers = list(data[0].keys())

    # Calculate column widths
    col_widths = {header: len(header) for header in headers}
    for row in data:
        for header in headers:
            value = str(row.get(header, ''))
            col_widths[header] = max(col_widths[header], len(value))

    # Build table
    lines = []

    # Header row
    header_cells = [header.ljust(col_widths[header]) for header in headers]
    lines.append('| ' + ' | '.join(header_cells) + ' |')

    # Separator row
    separator_cells = ['-' * col_widths[header] for header in headers]
    lines.append('| ' + ' | '.join(separator_cells) + ' |')

    # Data rows
    for row in data:
        cells = [str(row.get(header, '')).ljust(col_widths[header]) for header in headers]
        lines.append('| ' + ' | '.join(cells) + ' |')

    return '\n'.join(lines)


def extract_tags_from_text(text: str) -> List[str]:
    """
    Extract hashtags from text.

    Args:
        text: Text content

    Returns:
        List of tags (without #)
    """
    # Match hashtags (word characters after #)
    tags = re.findall(r'#([\w-]+)', text)
    return tags


def replace_notion_variables(text: str, variables: Dict[str, str]) -> str:
    """
    Replace Notion template variables in text.

    Args:
        text: Text with variables
        variables: Dictionary of variable replacements

    Returns:
        Text with variables replaced
    """
    # Notion uses {{variable}} syntax
    for key, value in variables.items():
        text = text.replace(f'{{{{{key}}}}}', value)

    return text


def convert_notion_formula(formula: str) -> str:
    """
    Convert Notion formula to Obsidian Dataview format.

    Args:
        formula: Notion formula

    Returns:
        Dataview formula (simplified conversion)
    """
    # This is a simplified conversion
    # Full formula conversion would require parsing the formula syntax

    # Common conversions
    formula = formula.replace('prop("', 'this.')
    formula = formula.replace('")', '')

    return formula


def clean_notion_export_artifacts(content: str) -> str:
    """
    Remove Notion export artifacts from content.

    Args:
        content: Markdown content

    Returns:
        Cleaned content
    """
    # Remove Notion's export timestamp comments
    content = re.sub(r'<!-- Exported from Notion.*?-->', '', content, flags=re.MULTILINE)

    # Remove empty HTML comments
    content = re.sub(r'<!--\s*-->', '', content)

    # Remove Notion's database view markers
    content = re.sub(r'<!-- database:.+?-->', '', content, flags=re.MULTILINE)

    return content


def ensure_valid_yaml_value(value: any) -> str:
    """
    Ensure value is valid for YAML frontmatter.

    Args:
        value: Value to convert

    Returns:
        YAML-safe string
    """
    if value is None:
        return ''

    value_str = str(value)

    # Quote values that contain special YAML characters
    if any(char in value_str for char in [':', '#', '[', ']', '{', '}', ',', '&', '*', '!', '|', '>', '@', '`']):
        # Escape quotes in the value
        value_str = value_str.replace('"', '\\"')
        return f'"{value_str}"'

    return value_str


def get_relative_path(from_path: Path, to_path: Path) -> str:
    """
    Get relative path from one file to another.

    Args:
        from_path: Source file path
        to_path: Target file path

    Returns:
        Relative path string
    """
    try:
        rel_path = to_path.relative_to(from_path.parent)
        return str(rel_path).replace('\\', '/')
    except ValueError:
        # Files are not in relative paths, return absolute
        return str(to_path)


def slugify(text: str) -> str:
    """
    Convert text to slug format.

    Args:
        text: Text to slugify

    Returns:
        Slugified text
    """
    # Convert to lowercase
    text = text.lower()

    # Replace spaces with hyphens
    text = re.sub(r'\s+', '-', text)

    # Remove special characters
    text = re.sub(r'[^\w-]', '', text)

    # Remove multiple hyphens
    text = re.sub(r'-+', '-', text)

    # Remove leading/trailing hyphens
    text = text.strip('-')

    return text


def word_count(text: str) -> int:
    """
    Count words in text (excluding code blocks and frontmatter).

    Args:
        text: Markdown text

    Returns:
        Word count
    """
    # Remove frontmatter
    if text.startswith('---'):
        parts = text.split('---', 2)
        if len(parts) >= 3:
            text = parts[2]

    # Remove code blocks
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)

    # Remove inline code
    text = re.sub(r'`[^`]+`', '', text)

    # Remove links but keep text
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)

    # Remove markdown formatting
    text = re.sub(r'[#*_~`]', '', text)

    # Count words
    words = text.split()
    return len(words)


def reading_time(text: str, wpm: int = 200) -> int:
    """
    Calculate reading time in minutes.

    Args:
        text: Text to analyze
        wpm: Words per minute reading speed

    Returns:
        Reading time in minutes
    """
    words = word_count(text)
    minutes = max(1, round(words / wpm))
    return minutes
