#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example usage script for Notion to Obsidian converter.
This demonstrates various ways to use the converter programmatically.
"""

import sys
import io
from pathlib import Path
from notion_to_obsidian import NotionToObsidianConverter
from obsidian_linter import ObsidianLinter

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def example_basic_conversion():
    """Basic conversion example."""
    print("=" * 60)
    print("Example 1: Basic Conversion")
    print("=" * 60)

    # Define paths
    input_dir = "./NotionExport"  # Replace with your Notion export path
    output_dir = "./ObsidianVault"  # Replace with your desired output path

    # Create converter instance
    converter = NotionToObsidianConverter(
        input_dir=input_dir,
        output_dir=output_dir,
        verbose=True
    )

    # Run conversion
    try:
        converter.convert_all()
        print("\nConversion completed successfully!")
    except FileNotFoundError:
        print(f"\nError: Input directory not found: {input_dir}")
        print("Please update the path in this example script.")
    except Exception as e:
        print(f"\nError during conversion: {e}")


def example_lint_single_file():
    """Example of linting a single file."""
    print("\n" + "=" * 60)
    print("Example 2: Lint Single File")
    print("=" * 60)

    # Example content with formatting issues
    content = """# MyPage
This is a paragraph.

-Item 1
-Item 2
  -Nested item

##Subheading

This has  multiple  spaces.

| Column 1|Column 2 |
|---|---|
|Data1|Data2|


"""

    print("\nOriginal content:")
    print("-" * 40)
    print(content)
    print("-" * 40)

    # Create linter and lint content
    linter = ObsidianLinter()
    linted = linter.lint(content)

    print("\nLinted content:")
    print("-" * 40)
    print(linted)
    print("-" * 40)


def example_custom_linter_config():
    """Example of using custom linter configuration."""
    print("\n" + "=" * 60)
    print("Example 3: Custom Linter Configuration")
    print("=" * 60)

    # Custom linter configuration
    custom_config = {
        'max_blank_lines': 1,  # Allow only 1 blank line
        'ensure_final_newline': True,
        'trim_trailing_whitespace': True,
        'space_after_list_marker': True,
        'space_after_heading': True,
        'consistent_list_style': True,
    }

    content = """# Heading


Too many blank lines above.

- Item 1
- Item 2
"""

    print("\nOriginal content (3 blank lines):")
    print("-" * 40)
    print(repr(content))
    print("-" * 40)

    linter = ObsidianLinter(config=custom_config)
    linted = linter.lint(content)

    print("\nLinted content (max 1 blank line):")
    print("-" * 40)
    print(repr(linted))
    print("-" * 40)


def example_validate_file():
    """Example of validating a file for issues."""
    print("\n" + "=" * 60)
    print("Example 4: Validate File")
    print("=" * 60)

    content = """#Heading without space
This is text.

-List without space
- Correct list item
1.Numbered without space
"""

    print("\nValidating content...")

    linter = ObsidianLinter()
    issues = linter.validate(content)

    if issues:
        print(f"\nFound {len(issues)} issues:")
        for line_num, issue in issues:
            print(f"  Line {line_num}: {issue}")
    else:
        print("\nNo issues found!")


def example_batch_conversion():
    """Example of converting with custom processing."""
    print("\n" + "=" * 60)
    print("Example 5: Batch Conversion with Custom Processing")
    print("=" * 60)

    class CustomConverter(NotionToObsidianConverter):
        """Custom converter with additional processing."""

        def _convert_content(self, content, source_file):
            # Call parent conversion
            content = super()._convert_content(content, source_file)

            # Add custom tag to all converted files
            if content.startswith('---'):
                # Insert tag in frontmatter
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if line.strip() == '---' and i > 0:
                        lines.insert(i, 'tags: [converted-from-notion]')
                        break
                content = '\n'.join(lines)

            return content

    print("\nCustom converter class created.")
    print("This adds 'tags: [converted-from-notion]' to all files.")
    print("\nTo use:")
    print("  converter = CustomConverter('input', 'output', verbose=True)")
    print("  converter.convert_all()")


def example_convert_notion_features():
    """Example showing various Notion feature conversions."""
    print("\n" + "=" * 60)
    print("Example 6: Notion Feature Conversions")
    print("=" * 60)

    from notion_to_obsidian import NotionToObsidianConverter

    converter = NotionToObsidianConverter('.', '.', verbose=False)

    examples = {
        'Heading': {
            'before': '##Heading',
            'after': converter._convert_headings('##Heading')
        },
        'List': {
            'before': '-Item 1\n-Item 2',
            'after': converter._convert_lists('-Item 1\n-Item 2')
        },
        'Checkbox': {
            'before': '- [ ]Task\n- [x]Done',
            'after': converter._convert_checkboxes('- [ ]Task\n- [x]Done')
        },
        'Callout': {
            'before': '> 💡 This is a tip',
            'after': converter._convert_callouts('> 💡 This is a tip')
        },
    }

    for name, example in examples.items():
        print(f"\n{name} Conversion:")
        print(f"  Before: {repr(example['before'])}")
        print(f"  After:  {repr(example['after'])}")


def main():
    """Run all examples."""
    print("\n")
    print("=" * 60)
    print(" " * 10 + "Notion to Obsidian Converter Examples")
    print("=" * 60)
    print("\n")

    # Run examples
    try:
        example_lint_single_file()
        example_custom_linter_config()
        example_validate_file()
        example_batch_conversion()
        example_convert_notion_features()

        print("\n" + "=" * 60)
        print("Note: Basic conversion example requires actual files.")
        print("Update the paths in example_basic_conversion() and uncomment below:")
        print("=" * 60)
        # Uncomment when you have actual Notion export to test:
        # example_basic_conversion()

    except Exception as e:
        print(f"\nError running examples: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)
    print("\nFor actual conversion, use:")
    print("  python notion_to_obsidian.py <input_dir> <output_dir>")
    print("\n")


if __name__ == '__main__':
    main()
