#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Notion to Obsidian Converter
Converts exported Notion pages with subpages to beautifully formatted Obsidian pages.
Handles lists, databases, and all Notion features.
"""

import os
import re
import shutil
import argparse
import sys
import io
from pathlib import Path
from typing import Dict, List, Set
import html

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from obsidian_linter import ObsidianLinter
from notion_database import NotionDatabaseConverter
from utils import (
    sanitize_filename,
    extract_frontmatter,
    parse_notion_csv,
    convert_notion_date,
)


class NotionToObsidianConverter:
    """Main converter class for Notion to Obsidian conversion."""

    def __init__(self, input_dir: str, output_dir: str, verbose: bool = False):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.verbose = verbose
        self.linter = ObsidianLinter()
        self.db_converter = NotionDatabaseConverter()
        self.file_mapping: Dict[str, str] = {}  # Maps old paths to new paths
        self.processed_files: Set[str] = set()
        self.databases_converted = []

    def log(self, message: str):
        """Print log message if verbose mode is enabled."""
        if self.verbose:
            print(f"[INFO] {message}")

    def convert_all(self):
        """Convert all Notion files to Obsidian format."""
        if not self.input_dir.exists():
            raise FileNotFoundError(f"Input directory not found: {self.input_dir}")

        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.log(f"Starting conversion from {self.input_dir} to {self.output_dir}")

        # First pass: detect and convert CSV databases
        self._convert_csv_databases()

        # Second pass: collect all markdown files and create mapping
        self._build_file_mapping()

        # Third pass: convert all files
        for md_file in self.input_dir.rglob("*.md"):
            self._convert_file(md_file)

        # Fourth pass: copy all assets (images, PDFs, etc.)
        self._copy_assets()

        # Fifth pass: embed database queries in pages with matching folders
        self._embed_all_database_queries()

        self.log(f"Conversion complete! Processed {len(self.processed_files)} files.")
        if self.databases_converted:
            self.log(f"Converted {len(self.databases_converted)} databases to Dataview format.")

    def _build_file_mapping(self):
        """Build mapping of Notion file names to Obsidian file names."""
        for md_file in self.input_dir.rglob("*.md"):
            relative_path = md_file.relative_to(self.input_dir)

            # Remove Notion's UUID from filename
            clean_name = self._clean_notion_filename(md_file.stem)

            # Create new path maintaining directory structure
            new_relative_path = relative_path.parent / f"{clean_name}.md"
            new_path = self.output_dir / new_relative_path

            self.file_mapping[str(md_file)] = str(new_path)

    def _clean_notion_filename(self, filename: str) -> str:
        """Remove Notion's UUID suffix from filename."""
        # Notion adds UUIDs like "Page Name 8a7b3c4d5e6f7g8h9i0j"
        # Remove the trailing UUID (32 hex chars or formatted UUID)
        cleaned = re.sub(r'\s+[a-f0-9]{32}$', '', filename, flags=re.IGNORECASE)
        cleaned = re.sub(r'\s+[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$',
                        '', cleaned, flags=re.IGNORECASE)
        return sanitize_filename(cleaned)

    def _convert_file(self, md_file: Path):
        """Convert a single Notion markdown file to Obsidian format."""
        if str(md_file) in self.processed_files:
            return

        self.log(f"Converting: {md_file.name}")

        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Convert content
        converted = self._convert_content(content, md_file)

        # Lint the converted content
        linted = self.linter.lint(converted)

        # Get output path
        output_path = Path(self.file_mapping[str(md_file)])
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Write converted file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(linted)

        self.processed_files.add(str(md_file))
        self.log(f"Saved: {output_path}")

    def _convert_content(self, content: str, source_file: Path) -> str:
        """Convert Notion markdown content to Obsidian format."""
        # Extract and convert frontmatter
        frontmatter, body = extract_frontmatter(content)

        # Add Notion metadata to frontmatter
        if frontmatter is None:
            frontmatter = {}

        frontmatter['source'] = 'notion'
        frontmatter['created'] = self._get_file_date(source_file)

        # Convert various Notion elements
        body = self._convert_headings(body)
        body = self._convert_lists(body)
        body = self._convert_checkboxes(body)
        body = self._convert_code_blocks(body)
        body = self._convert_callouts(body)
        body = self._convert_tables(body)
        body = self._convert_links(body, source_file)
        body = self._convert_images(body, source_file)
        body = self._convert_notion_toggles(body)
        body = self._convert_databases(body)
        body = self._decode_html_entities(body)

        # Reconstruct with frontmatter
        if frontmatter:
            frontmatter_text = "---\n"
            for key, value in frontmatter.items():
                if isinstance(value, list):
                    frontmatter_text += f"{key}:\n"
                    for item in value:
                        frontmatter_text += f"  - {item}\n"
                else:
                    frontmatter_text += f"{key}: {value}\n"
            frontmatter_text += "---\n\n"
            body = frontmatter_text + body

        return body

    def _get_file_date(self, file_path: Path) -> str:
        """Get file creation/modification date."""
        import datetime
        timestamp = file_path.stat().st_mtime
        return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')

    def _convert_headings(self, content: str) -> str:
        """Ensure proper heading format."""
        # Add space after # if missing
        content = re.sub(r'^(#{1,6})([^# \n])', r'\1 \2', content, flags=re.MULTILINE)
        return content

    def _convert_lists(self, content: str) -> str:
        """Convert Notion lists to proper Obsidian format."""
        lines = content.split('\n')
        converted_lines = []

        for i, line in enumerate(lines):
            # Fix bullet lists - ensure space after dash
            if re.match(r'^\s*-[^ \n]', line):
                line = re.sub(r'^(\s*)-([^ \n])', r'\1- \2', line)

            # Fix numbered lists - ensure space after number
            line = re.sub(r'^(\s*\d+\.)[^ \n]', r'\1 ', line)

            # Convert Notion's nested lists (indentation)
            # Notion uses tabs, Obsidian prefers 2/4 spaces
            if line.startswith('\t'):
                indent_level = len(line) - len(line.lstrip('\t'))
                line = '  ' * indent_level + line.lstrip('\t')

            converted_lines.append(line)

        return '\n'.join(converted_lines)

    def _convert_checkboxes(self, content: str) -> str:
        """Convert Notion checkboxes to Obsidian task format."""
        # Notion exports checkboxes as "- [ ]" or "- [x]"
        # Ensure proper spacing
        content = re.sub(r'^\s*-\s*\[\s*\]', '- [ ]', content, flags=re.MULTILINE)
        content = re.sub(r'^\s*-\s*\[x\]', '- [x]', content, flags=re.MULTILINE | re.IGNORECASE)
        return content

    def _convert_code_blocks(self, content: str) -> str:
        """Convert Notion code blocks to Obsidian format."""
        # Notion sometimes doesn't specify language
        # Ensure code blocks are properly formatted
        lines = content.split('\n')
        converted_lines = []
        in_code_block = False

        for line in lines:
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                # Ensure there's a newline before code block starts
                if in_code_block and converted_lines and converted_lines[-1].strip():
                    converted_lines.append('')

            converted_lines.append(line)

            # Ensure there's a newline after code block ends
            if not in_code_block and line.strip() == '```':
                if converted_lines[-1].strip() == '```':
                    converted_lines.append('')

        return '\n'.join(converted_lines)

    def _convert_callouts(self, content: str) -> str:
        """Convert Notion callouts/alerts to Obsidian callouts."""
        # Notion uses blockquotes for callouts
        # Convert to Obsidian callout syntax

        # Pattern for Notion callouts (blockquotes with emoji/icon)
        callout_patterns = {
            r'💡': 'tip',
            r'⚠️': 'warning',
            r'❗': 'important',
            r'ℹ️': 'info',
            r'📝': 'note',
            r'✅': 'success',
            r'❌': 'error',
            r'🔥': 'danger',
        }

        lines = content.split('\n')
        converted_lines = []
        i = 0

        while i < len(lines):
            line = lines[i]

            # Check if line is a blockquote with an emoji
            if line.strip().startswith('>'):
                matched = False
                for emoji, callout_type in callout_patterns.items():
                    if emoji in line:
                        # Convert to Obsidian callout
                        content_text = line.replace('>', '').replace(emoji, '').strip()
                        converted_lines.append(f'> [!{callout_type}]')
                        if content_text:
                            converted_lines.append(f'> {content_text}')

                        # Continue with remaining blockquote lines
                        i += 1
                        while i < len(lines) and lines[i].strip().startswith('>'):
                            converted_lines.append(lines[i])
                            i += 1
                        i -= 1
                        matched = True
                        break

                if not matched:
                    converted_lines.append(line)
            else:
                converted_lines.append(line)

            i += 1

        return '\n'.join(converted_lines)

    def _convert_tables(self, content: str) -> str:
        """Ensure Notion tables are properly formatted for Obsidian."""
        lines = content.split('\n')
        converted_lines = []

        for i, line in enumerate(lines):
            # Detect table lines
            if '|' in line and line.strip().startswith('|'):
                # Ensure proper spacing around pipes
                cells = line.split('|')
                cells = [cell.strip() for cell in cells]
                line = '| ' + ' | '.join(cell for cell in cells if cell or cells.index(cell) == 0) + ' |'
                line = line.replace('|  |', '|')

            converted_lines.append(line)

        return '\n'.join(converted_lines)

    def _convert_links(self, content: str, source_file: Path) -> str:
        """Convert Notion internal links to Obsidian wikilinks."""
        # Notion exports links as [Page Name](Page%20Name%20uuid.md)

        def replace_link(match):
            link_text = match.group(1)
            link_url = match.group(2)

            # Check if it's an internal .md link
            if link_url.endswith('.md'):
                # URL decode
                link_url = html.unescape(link_url)
                link_url = link_url.replace('%20', ' ')

                # Find the corresponding file in mapping
                source_dir = source_file.parent
                full_link_path = (source_dir / link_url).resolve()

                # Get clean name
                clean_name = self._clean_notion_filename(Path(link_url).stem)

                # Convert to wikilink
                return f'[[{clean_name}]]'

            # External link, keep as is
            return match.group(0)

        # Match markdown links
        content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', replace_link, content)

        return content

    def _convert_images(self, content: str, source_file: Path) -> str:
        """Convert Notion image links to Obsidian format."""
        # Notion exports images with encoded URLs

        def replace_image(match):
            alt_text = match.group(1)
            image_url = match.group(2)

            # URL decode
            image_url = html.unescape(image_url)
            image_url = image_url.replace('%20', ' ')

            # If it's a local file, use just the filename
            if not image_url.startswith('http'):
                image_name = Path(image_url).name
                return f'![[{image_name}]]'

            # External image, keep markdown format
            return match.group(0)

        content = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', replace_image, content)

        return content

    def _convert_notion_toggles(self, content: str) -> str:
        """Convert Notion toggle blocks to Obsidian format."""
        # Notion toggle lists can be represented as collapsible sections
        # Using HTML details/summary tags which Obsidian supports

        lines = content.split('\n')
        converted_lines = []
        i = 0

        while i < len(lines):
            line = lines[i]

            # Detect toggle pattern (usually "▸ Title" or similar)
            if re.match(r'^\s*[▸▾►▼]\s+', line):
                # Extract title
                title = re.sub(r'^\s*[▸▾►▼]\s+', '', line)

                # Start collapsible section
                converted_lines.append(f'<details>')
                converted_lines.append(f'<summary>{title}</summary>')
                converted_lines.append('')

                # Collect indented content
                i += 1
                while i < len(lines) and (lines[i].startswith('\t') or lines[i].startswith('  ') or not lines[i].strip()):
                    content_line = lines[i].lstrip('\t').lstrip('  ')
                    if content_line.strip():
                        converted_lines.append(content_line)
                    elif lines[i].strip():
                        converted_lines.append(lines[i])
                    i += 1

                converted_lines.append('')
                converted_lines.append('</details>')
                converted_lines.append('')
                i -= 1
            else:
                converted_lines.append(line)

            i += 1

        return '\n'.join(converted_lines)

    def _convert_databases(self, content: str) -> str:
        """Convert Notion database views to Obsidian dataview format."""
        # This is a placeholder for database conversion
        # Notion databases are complex and may need custom handling
        # For now, we'll preserve them as tables
        return content

    def _decode_html_entities(self, content: str) -> str:
        """Decode HTML entities that Notion might use."""
        content = html.unescape(content)
        return content

    def _copy_assets(self):
        """Copy all asset files (images, PDFs, etc.) to output directory."""
        asset_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.pdf',
                          '.mp4', '.webm', '.mp3', '.wav', '.csv']

        # Create attachments folder in Obsidian vault
        attachments_dir = self.output_dir / 'attachments'
        attachments_dir.mkdir(exist_ok=True)

        for asset_file in self.input_dir.rglob('*'):
            if asset_file.is_file() and asset_file.suffix.lower() in asset_extensions:
                # Clean filename
                clean_name = self._clean_notion_filename(asset_file.stem)
                new_name = f"{clean_name}{asset_file.suffix}"

                # Copy to attachments folder
                dest_path = attachments_dir / new_name

                # Handle duplicate names
                counter = 1
                while dest_path.exists():
                    new_name = f"{clean_name}_{counter}{asset_file.suffix}"
                    dest_path = attachments_dir / new_name
                    counter += 1

                shutil.copy2(asset_file, dest_path)
                self.log(f"Copied asset: {asset_file.name} -> {new_name}")

    def _embed_all_database_queries(self):
        """
        Post-processing step: Find all pages that have matching database folders
        and append Dataview queries to display database items.

        Logic: If "Page Name.md" has a folder "Page Name/" containing *_Database folders,
        then append database queries to the end of Page Name.md
        """
        self.log("[INFO] Checking for pages with embedded databases...")

        # Scan all .md files in output directory
        for md_file in self.output_dir.rglob("*.md"):
            # Skip database index files
            if md_file.stem.endswith('_Index'):
                continue

            # Skip files inside _Database folders
            if any('_Database' in str(p) for p in md_file.parents):
                continue

            # Check if there's a matching folder
            page_stem = md_file.stem
            matching_folder = md_file.parent / page_stem

            if not matching_folder.exists() or not matching_folder.is_dir():
                continue

            # Check if this folder contains any database folders (ending with _Database)
            database_folders = [f for f in matching_folder.iterdir()
                              if f.is_dir() and f.name.endswith('_Database')]

            if not database_folders:
                continue

            # This page has embedded databases! Add Dataview queries at the end
            self.log(f"[DATABASE] Embedding queries for {len(database_folders)} database(s) in {md_file.name}")

            # Read current content
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check if already has database section (don't duplicate)
            if '## Databases' in content or '## databases' in content.lower():
                self.log(f"[SKIP] {md_file.name} already has database section")
                continue

            # Build the embedded section
            embedded_section = "\n\n---\n\n## Databases\n\n"
            embedded_section += "*This page contains the following databases:*\n\n"

            for db_folder in sorted(database_folders):
                # Get database name (remove _Database suffix)
                db_name = db_folder.name.replace('_Database', '')

                # Relative path from page to database folder
                relative_db_path = f"{page_stem}/{db_folder.name}"

                embedded_section += f"### {db_name}\n\n"
                embedded_section += f"```dataview\n"
                embedded_section += f"LIST\n"
                embedded_section += f'FROM "{relative_db_path}"\n'
                embedded_section += f'WHERE contains(tags, "database-item")\n'
                embedded_section += f"SORT file.name ASC\n"
                embedded_section += f"```\n\n"
                embedded_section += f"*[View full database]({relative_db_path}/{db_name}_Index.md)*\n\n"

            # Append to content and write back
            updated_content = content.rstrip() + embedded_section

            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(updated_content)

            self.log(f"[OK] Added database queries to {md_file.name}")

    def _convert_csv_databases(self):
        """Detect and convert Notion CSV databases to Obsidian Dataview format."""
        # Find all CSV files (Notion exports databases as CSV)
        csv_files = list(self.input_dir.rglob('*.csv'))

        for csv_file in csv_files:
            # Check if this is a database export
            # Notion database CSVs are usually in a folder with the database name
            # or have specific naming patterns like "Database Name.csv"

            # Determine database name and output location
            if csv_file.parent != self.input_dir:
                # CSV in subdirectory - use parent directory name
                db_name = self._clean_notion_filename(csv_file.parent.name)
                relative_path = csv_file.parent.relative_to(self.input_dir)
                db_output_dir = self.output_dir / relative_path / f'{db_name}_Database'
            else:
                # CSV in root - use CSV filename
                db_name = self._clean_notion_filename(csv_file.stem)
                db_output_dir = self.output_dir / f'{db_name}_Database'

            self.log(f"Converting database: {db_name}")

            try:
                result = self.db_converter.convert_database_folder(
                    csv_file,
                    db_output_dir
                )

                if 'error' not in result:
                    self.databases_converted.append({
                        'name': db_name,
                        'rows': result['rows_converted'],
                        'index': result['index_file']
                    })
                    self.log(f"[OK] Converted {result['rows_converted']} database rows")
                else:
                    self.log(f"[FAIL] Failed to convert database: {result['error']}")

            except Exception as e:
                self.log(f"[ERROR] Error converting database {db_name}: {e}")


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Convert Notion export to Obsidian format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python notion_to_obsidian.py ./NotionExport ./ObsidianVault
  python notion_to_obsidian.py ./NotionExport ./ObsidianVault --verbose
        """
    )

    parser.add_argument('input_dir', help='Path to Notion export directory')
    parser.add_argument('output_dir', help='Path to Obsidian vault directory')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Enable verbose logging')

    args = parser.parse_args()

    try:
        converter = NotionToObsidianConverter(
            args.input_dir,
            args.output_dir,
            verbose=args.verbose
        )
        converter.convert_all()
        print(f"\n[SUCCESS] Conversion successful!")
        print(f"Output saved to: {args.output_dir}")

    except Exception as e:
        print(f"\n[ERROR] Error during conversion: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == '__main__':
    exit(main())
