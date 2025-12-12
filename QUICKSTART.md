# Quick Start Guide

Get started with the Notion to Obsidian Converter in 3 easy steps!

## Step 1: Export from Notion

1. Open the page you want to export in Notion
2. Click the `...` (three dots) menu in the top right
3. Select `Export`
4. Choose settings:
   - Format: **Markdown & CSV**
   - Check: **Include subpages**
   - Uncheck: Create folders for subpages (optional)
5. Click `Export` button
6. Save and extract the ZIP file

## Step 2: Run the Converter

### Option A: Using the Batch Script (Windows)

Double-click `convert.bat` or run in Command Prompt:

```cmd
convert.bat "C:\path\to\NotionExport" "C:\path\to\ObsidianVault"
```

### Option B: Using the Shell Script (Mac/Linux)

First, make it executable:

```bash
chmod +x convert.sh
```

Then run:

```bash
./convert.sh /path/to/NotionExport /path/to/ObsidianVault
```

### Option C: Using Python Directly

```bash
python notion_to_obsidian.py ./NotionExport ./ObsidianVault --verbose
```

## Step 3: Open in Obsidian

1. Open Obsidian
2. Click "Open folder as vault"
3. Select your output directory
4. Start using your converted notes!

## What Gets Fixed Automatically

The converter will automatically:

- ✅ Convert Notion links to Obsidian wikilinks
- ✅ Fix list formatting (bullets, numbers, tasks)
- ✅ Add proper spacing after headings
- ✅ Format tables properly
- ✅ Convert callouts to Obsidian syntax
- ✅ Organize images in attachments folder
- ✅ Remove Notion UUIDs from filenames
- ✅ Fix syntax errors
- ✅ Add YAML frontmatter

## Common Issues

**Problem**: "Python not found"
**Solution**: Install Python 3.7+ from [python.org](https://www.python.org/)

**Problem**: "Input directory not found"
**Solution**: Make sure you extracted the Notion ZIP export first

**Problem**: "Permission denied"
**Solution**:
- Windows: Run Command Prompt as Administrator
- Mac/Linux: Run `chmod +x convert.sh` first

**Problem**: Images not showing
**Solution**: In Obsidian settings, set "Attachment folder path" to `attachments`

## Need More Help?

See the full [README.md](README.md) for:
- Detailed feature list
- Advanced usage examples
- Customization options
- Troubleshooting guide

## Example Workflow

```
1. Export from Notion → NotionExport.zip
2. Extract → NotionExport/
3. Run converter → python notion_to_obsidian.py NotionExport MyVault
4. Open MyVault in Obsidian
5. Enjoy! 🎉
```

## Tips

💡 **Tip 1**: Always keep a backup of your Notion export before converting

💡 **Tip 2**: Use `--verbose` flag to see detailed conversion progress

💡 **Tip 3**: Run the linter on existing Obsidian files: `python obsidian_linter.py myfile.md`

💡 **Tip 4**: Test with a small export first to ensure everything works correctly

💡 **Tip 5**: Check the `attachments/` folder for all your images and files

---

Happy converting! 📝✨
