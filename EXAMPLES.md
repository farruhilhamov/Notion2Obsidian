# Conversion Examples

This document shows real examples of how Notion content is converted to Obsidian format.

## Table of Contents

- [Headings](#headings)
- [Lists](#lists)
- [Task Lists](#task-lists)
- [Links](#links)
- [Images](#images)
- [Tables](#tables)
- [Callouts](#callouts)
- [Code Blocks](#code-blocks)
- [Toggle Blocks](#toggle-blocks)
- [Emphasis](#emphasis)

---

## Headings

### Before (Notion)

```markdown
#Heading 1
##Heading 2
###Heading 3
```

### After (Obsidian)

```markdown
# Heading 1
## Heading 2
### Heading 3
```

**What changed**: Added space after `#` symbols

---

## Lists

### Before (Notion)

```markdown
-Item 1
-Item 2
  -Nested item A
  -Nested item B
*Another item
+Yet another

1.First
2.Second
  1.Nested numbered
```

### After (Obsidian)

```markdown
- Item 1
- Item 2
  - Nested item A
  - Nested item B
- Another item
- Yet another

1. First
2. Second
  1. Nested numbered
```

**What changed**:
- Added space after `-`, `*`, `+`
- Converted all bullets to `-` for consistency
- Fixed numbered list spacing

---

## Task Lists

### Before (Notion)

```markdown
-[ ]Incomplete task
-[x]Completed task
-[ ]Another task with-[ ]nested task
```

### After (Obsidian)

```markdown
- [ ] Incomplete task
- [x] Completed task
- [ ] Another task with
  - [ ] nested task
```

**What changed**: Proper spacing around checkbox syntax

---

## Links

### Before (Notion)

```markdown
[My Page](My%20Page%20a1b2c3d4.md)
[External Link](https://example.com)
[Another Page](../folder/Another%20Page%20e5f6g7h8.md)
```

### After (Obsidian)

```markdown
[[My Page]]
[External Link](https://example.com)
[[Another Page]]
```

**What changed**:
- Internal `.md` links converted to wikilinks
- URL decoding applied
- Notion UUIDs removed
- External links preserved

---

## Images

### Before (Notion)

```markdown
![](image%20name%20abc123.png)
![My Image](path/to/image%20def456.jpg)
![External](https://example.com/image.png)
```

### After (Obsidian)

```markdown
![[image name.png]]
![[image.jpg]]
![External](https://example.com/image.png)
```

**What changed**:
- Local images converted to Obsidian embed syntax
- URL decoding applied
- External images preserved as markdown
- Images copied to `attachments/` folder

---

## Tables

### Before (Notion)

```markdown
|Column 1|Column 2|Column 3|
|---|---|---|
|Data 1|Data 2|Data 3|
|More data|Even more|Last|
```

### After (Obsidian)

```markdown
| Column 1  | Column 2  | Column 3 |
| --------- | --------- | -------- |
| Data 1    | Data 2    | Data 3   |
| More data | Even more | Last     |
```

**What changed**: Added proper spacing and alignment

---

## Callouts

### Before (Notion)

```markdown
> 💡 This is a helpful tip
> You should remember this!

> ⚠️ Warning: Be careful here

> ❗ This is important information

> 📝 Note to self
```

### After (Obsidian)

```markdown
> [!tip]
> This is a helpful tip
> You should remember this!

> [!warning]
> Warning: Be careful here

> [!important]
> This is important information

> [!note]
> Note to self
```

**What changed**: Converted emoji-based callouts to Obsidian callout syntax

### Supported Callout Types

| Emoji | Obsidian Type | Usage |
|-------|---------------|-------|
| 💡 | `[!tip]` | Tips and helpful hints |
| ⚠️ | `[!warning]` | Warnings and cautions |
| ❗ | `[!important]` | Important information |
| ℹ️ | `[!info]` | General information |
| 📝 | `[!note]` | Notes and reminders |
| ✅ | `[!success]` | Success messages |
| ❌ | `[!error]` | Errors and failures |
| 🔥 | `[!danger]` | Dangerous actions |

---

## Code Blocks

### Before (Notion)

```markdown
```python
def hello():
    print("Hello World")
```
```

### After (Obsidian)

```markdown
```python
def hello():
    print("Hello World")
```
```

**What changed**: Ensured proper spacing around code blocks

---

## Toggle Blocks

### Before (Notion)

```markdown
▸ Click to expand
  Hidden content here
  More hidden content
```

### After (Obsidian)

```markdown
<details>
<summary>Click to expand</summary>

Hidden content here
More hidden content

</details>
```

**What changed**: Converted to HTML details/summary tags (Obsidian compatible)

---

## Emphasis

### Before (Notion)

```markdown
**Bold text**
*Italic text*
***Bold and italic***
~~Strikethrough~~
`Inline code`
```

### After (Obsidian)

```markdown
**Bold text**
*Italic text*
***Bold and italic***
~~Strikethrough~~
`Inline code`
```

**What changed**: Cleaned up spacing around emphasis markers

---

## Complex Example

### Before (Notion)

```markdown
#Project Planning

##Goals
-[ ]Complete project setup
-[ ]Design architecture
-[x]Initial research

##Resources
Check out [Documentation](Documentation%20xyz123.md) for more info.

> 💡 Remember to update the timeline!

###Technical Details
```python
def setup_project():
    print("Setting up...")
```

|Task|Status|Owner|
|---|---|---|
|Design|In Progress|Alice|
|Development|Not Started|Bob|
```

### After (Obsidian)

```markdown
---
source: notion
created: 2025-12-12
---

# Project Planning

## Goals

- [ ] Complete project setup
- [ ] Design architecture
- [x] Initial research

## Resources

Check out [[Documentation]] for more info.

> [!tip]
> Remember to update the timeline!

### Technical Details

```python
def setup_project():
    print("Setting up...")
```

| Task        | Status       | Owner |
| ----------- | ------------ | ----- |
| Design      | In Progress  | Alice |
| Development | Not Started  | Bob   |
```

**What changed**:
- Added YAML frontmatter
- Fixed heading spacing
- Fixed list formatting
- Converted internal link to wikilink
- Converted callout syntax
- Added proper table formatting
- Ensured code block spacing

---

## Before and After Summary

### Common Fixes Applied

1. ✅ Heading spacing (`##Text` → `## Text`)
2. ✅ List markers (`-Item` → `- Item`)
3. ✅ Checkbox spacing (`-[ ]Task` → `- [ ] Task`)
4. ✅ Internal links (`[Page](Page%20uuid.md)` → `[[Page]]`)
5. ✅ Image embeds (`![](image.png)` → `![[image.png]]`)
6. ✅ Table formatting (proper spacing and alignment)
7. ✅ Callouts (emoji → Obsidian syntax)
8. ✅ Frontmatter (added metadata)
9. ✅ Trailing whitespace (removed)
10. ✅ Multiple blank lines (limited to 2)

### File Organization

**Before**:
```
NotionExport/
├── My Page 8a7b3c4d.md
├── Another Page 1e2f3g4h.md
├── image 5i6j7k8l.png
└── Subfolder 9m0n1o2p/
    └── Subpage 3q4r5s6t.md
```

**After**:
```
ObsidianVault/
├── My Page.md
├── Another Page.md
├── Subfolder/
│   └── Subpage.md
└── attachments/
    └── image.png
```

---

## Testing Your Conversion

To test if the conversion worked correctly:

1. **Check links**: Click on internal links to ensure they navigate correctly
2. **View images**: Ensure all images are displayed
3. **Test tasks**: Check/uncheck tasks to verify they work
4. **Review callouts**: Ensure callouts render with proper styling
5. **Validate tables**: Check that tables are properly formatted
6. **Check frontmatter**: Open any file and verify YAML frontmatter exists

---

## Need Help?

- Full documentation: [README.md](README.md)
- Quick start: [QUICKSTART.md](QUICKSTART.md)
- Run examples: `python example_usage.py`

---

Happy converting! 🎉
