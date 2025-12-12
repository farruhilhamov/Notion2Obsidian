#!/usr/bin/env python3
"""
Notion Database to Obsidian Dataview Converter
Converts Notion databases (Base files) to Obsidian Dataview format.
"""

import csv
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


class NotionDatabaseConverter:
    """Converts Notion databases to Obsidian Dataview format."""

    def __init__(self):
        self.property_type_map = {
            'text': 'text',
            'number': 'number',
            'select': 'text',
            'multi_select': 'list',
            'date': 'date',
            'person': 'text',
            'files': 'text',
            'checkbox': 'boolean',
            'url': 'text',
            'email': 'text',
            'phone': 'text',
            'formula': 'text',
            'relation': 'list',
            'rollup': 'text',
            'created_time': 'date',
            'created_by': 'text',
            'last_edited_time': 'date',
            'last_edited_by': 'text',
        }

    def convert_database_folder(self, database_path: Path, output_dir: Path) -> Dict[str, Any]:
        """
        Convert a Notion database (folder with CSV) to Obsidian Dataview format.

        Args:
            database_path: Path to database folder or CSV file
            output_dir: Output directory for converted files

        Returns:
            Dictionary with conversion results
        """
        # Find CSV file
        csv_file = self._find_csv_file(database_path)
        if not csv_file:
            return {'error': 'No CSV file found in database'}

        # Parse CSV
        rows, headers = self._parse_database_csv(csv_file)

        # Create individual note files for each row
        created_files = []
        for i, row in enumerate(rows):
            note_file = self._create_database_note(row, headers, output_dir, i)
            created_files.append(note_file)

        # Create index/view file
        index_file = self._create_database_index(
            database_path.stem if database_path.is_dir() else csv_file.stem,
            headers,
            output_dir
        )

        return {
            'csv_file': str(csv_file),
            'rows_converted': len(rows),
            'files_created': created_files,
            'index_file': str(index_file),
            'headers': headers
        }

    def _find_csv_file(self, path: Path) -> Optional[Path]:
        """Find CSV file in database folder."""
        if path.is_file() and path.suffix == '.csv':
            return path

        if path.is_dir():
            csv_files = list(path.glob('*.csv'))
            if csv_files:
                return csv_files[0]

        return None

    def _parse_database_csv(self, csv_file: Path) -> tuple[List[Dict], List[Dict]]:
        """
        Parse Notion database CSV.

        Returns:
            Tuple of (rows, headers_with_types)
        """
        rows = []
        headers = []

        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            # Extract headers with type information
            original_headers = reader.fieldnames or []
            for header in original_headers:
                # Notion exports headers as "PropertyName" or "PropertyName (Type)"
                match = re.match(r'^(.+?)\s*(?:\((.+?)\))?$', header)
                if match:
                    name = match.group(1).strip()
                    prop_type = match.group(2).lower() if match.group(2) else 'text'
                    headers.append({
                        'original': header,
                        'name': name,
                        'type': prop_type,
                        'key': self._sanitize_key(name)
                    })

            # Read rows
            for row in reader:
                cleaned_row = {}
                for i, header_info in enumerate(headers):
                    value = row.get(header_info['original'], '')
                    cleaned_row[header_info['key']] = self._convert_value(
                        value,
                        header_info['type']
                    )
                rows.append(cleaned_row)

        return rows, headers

    def _sanitize_key(self, name: str) -> str:
        """Convert property name to valid YAML key."""
        # Convert to lowercase, replace spaces with underscores
        key = name.lower()
        key = re.sub(r'[^\w\s-]', '', key)
        key = re.sub(r'[-\s]+', '_', key)
        return key

    def _convert_value(self, value: str, prop_type: str) -> Any:
        """Convert Notion value to appropriate Python type."""
        if not value or value.strip() == '':
            return None

        value = value.strip()

        # Checkbox
        if prop_type == 'checkbox':
            return value.lower() in ['yes', 'true', 'checked', '☑', '✓']

        # Multi-select (comma-separated)
        if prop_type == 'multi_select' or prop_type == 'multi-select':
            return [item.strip() for item in value.split(',') if item.strip()]

        # Number
        if prop_type == 'number':
            try:
                if '.' in value:
                    return float(value)
                return int(value)
            except ValueError:
                return value

        # Date
        if prop_type == 'date' or 'time' in prop_type:
            return self._parse_date(value)

        # Default: return as string
        return value

    def _parse_date(self, date_str: str) -> str:
        """Parse and standardize date format."""
        if not date_str:
            return None

        # Try common formats
        formats = [
            '%Y-%m-%d',
            '%B %d, %Y',
            '%d/%m/%Y',
            '%m/%d/%Y',
            '%Y/%m/%d',
            '%Y-%m-%dT%H:%M:%S',
            '%Y-%m-%d %H:%M:%S',
        ]

        for fmt in formats:
            try:
                dt = datetime.strptime(date_str.strip(), fmt)
                return dt.strftime('%Y-%m-%d')
            except ValueError:
                continue

        # If no format matches, return original
        return date_str

    def _create_database_note(
        self,
        row: Dict,
        headers: List[Dict],
        output_dir: Path,
        index: int
    ) -> Path:
        """Create individual note file for database row."""
        output_dir.mkdir(parents=True, exist_ok=True)

        # Try to get a good filename from the row
        # First try "Name" field, then "Title", then first text field
        filename = None
        for key in ['name', 'title', 'page', 'item']:
            if key in row and row[key]:
                filename = self._sanitize_filename(str(row[key]))
                break

        if not filename:
            # Use first non-empty value
            for value in row.values():
                if value:
                    filename = self._sanitize_filename(str(value))
                    break

        if not filename:
            filename = f'item_{index + 1}'

        filepath = output_dir / f'{filename}.md'

        # Handle duplicate filenames
        counter = 1
        while filepath.exists():
            filepath = output_dir / f'{filename}_{counter}.md'
            counter += 1

        # Build frontmatter
        frontmatter = self._build_frontmatter(row, headers)

        # Build content
        content = self._build_note_content(row, headers)

        # Write file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('---\n')
            f.write(frontmatter)
            f.write('---\n\n')
            f.write(content)

        return filepath

    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename for filesystem."""
        # Remove invalid characters
        filename = re.sub(r'[<>:"/\\|?*]', '-', filename)
        # Limit length
        if len(filename) > 100:
            filename = filename[:100]
        # Remove leading/trailing spaces and dots
        filename = filename.strip('. ')
        return filename or 'untitled'

    def _build_frontmatter(self, row: Dict, headers: List[Dict]) -> str:
        """Build YAML frontmatter from row data."""
        lines = []

        for header in headers:
            key = header['key']
            value = row.get(key)

            if value is None:
                continue

            # Format value for YAML
            if isinstance(value, bool):
                lines.append(f'{key}: {str(value).lower()}')
            elif isinstance(value, list):
                if value:
                    lines.append(f'{key}:')
                    for item in value:
                        lines.append(f'  - {item}')
            elif isinstance(value, (int, float)):
                lines.append(f'{key}: {value}')
            else:
                # String value - quote if necessary
                value_str = str(value)
                if any(char in value_str for char in [':', '#', '[', ']', '{', '}', ',', '&', '*', '!', '|', '>', '@', '`']):
                    value_str = value_str.replace('"', '\\"')
                    lines.append(f'{key}: "{value_str}"')
                else:
                    lines.append(f'{key}: {value_str}')

        # Add database tag
        lines.append('tags:')
        lines.append('  - database-item')

        return '\n'.join(lines) + '\n'

    def _build_note_content(self, row: Dict, headers: List[Dict]) -> str:
        """Build note content from row data."""
        # Get the main title
        title = None
        for key in ['name', 'title', 'page', 'item']:
            if key in row and row[key]:
                title = str(row[key])
                break

        if not title:
            for value in row.values():
                if value:
                    title = str(value)
                    break

        if not title:
            title = 'Untitled'

        content = f'# {title}\n\n'

        # Add property table for quick reference
        content += '## Properties\n\n'
        content += '| Property | Value |\n'
        content += '|----------|-------|\n'

        for header in headers:
            key = header['key']
            name = header['name']
            value = row.get(key)

            if value is not None:
                if isinstance(value, list):
                    value_str = ', '.join(str(v) for v in value)
                elif isinstance(value, bool):
                    value_str = '✓' if value else '✗'
                else:
                    value_str = str(value)

                content += f'| {name} | {value_str} |\n'

        content += '\n## Notes\n\n'
        content += '*Add your notes here...*\n'

        return content

    def _create_database_index(
        self,
        database_name: str,
        headers: List[Dict],
        output_dir: Path
    ) -> Path:
        """Create index file with Dataview queries."""
        index_path = output_dir / f'{database_name}_Index.md'

        content = f'# {database_name} Database\n\n'
        content += f'*Converted from Notion database*\n\n'

        # Add Dataview table query
        content += '## All Items\n\n'
        content += '```dataview\n'
        content += 'TABLE '

        # Add main properties
        display_props = []
        for header in headers[:5]:  # Show first 5 properties
            if header['key'] not in ['name', 'title']:
                display_props.append(f'{header["key"]} as "{header["name"]}"')

        content += ', '.join(display_props)
        content += '\n'
        content += f'FROM "{output_dir.name}"\n'
        content += 'WHERE contains(tags, "database-item")\n'
        content += 'SORT file.name ASC\n'
        content += '```\n\n'

        # Add filtered views
        content += '## Quick Views\n\n'

        # Find checkbox properties for status views
        checkbox_props = [h for h in headers if h['type'] == 'checkbox']
        if checkbox_props:
            content += '### By Status\n\n'
            for prop in checkbox_props[:2]:  # First 2 checkbox properties
                content += f'**{prop["name"]} = Yes:**\n'
                content += '```dataview\n'
                content += 'TABLE '
                content += ', '.join(display_props[:3])
                content += '\n'
                content += f'FROM "{output_dir.name}"\n'
                content += f'WHERE {prop["key"]} = true\n'
                content += '```\n\n'

        # Find date properties for timeline views
        date_props = [h for h in headers if 'date' in h['type'] or 'time' in h['type']]
        if date_props:
            content += '### Timeline\n\n'
            prop = date_props[0]
            content += f'**Sorted by {prop["name"]}:**\n'
            content += '```dataview\n'
            content += f'TABLE {prop["key"]} as "Date", '
            content += ', '.join(display_props[:2])
            content += '\n'
            content += f'FROM "{output_dir.name}"\n'
            content += f'WHERE {prop["key"]}\n'
            content += f'SORT {prop["key"]} DESC\n'
            content += '```\n\n'

        # Add list view
        content += '### List View\n\n'
        content += '```dataview\n'
        content += 'LIST\n'
        content += f'FROM "{output_dir.name}"\n'
        content += 'WHERE contains(tags, "database-item")\n'
        content += 'SORT file.name ASC\n'
        content += '```\n\n'

        # Add instructions
        content += '## How to Use\n\n'
        content += '1. Install the [Dataview plugin](https://github.com/blacksmithgu/obsidian-dataview) in Obsidian\n'
        content += '2. Enable Dataview in Settings → Community Plugins\n'
        content += '3. The tables above will automatically populate with your data\n'
        content += '4. Click on any item to edit it\n'
        content += '5. Modify frontmatter properties to update the database\n\n'

        # Add property reference
        content += '## Available Properties\n\n'
        for header in headers:
            content += f'- **{header["name"]}** (`{header["key"]}`) - {header["type"]}\n'

        content += '\n## Custom Queries\n\n'
        content += 'You can create your own Dataview queries. Examples:\n\n'
        content += '```dataview\n'
        content += '# Search for specific text\n'
        content += 'TABLE\n'
        content += f'FROM "{output_dir.name}"\n'
        content += 'WHERE contains(file.name, "search-term")\n'
        content += '```\n\n'
        content += '```dataview\n'
        content += '# Count items\n'
        content += 'TABLE length(rows) as "Count"\n'
        content += f'FROM "{output_dir.name}"\n'
        content += 'GROUP BY tags\n'
        content += '```\n'

        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return index_path

    def create_inline_database(self, rows: List[Dict], headers: List[Dict]) -> str:
        """
        Create inline database as markdown table (for simple databases).

        Args:
            rows: List of row dictionaries
            headers: List of header information

        Returns:
            Markdown table string
        """
        if not rows or not headers:
            return ''

        # Build header row
        header_names = [h['name'] for h in headers]
        table = '| ' + ' | '.join(header_names) + ' |\n'
        table += '| ' + ' | '.join(['---' for _ in headers]) + ' |\n'

        # Build data rows
        for row in rows:
            cells = []
            for header in headers:
                value = row.get(header['key'], '')

                if value is None:
                    cells.append('')
                elif isinstance(value, bool):
                    cells.append('✓' if value else '✗')
                elif isinstance(value, list):
                    cells.append(', '.join(str(v) for v in value))
                else:
                    cells.append(str(value))

            table += '| ' + ' | '.join(cells) + ' |\n'

        return table


def main():
    """CLI entry point for database converter."""
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description='Convert Notion database to Obsidian Dataview format'
    )
    parser.add_argument('database_path', help='Path to Notion database folder or CSV file')
    parser.add_argument('output_dir', help='Output directory for converted notes')
    parser.add_argument('--inline', action='store_true',
                       help='Create inline table instead of separate files')

    args = parser.parse_args()

    try:
        converter = NotionDatabaseConverter()

        database_path = Path(args.database_path)
        output_dir = Path(args.output_dir)

        if args.inline:
            # Parse CSV and create inline table
            csv_file = converter._find_csv_file(database_path)
            if not csv_file:
                print('Error: No CSV file found')
                return 1

            rows, headers = converter._parse_database_csv(csv_file)
            table = converter.create_inline_database(rows, headers)
            print(table)
        else:
            # Convert to Dataview format
            result = converter.convert_database_folder(database_path, output_dir)

            if 'error' in result:
                print(f'Error: {result["error"]}')
                return 1

            print(f'\n✅ Database conversion successful!')
            print(f'📊 Converted {result["rows_converted"]} rows')
            print(f'📁 Created {len(result["files_created"])} note files')
            print(f'📑 Index file: {result["index_file"]}')
            print(f'\n💡 Next steps:')
            print(f'1. Install Dataview plugin in Obsidian')
            print(f'2. Open the index file: {result["index_file"]}')
            print(f'3. Your database is ready to use!')

        return 0

    except Exception as e:
        print(f'\n❌ Error: {e}')
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    exit(main())
