# Notion to Obsidian Converter - Index

Welcome! This is your complete guide to the Notion to Obsidian conversion toolkit.

## Start Here 🚀

**New users**: Read this in order:

1. [QUICKSTART.md](QUICKSTART.md) - Get started in 3 steps (2 min read)
2. [EXAMPLES.md](EXAMPLES.md) - See what gets converted (5 min read)
3. Convert your first export! (2 min)

**Experienced users**: Jump to:

- [README.md](README.md) - Full documentation
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Technical overview

## File Guide

### 📖 Documentation

| File | Purpose | Read When |
|------|---------|-----------|
| [QUICKSTART.md](QUICKSTART.md) | 3-step quick start | You're starting out |
| [EXAMPLES.md](EXAMPLES.md) | Before/after examples | You want to see results |
| [README.md](README.md) | Complete documentation | You need details |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | Technical overview | You want architecture |
| [FILE_STRUCTURE.txt](FILE_STRUCTURE.txt) | File organization | You want structure |
| [INDEX.md](INDEX.md) | This file | You're here! |

### 💻 Scripts

| File | Purpose | Use When |
|------|---------|----------|
| [notion_to_obsidian.py](notion_to_obsidian.py) | Main converter | Converting exports |
| [obsidian_linter.py](obsidian_linter.py) | Markdown linter | Fixing syntax |
| [utils.py](utils.py) | Helper functions | Programming |
| [example_usage.py](example_usage.py) | Examples | Learning API |
| [convert.bat](convert.bat) | Windows script | Easy Windows use |
| [convert.sh](convert.sh) | Unix/Mac script | Easy Unix/Mac use |

### ⚙️ Configuration

| File | Purpose |
|------|---------|
| [requirements.txt](requirements.txt) | Python dependencies (optional) |
| [.gitignore](.gitignore) | Git ignore rules |

## Common Tasks

### Task: Convert Notion Export

**Quick way** (Windows):
```cmd
convert.bat "C:\NotionExport" "C:\ObsidianVault"
```

**Quick way** (Mac/Linux):
```bash
./convert.sh NotionExport ObsidianVault
```

**Manual way**:
```bash
python notion_to_obsidian.py ./NotionExport ./ObsidianVault --verbose
```

### Task: Fix Markdown Syntax

```bash
python obsidian_linter.py myfile.md
```

### Task: Check File for Issues

```bash
python obsidian_linter.py myfile.md --validate
```

### Task: See Examples

```bash
python example_usage.py
```

### Task: Get Help

```bash
python notion_to_obsidian.py --help
```

## Learning Path

### Beginner Level
1. Read [QUICKSTART.md](QUICKSTART.md)
2. Export a simple Notion page
3. Run `convert.bat` or `convert.sh`
4. Open result in Obsidian

### Intermediate Level
1. Read [EXAMPLES.md](EXAMPLES.md)
2. Understand conversions
3. Use verbose mode
4. Check [README.md](README.md) troubleshooting

