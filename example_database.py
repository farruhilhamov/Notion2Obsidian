#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example demonstrating Notion database (Base) conversion to Obsidian Dataview.
This shows how to convert Notion tables/databases into manageable Obsidian databases.
"""

import sys
import io
from pathlib import Path
from notion_database import NotionDatabaseConverter
import csv

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def create_sample_csv():
    """Create a sample CSV database file (like Notion exports)."""
    sample_dir = Path('./example_database_data')
    sample_dir.mkdir(exist_ok=True)

    csv_file = sample_dir / 'Tasks.csv'

    # Create sample data (Notion-style headers with types)
    headers = [
        'Name',
        'Status (Select)',
        'Priority (Select)',
        'Due Date (Date)',
        'Completed (Checkbox)',
        'Tags (Multi-select)',
        'Assigned To (Text)',
        'Notes (Text)'
    ]

    rows = [
        ['Finish project proposal', 'In Progress', 'High', '2025-12-20', 'No', 'work, urgent', 'Alice', 'Need to review with team'],
        ['Review code changes', 'Not Started', 'Medium', '2025-12-22', 'No', 'development, review', 'Bob', 'PR #123'],
        ['Update documentation', 'Done', 'Low', '2025-12-15', 'Yes', 'documentation', 'Charlie', 'Added API examples'],
        ['Fix login bug', 'In Progress', 'High', '2025-12-18', 'No', 'bug, urgent', 'Alice', 'Issue #456'],
        ['Team meeting prep', 'Not Started', 'Medium', '2025-12-25', 'No', 'meeting', 'Bob', 'Prepare slides'],
        ['Database migration', 'Done', 'High', '2025-12-10', 'Yes', 'development, database', 'Charlie', 'Successfully migrated'],
    ]

    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    return csv_file


def example_convert_database():
    """Example: Convert a Notion database to Obsidian Dataview format."""
    print("=" * 60)
    print("Example: Convert Notion Database to Obsidian Dataview")
    print("=" * 60)
    print()

    # Create sample CSV database
    print("Step 1: Creating sample database CSV...")
    csv_file = create_sample_csv()
    print(f"✓ Created: {csv_file}")
    print()

    # Convert database
    print("Step 2: Converting to Obsidian Dataview format...")
    converter = NotionDatabaseConverter()
    output_dir = Path('./example_database_output')

    result = converter.convert_database_folder(csv_file, output_dir)

    if 'error' in result:
        print(f"✗ Error: {result['error']}")
        return

    print(f"✓ Converted {result['rows_converted']} database rows")
    print(f"✓ Created {len(result['files_created'])} note files")
    print()

    # Show results
    print("Step 3: Files created:")
    print("-" * 40)
    for file in result['files_created'][:3]:  # Show first 3
        print(f"  📄 {Path(file).name}")
    if len(result['files_created']) > 3:
        print(f"  ... and {len(result['files_created']) - 3} more")
    print(f"  📑 {Path(result['index_file']).name}")
    print()

    # Show sample content
    print("Step 4: Sample file content:")
    print("-" * 40)
    sample_file = Path(result['files_created'][0])
    with open(sample_file, 'r', encoding='utf-8') as f:
        content = f.read()
    print(content[:500] + '...')
    print("-" * 40)
    print()

    # Show index file
    print("Step 5: Index file with Dataview queries:")
    print("-" * 40)
    index_file = Path(result['index_file'])
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()
    # Show first 600 characters
    print(content[:600] + '...')
    print("-" * 40)
    print()

    print("✅ Database conversion complete!")
    print()
    print(f"📁 Output directory: {output_dir}")
    print(f"📑 Open in Obsidian: {index_file}")
    print()
    print("Next steps:")
    print("  1. Install Dataview plugin in Obsidian")
    print("  2. Copy the output folder to your Obsidian vault")
    print("  3. Open the index file to see interactive queries")
    print()


def example_inline_table():
    """Example: Create inline database table."""
    print("=" * 60)
    print("Example: Inline Database Table")
    print("=" * 60)
    print()

    # Create sample data
    csv_file = create_sample_csv()

    converter = NotionDatabaseConverter()
    rows, headers = converter._parse_database_csv(csv_file)

    # Create inline table
    table = converter.create_inline_database(rows, headers)

    print("Generated Markdown Table:")
    print("-" * 40)
    print(table)
    print("-" * 40)
    print()
    print("This table can be embedded directly in markdown files!")
    print()


def example_property_types():
    """Example: Show how different property types are converted."""
    print("=" * 60)
    print("Example: Property Type Conversions")
    print("=" * 60)
    print()

    conversions = [
        ('Text', 'Task Name', 'name: Finish project'),
        ('Number', 'Priority: 5', 'priority: 5'),
        ('Checkbox', 'Completed: Yes', 'completed: true'),
        ('Date', 'Due: 2025-12-20', 'due_date: 2025-12-20'),
        ('Select', 'Status: Done', 'status: Done'),
        ('Multi-select', 'Tags: work, urgent', 'tags:\n  - work\n  - urgent'),
    ]

    print("Notion Property → Obsidian Frontmatter")
    print("-" * 40)
    for notion_type, notion_example, obsidian_output in conversions:
        print(f"\n{notion_type}:")
        print(f"  Notion:    {notion_example}")
        print(f"  Obsidian:  {obsidian_output}")
    print()


def example_dataview_queries():
    """Example: Show Dataview query examples."""
    print("=" * 60)
    print("Example: Dataview Query Templates")
    print("=" * 60)
    print()

    queries = {
        'Table View': '''```dataview
TABLE status, priority, due_date
FROM "Tasks_Database"
WHERE contains(tags, "database-item")
SORT due_date ASC
```''',

        'Filtered by Status': '''```dataview
TABLE priority, due_date
FROM "Tasks_Database"
WHERE status = "In Progress"
```''',

        'Incomplete Tasks': '''```dataview
LIST
FROM "Tasks_Database"
WHERE completed = false
SORT priority DESC
```''',

        'Grouped by Priority': '''```dataview
TABLE rows.file.link as "Tasks"
FROM "Tasks_Database"
GROUP BY priority
```''',

        'Count by Status': '''```dataview
TABLE length(rows) as "Count"
FROM "Tasks_Database"
GROUP BY status
```'''
    }

    for name, query in queries.items():
        print(f"\n{name}:")
        print("-" * 40)
        print(query)

    print("\n" + "=" * 60)
    print("These queries work in Obsidian with Dataview plugin!")
    print()


def example_workflow():
    """Example: Show complete workflow from Notion to Obsidian."""
    print("=" * 60)
    print("Example: Complete Notion Database Workflow")
    print("=" * 60)
    print()

    workflow_steps = [
        ("1. Export from Notion", [
            "Open your database in Notion",
            "Click ... → Export",
            "Choose 'Markdown & CSV'",
            "Download and extract ZIP"
        ]),
        ("2. Convert to Obsidian", [
            "Run: python notion_to_obsidian.py NotionExport ObsidianVault",
            "Databases are auto-detected and converted",
            "Each row becomes a separate note file",
            "Index file with queries is created"
        ]),
        ("3. Setup Obsidian", [
            "Install Dataview plugin",
            "Enable in Community Plugins",
            "Open your vault",
            "Navigate to database folder"
        ]),
        ("4. Use Your Database", [
            "Open the _Index.md file",
            "See live table/list views",
            "Click on items to edit",
            "Modify frontmatter to update data",
            "Create custom queries"
        ]),
        ("5. Manage & Extend", [
            "Add new items (create .md files)",
            "Edit properties in frontmatter",
            "Create custom view files",
            "Use JavaScript for advanced queries"
        ])
    ]

    for step, actions in workflow_steps:
        print(f"\n{step}")
        print("-" * 40)
        for action in actions:
            print(f"  • {action}")

    print("\n" + "=" * 60)
    print()


def main():
    """Run all database examples."""
    print("\n")
    print("=" * 60)
    print("     Notion Database Conversion Examples")
    print("=" * 60)
    print("\n")

    try:
        example_property_types()
        print("\n")

        example_dataview_queries()
        print("\n")

        example_workflow()
        print("\n")

        example_inline_table()
        print("\n")

        example_convert_database()

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 60)
    print("All database examples completed!")
    print("=" * 60)
    print("\nFor more information:")
    print("  • Read: DATABASE_GUIDE.md")
    print("  • Full docs: README.md")
    print("  • Quick start: QUICKSTART.md")
    print("\n")


if __name__ == '__main__':
    main()
