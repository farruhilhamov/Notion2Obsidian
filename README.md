# Notion to Obsidian Converter

A powerful automation script that converts exported Notion pages (with subpages) into beautifully formatted Obsidian pages. Includes comprehensive list handling, proper formatting conversion, and an intelligent linter to fix syntax mistakes.

## Features

- **Complete Notion Export Conversion**: Converts entire Notion exports including nested pages and subpages
- **List Formatting**: Properly converts all Notion list types (bullet lists, numbered lists, task lists) to Obsidian format
- **Database Support**: Handles Notion databases and tables
- **Asset Management**: Automatically copies and organizes images, PDFs, and other attachments
- **Link Conversion**: Converts Notion internal links to Obsidian wikilinks
- **Callout Conversion**: Transforms Notion callouts to Obsidian callout syntax
- **Toggle Support**: Converts Notion toggle blocks to collapsible HTML sections
- **Intelligent Linter**: Fixes syntax errors, formatting issues, and ensures Obsidian best practices
- **YAML Frontmatter**: Generates and standardizes frontmatter with metadata

## Installation

1. Clone or download this repository to your local machine

2. Ensure you have Python 3.7+ installed:
   ```bash
   python --version
   ```

3. (Optional) Install optional dependencies for enhanced features:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Conversion

Export your Notion page:
1. In Notion, click the `...` menu on any page
2. Select `Export`
3. Choose `Markdown & CSV` format
4. Enable `Include subpages`
5. Click `Export` and save the ZIP file
6. Extract the ZIP file to a folder

Run the converter:

```bash
python notion_to_obsidian.py <input_directory> <output_directory>
```

**Example:**
```bash
python notion_to_obsidian.py ./NotionExport ./MyObsidianVault
```

### Verbose Mode

For detailed logging during conversion:

```bash
python notion_to_obsidian.py ./NotionExport ./MyObsidianVault --verbose
```

### Standalone Linter

You can also use the linter independently on existing markdown files:

```bash
# Lint and fix a file
python obsidian_linter.py myfile.md

# Check if file needs linting (without modifying)
python obsidian_linter.py myfile.md --check

# Validate and report issues
python obsidian_linter.py myfile.md --validate
```

## What Gets Converted

### Headings
```markdown
# Notion: ##Heading (no space)
# Obsidian: ## Heading (properly formatted)
```

### Lists
**Bullet Lists:**
```markdown
# Notion:
- Item 1
  - Nested item
* Item 2

# Obsidian:
- Item 1
  - Nested item
- Item 2
```

**Numbered Lists:**
```markdown
# Notion:
1.Item one
2.Item two

# Obsidian:
1. Item one
2. Item two
```

**Task Lists:**
```markdown
# Notion:
- [ ]Unchecked task
- [x]Checked task

# Obsidian:
- [ ] Unchecked task
- [x] Checked task
```

### Tables
Notion tables are automatically formatted with proper spacing and alignment for Obsidian.

### Links
```markdown
# Notion: [Page Name](Page%20Name%20uuid123.md)
# Obsidian: [[Page Name]]
```

### Images
```markdown
# Notion: ![](image%20name%20uuid.png)
# Obsidian: ![[image name.png]]
```

### Callouts
```markdown
# Notion:
> 💡 This is a tip

# Obsidian:
> [!tip]
> This is a tip
```

Supported callout types:
- 💡 → `[!tip]`
- ⚠️ → `[!warning]`
- ❗ → `[!important]`
- ℹ️ → `[!info]`
- 📝 → `[!note]`
- ✅ → `[!success]`
- ❌ → `[!error]`

### Toggle Blocks
```markdown
# Notion:
▸ Toggle Title
  Hidden content

# Obsidian:
<details>
<summary>Toggle Title</summary>

Hidden content

</details>
```

### Code Blocks
Properly formatted code blocks with syntax highlighting preserved.

## Linting Rules

The built-in linter automatically applies these rules:

1. **Heading Formatting**: Ensures space after `#` symbols
2. **List Spacing**: Adds proper spacing after list markers (`-`, `*`, `1.`)
3. **Consistent Lists**: Standardizes all bullet lists to use `-`
4. **Table Formatting**: Properly aligns table columns with spacing
5. **Link Spacing**: Removes extra spaces in links and wikilinks
6. **Emphasis Formatting**: Fixes spacing around `**bold**` and `*italic*`
7. **Trailing Whitespace**: Removes trailing spaces from lines
8. **Multiple Blank Lines**: Limits consecutive blank lines to 2
9. **Final Newline**: Ensures files end with a newline
10. **YAML Frontmatter**: Standardizes frontmatter formatting