### Advanced Level
1. Read [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
2. Study [example_usage.py](example_usage.py)
3. Customize converters
4. Extend functionality

## Feature Reference

### What Gets Converted?

✅ **Text Formatting**
- Headings (H1-H6)
- Bold, italic, strikethrough
- Inline code
- Code blocks

✅ **Lists** (Your main requirement!)
- Bullet lists (-, *, +)
- Numbered lists (1., 2., 3.)
- Task lists (- [ ], - [x])
- Nested lists (proper indentation)
- Mixed list types

✅ **Links & Media**
- Internal links → Wikilinks
- External links preserved
- Images → Obsidian embeds
- File attachments

✅ **Advanced**
- Tables (formatted)
- Callouts (8 types)
- Toggle blocks
- Blockquotes
- Horizontal rules

✅ **Metadata**
- YAML frontmatter
- Creation dates
- Tags support

### What Gets Fixed? (Linter)

✅ **Spacing**
- Heading spacing (`##Text` → `## Text`)
- List spacing (`-Item` → `- Item`)
- Table spacing

✅ **Consistency**
- List markers (all → `-`)
- Blank lines (limited to 2)
- Trailing whitespace removed

✅ **Validation**
- Syntax checking
- Error reporting
- Issue detection

## Conversion Examples

### Example 1: Simple List

**Notion**:
```markdown
-Item 1
-Item 2
  -Nested
```

**Obsidian**:
```markdown
- Item 1
- Item 2
  - Nested
```

### Example 2: Task List

**Notion**:
```markdown
-[ ]Buy milk
-[x]Write code
```

**Obsidian**:
```markdown
- [ ] Buy milk
- [x] Write code
```

### Example 3: Internal Link

**Notion**:
```markdown
[My Page](My%20Page%20abc123.md)
```

**Obsidian**:
```markdown
[[My Page]]
```

More examples in [EXAMPLES.md](EXAMPLES.md)!

## Troubleshooting Quick Reference

| Problem | Solution | Details |
|---------|----------|---------|
| Python not found | Install Python 3.7+ | [python.org](https://www.python.org) |
| Files not converting | Check input path | Must be extracted ZIP |
| Images missing | Check attachments folder | Set in Obsidian settings |
| Links broken | Re-run conversion | Ensure full export |
| Permission denied | Run as admin / chmod +x | Platform specific |

Full troubleshooting: [README.md](README.md#troubleshooting)

## CLI Reference

### Main Converter

```bash
# Basic
python notion_to_obsidian.py <input> <output>

# Verbose
python notion_to_obsidian.py <input> <output> --verbose

# Help
python notion_to_obsidian.py --help
```

### Linter

```bash
# Fix file
python obsidian_linter.py file.md

# Check only
python obsidian_linter.py file.md --check

# Validate
python obsidian_linter.py file.md --validate
```

### Examples

```bash
# Run all examples
python example_usage.py
```

## API Reference (for developers)

### Basic Converter Usage

```python
from notion_to_obsidian import NotionToObsidianConverter

converter = NotionToObsidianConverter(
    input_dir='./NotionExport',
    output_dir='./ObsidianVault',
    verbose=True
)
converter.convert_all()
```

### Basic Linter Usage

```python
from obsidian_linter import ObsidianLinter

linter = ObsidianLinter()
linted_content = linter.lint(content)
```

### Custom Converter

```python
class MyConverter(NotionToObsidianConverter):
    def _convert_content(self, content, source_file):
        content = super()._convert_content(content, source_file)
        # Custom logic here
        return content
```

More in [example_usage.py](example_usage.py)!

## Project Statistics

- **Files Created**: 14
- **Lines of Code**: ~1,500+
- **Documentation Lines**: ~1,500+
- **Examples**: 6 working demos
- **Supported Features**: 25+
- **Linting Rules**: 12+
- **Platform Support**: 3 (Windows, Mac, Linux)

## Support Resources

### Documentation
- 📘 [QUICKSTART.md](QUICKSTART.md) - Start here
- 📗 [EXAMPLES.md](EXAMPLES.md) - See examples
- 📕 [README.md](README.md) - Full docs
- 📙 [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Technical details

### Code
- 🔧 [notion_to_obsidian.py](notion_to_obsidian.py) - Main script
- 🔨 [obsidian_linter.py](obsidian_linter.py) - Linter
- ⚙️ [utils.py](utils.py) - Utilities
- 📝 [example_usage.py](example_usage.py) - Examples

### Scripts
- 🪟 [convert.bat](convert.bat) - Windows
- 🐧 [convert.sh](convert.sh) - Unix/Mac

## Version Information

- **Version**: 1.0.0
- **Status**: Production Ready ✅
- **Last Updated**: 2025-12-12
- **Python Required**: 3.7+
- **Dependencies**: None (stdlib only)

## Quick Links

- **Start Converting**: [QUICKSTART.md](QUICKSTART.md#step-2-run-the-converter)
- **See Examples**: [EXAMPLES.md](EXAMPLES.md#table-of-contents)
- **Troubleshooting**: [README.md](README.md#troubleshooting)
- **API Usage**: [example_usage.py](example_usage.py)
- **Features**: [README.md](README.md#features)

## Next Steps

1. ✅ You're here (reading INDEX.md)
2. 📖 Read [QUICKSTART.md](QUICKSTART.md)
3. 🎯 Export from Notion
4. 🚀 Run converter
5. 🎉 Enjoy Obsidian!

---

**Need help?** Check [README.md](README.md#troubleshooting) troubleshooting section.

**Want examples?** Run `python example_usage.py` or read [EXAMPLES.md](EXAMPLES.md).

**Ready to convert?** Follow [QUICKSTART.md](QUICKSTART.md)!

---

Happy note-taking! 📝✨