## File Organization

The converter maintains your Notion folder structure:

```
Output Directory/
├── Page 1.md
├── Page 2.md
├── Subfolder/
│   ├── Subpage 1.md
│   └── Subpage 2.md
└── attachments/
    ├── image1.png
    ├── image2.jpg
    └── document.pdf
```

All images and attachments are organized in an `attachments/` folder within your output directory.

## Frontmatter

The converter adds YAML frontmatter to each page:

```yaml
---
source: notion
created: 2025-12-12
---
```

You can extend this by modifying the `_convert_content` method in [notion_to_obsidian.py](notion_to_obsidian.py:79).

## Advanced Usage

### Custom Linter Configuration

You can customize linting rules by creating a custom linter instance:

```python
from obsidian_linter import ObsidianLinter

config = {
    'max_blank_lines': 3,
    'ensure_final_newline': True,
    'trim_trailing_whitespace': True,
    'space_after_list_marker': True,
    # ... more options
}

linter = ObsidianLinter(config=config)
linted_content = linter.lint(your_content)
```

### Extending the Converter

To add custom conversion rules, extend the `NotionToObsidianConverter` class:

```python
from notion_to_obsidian import NotionToObsidianConverter

class CustomConverter(NotionToObsidianConverter):
    def _convert_content(self, content, source_file):
        content = super()._convert_content(content, source_file)
        # Add your custom conversions here
        return content
```

## Troubleshooting

### Issue: Links not converting properly
**Solution**: Ensure your Notion export was done with "Include subpages" enabled and in "Markdown & CSV" format.

### Issue: Images not showing
**Solution**: Check that the images were exported in the same directory structure. The converter copies them to `attachments/` folder.

### Issue: Special characters in filenames
**Solution**: The converter automatically sanitizes filenames, but if you encounter issues, check the `sanitize_filename()` function in [utils.py](utils.py:14).

### Issue: Tables not formatting correctly
**Solution**: Ensure your Notion tables have proper headers. The converter expects standard markdown table format.

## Supported Notion Features

✅ Headings (H1-H6)
✅ Bullet lists
✅ Numbered lists
✅ Task lists (checkboxes)
✅ Tables
✅ Code blocks
✅ Inline code
✅ Bold, italic, strikethrough
✅ Links (internal and external)
✅ Images
✅ Files/attachments
✅ Callouts/alerts
✅ Toggle blocks
✅ Blockquotes
✅ Horizontal rules
✅ Nested pages

⚠️ Partial Support:
- Databases (converted as tables)
- Formulas (basic conversion)
- Embeds (preserved as links)

❌ Not Supported:
- Live database views
- Notion-specific blocks (board, gallery, timeline views)
- Synced blocks
- Comments

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

This project is open source and available under the MIT License.

## Credits

Created for converting Notion exports to Obsidian format with proper list handling and syntax correction.

## Examples

### Example 1: Basic Page Conversion

**Input (Notion):**
```markdown
# My Page

This is a paragraph with a [link](Another%20Page%20abc123.md).

-Item 1
-Item 2
  -Nested item

##Subheading
```

**Output (Obsidian):**
```markdown
---
source: notion
created: 2025-12-12
---

# My Page

This is a paragraph with a [[Another Page]].

- Item 1
- Item 2
  - Nested item

## Subheading
```

### Example 2: Complex List with Tasks

**Input (Notion):**
```markdown
-[ ]Task one
-[x]Task two
1.First item
2.Second item
```

**Output (Obsidian):**
```markdown
- [ ] Task one
- [x] Task two

1. First item
2. Second item
```

### Example 3: Callout Conversion

**Input (Notion):**
```markdown
> 💡 Remember to save your work regularly!
> This is important for data safety.
```

**Output (Obsidian):**
```markdown
> [!tip]
> Remember to save your work regularly!
> This is important for data safety.
```

## FAQ

**Q: Can I run this on multiple Notion exports?**
A: Yes, you can run the converter multiple times with different input/output directories.

**Q: Will this modify my original Notion export?**
A: No, the converter only reads from the input directory and writes to the output directory. Your original files remain untouched.

**Q: Can I customize which files get converted?**
A: Currently, all `.md` files in the input directory are converted. You can modify the `convert_all()` method to add filtering logic.

**Q: Does this work on Windows/Mac/Linux?**
A: Yes, the script is cross-platform and works on all major operating systems.

**Q: What Python version do I need?**
A: Python 3.7 or higher is required.

## Support

For issues, questions, or suggestions, please open an issue on the repository.

---

Happy note-taking! 📝
