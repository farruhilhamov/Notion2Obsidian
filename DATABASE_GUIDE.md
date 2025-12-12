# Notion Database to Obsidian Guide

Complete guide for converting Notion databases (including Base lists) to manageable Obsidian databases using Dataview.

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [How It Works](#how-it-works)
- [Database Features](#database-features)
- [Dataview Setup](#dataview-setup)
- [Query Examples](#query-examples)
- [Managing Your Database](#managing-your-database)
- [Advanced Usage](#advanced-usage)

---

## Overview

### What Gets Converted?

When you export a Notion database (including Base tables with lists), the converter:

1. ✅ Creates individual Obsidian notes for each database row
2. ✅ Adds all properties as YAML frontmatter
3. ✅ Generates an index file with Dataview queries
4. ✅ Preserves all data types (text, numbers, dates, checkboxes, lists)
5. ✅ Creates multiple view templates (table, list, filtered)

### Notion Database → Obsidian Structure

**Notion:**
```
Base Database
├── Item 1 (Name: Task A, Status: Done, Priority: High)
├── Item 2 (Name: Task B, Status: In Progress, Priority: Medium)
└── Item 3 (Name: Task C, Status: Not Started, Priority: Low)
```

**Obsidian:**
```
Base_Database/
├── Task A.md          (with frontmatter)
├── Task B.md          (with frontmatter)
├── Task C.md          (with frontmatter)
└── Base_Index.md      (Dataview queries)
```

---

## Quick Start

### Step 1: Export from Notion

1. Open your Notion database page
2. Click `...` → `Export`
3. Format: **Markdown & CSV**
4. Check: **Include subpages**
5. Export and extract ZIP

### Step 2: Convert

```bash
python notion_to_obsidian.py ./NotionExport ./ObsidianVault --verbose
```

The converter automatically detects CSV files (databases) and converts them!

### Step 3: Install Dataview Plugin

1. Open Obsidian Settings
2. Go to **Community Plugins**
3. Browse and install **Dataview**
4. Enable the plugin

### Step 4: View Your Database

Open the `{DatabaseName}_Index.md` file to see your database with interactive queries!

---

## How It Works

### 1. Individual Note Files

Each database row becomes a separate markdown file:

**Example: Task A.md**
```markdown
---
name: Task A
status: Done
priority: High
due_date: 2025-12-15
completed: true
tags:
  - database-item
---

# Task A

## Properties

| Property | Value |
|----------|-------|
| Name | Task A |
| Status | Done |
| Priority | High |
| Due Date | 2025-12-15 |
| Completed | ✓ |

## Notes

*Add your notes here...*
```

### 2. Index File with Dataview Queries

The index file contains live queries that display your data:

**Example: Base_Index.md**
```markdown
# Base Database

## All Items

​```dataview
TABLE status as "Status", priority as "Priority", due_date as "Due Date"
FROM "Base_Database"
WHERE contains(tags, "database-item")
SORT file.name ASC
​```

## Quick Views

### By Status

**Status = Done:**
​```dataview
TABLE priority as "Priority", due_date as "Due Date"
FROM "Base_Database"
WHERE status = "Done"
​```
```

---

## Database Features

### Supported Property Types

| Notion Type | Obsidian Type | Example |
|-------------|---------------|---------|
| Text | `text` | `name: Task A` |
| Number | `number` | `priority: 5` |
| Checkbox | `boolean` | `completed: true` |
| Date | `date` | `due_date: 2025-12-15` |
| Select | `text` | `status: Done` |
| Multi-select | `list` | `tags: [work, urgent]` |
| URL | `text` | `link: https://example.com` |
| Email | `text` | `email: user@example.com` |
| Phone | `text` | `phone: 555-1234` |

### Property Naming

Notion properties are automatically converted to valid YAML keys:

| Notion Property | Obsidian Key |
|----------------|--------------|
| Task Name | `task_name` |
| Due Date | `due_date` |
| Is Complete? | `is_complete` |
| Priority Level | `priority_level` |

---

## Dataview Setup

### Installation

1. Open Obsidian Settings (⚙️)
2. Navigate to: **Community Plugins** → **Browse**
3. Search: "Dataview"
4. Click **Install**, then **Enable**

### Enable JavaScript Queries (Optional)

For advanced queries:

1. Settings → **Dataview**
2. Enable: **Enable JavaScript Queries**
3. Enable: **Enable Inline JavaScript Queries**

### Verify Installation

Create a test note with:

```markdown
​```dataview
LIST
FROM ""
LIMIT 5
​```
```

If you see a list of files, Dataview is working!

---

## Query Examples

### Basic Table View

Show all items with selected properties:

```markdown
​```dataview
TABLE status, priority, due_date
FROM "Base_Database"
WHERE contains(tags, "database-item")
​```
```

### Filtered Views

**Show only incomplete tasks:**
```markdown
​```dataview
TABLE priority as "Priority", due_date as "Due"
FROM "Base_Database"
WHERE completed = false
SORT due_date ASC
​```
```

**Show high priority items:**
```markdown
​```dataview
TABLE status, due_date
FROM "Base_Database"
WHERE priority = "High"
​```
```

**Show items due this week:**
```markdown
​```dataview
TABLE status, priority
FROM "Base_Database"
WHERE due_date >= date(today) AND due_date <= date(today) + dur(7 days)
SORT due_date ASC
​```
```

### List Views

**Simple list of all items:**
```markdown
​```dataview
LIST
FROM "Base_Database"
WHERE contains(tags, "database-item")
SORT file.name
​```
```

**List with extra info:**
```markdown
​```dataview
LIST status + " - " + priority
FROM "Base_Database"
WHERE contains(tags, "database-item")
​```
```

### Grouped Views

**Group by status:**
```markdown
​```dataview
TABLE rows.file.link as "Items"
FROM "Base_Database"
WHERE contains(tags, "database-item")
GROUP BY status
​```
```

**Count items by priority:**
```markdown
​```dataview
TABLE length(rows) as "Count"
FROM "Base_Database"
WHERE contains(tags, "database-item")
GROUP BY priority
​```
```

### Calendar/Timeline Views

**Sort by date:**
```markdown
​```dataview
TABLE status, priority
FROM "Base_Database"
WHERE due_date
SORT due_date DESC
​```
```

**Upcoming deadlines:**
```markdown
​```dataview
TABLE due_date as "Deadline", priority
FROM "Base_Database"
WHERE due_date >= date(today)
SORT due_date ASC
LIMIT 10
​```
```

### Task Views

**Show checkboxes:**
```markdown
​```dataview
TASK
FROM "Base_Database"
WHERE !completed
​```
```

---

## Managing Your Database

### Adding New Items

1. Create new `.md` file in database folder
2. Add frontmatter with properties:

```markdown
---
name: New Task
status: Not Started
priority: Medium
due_date: 2025-12-20
completed: false
tags:
  - database-item
---

# New Task

## Notes

Your notes here...
```

### Editing Items

**Option 1: Edit frontmatter directly**
- Open the note file
- Modify values in the `---` section
- Dataview updates automatically

**Option 2: Use Obsidian's properties panel**
- Enable: Settings → Core Plugins → **Properties View**
- Click on any property to edit

### Deleting Items

Simply delete the `.md` file - Dataview updates automatically.

### Bulk Operations

Use text editor or scripts to modify multiple files:

**Example: Add tag to all items**
```bash
# Find all database items and add a tag
find Base_Database -name "*.md" -exec sed -i '/tags:/a\  - project-x' {} \;
```

---

## Advanced Usage

### Custom Views

Create your own view files:

**MyCustomView.md:**
```markdown
# My Custom Database View

## Urgent Tasks
​```dataview
TABLE status, due_date
FROM "Base_Database"
WHERE priority = "High" AND completed = false
SORT due_date ASC
​```

## Completed This Month
​```dataview
LIST
FROM "Base_Database"
WHERE completed = true AND due_date >= date(today) - dur(30 days)
​```
```

### JavaScript Queries

For complex logic (requires JS queries enabled):

```markdown
​```dataviewjs
let pages = dv.pages('"Base_Database"')
  .where(p => p.tags?.includes("database-item"));

let completed = pages.where(p => p.completed).length;
let total = pages.length;
let percentage = Math.round((completed / total) * 100);

dv.header(2, `Progress: ${completed}/${total} (${percentage}%)`);

dv.table(["Name", "Status", "Priority"],
  pages.map(p => [p.file.link, p.status, p.priority])
);
​```
```

### Inline Queries

Embed queries in regular notes:

```markdown
I have `= length(filter(rows, (r) => r.completed = false))` tasks remaining.

My next deadline is `= min(rows.due_date)`.
```

### Template for New Items

Create a template file:

**Templates/DatabaseItem.md:**
```markdown
---
name: "{{title}}"
status: Not Started
priority: Medium
due_date:
completed: false
tags:
  - database-item
---

# {{title}}

## Properties

*Properties are in frontmatter above*

## Notes

*Add your notes here...*

## Related

-

## Tasks

- [ ]
```

Use with Templater or core Templates plugin.

---

## Comparison: Notion vs Obsidian

### Notion Database Features

| Feature | Obsidian Equivalent |
|---------|---------------------|
| Table view | Dataview TABLE query |
| Board view | Manual or plugin (Kanban) |
| Gallery view | Manual or plugin |
| Calendar view | Dataview + Calendar plugin |
| List view | Dataview LIST query |
| Filters | Dataview WHERE clause |
| Sorts | Dataview SORT clause |
| Formulas | Dataview calculations |
| Relations | Dataview links |
| Rollups | Dataview GROUP BY |

### Advantages in Obsidian

✅ **Plain text** - Future-proof, no vendor lock-in
✅ **Offline** - Works without internet
✅ **Fast** - No loading times
✅ **Flexible** - Create any view you want
✅ **Version control** - Use Git to track changes
✅ **Programmable** - JavaScript queries for custom logic
✅ **Backlinks** - Automatic bidirectional linking

### What You Lose from Notion

❌ Real-time collaboration
❌ GUI for creating views
❌ Board/Gallery drag-and-drop
❌ Built-in database templates
❌ Sharing with public links

### Recommended Workflow

1. **Use Obsidian for**: Personal databases, knowledge management, local-first workflow
2. **Keep Notion for**: Team collaboration, client-facing databases
3. **Sync periodically**: Export from Notion, convert, review in Obsidian

---

## Troubleshooting

### Dataview queries not showing

**Problem**: Queries show as code blocks
**Solution**:
- Install Dataview plugin
- Enable in Settings → Community Plugins
- Refresh the note

### Properties not appearing

**Problem**: Frontmatter not recognized
**Solution**:
- Ensure `---` on separate lines
- Check YAML syntax (colons, indentation)
- No tabs, only spaces

### Query returns no results

**Problem**: `FROM` path incorrect
**Solution**:
- Use folder name exactly: `FROM "Base_Database"`
- Check file location
- Ensure tag exists: `WHERE contains(tags, "database-item")`

### Dates not sorting

**Problem**: Dates as text
**Solution**:
- Use format: `YYYY-MM-DD`
- Convert in query: `date(due_date)`

### Special characters in property names

**Problem**: Property names with spaces/symbols
**Solution**:
- Converter auto-fixes to: `property_name`
- Use underscores in queries: `WHERE task_name`

---

## Examples

### Example 1: Project Tracker

**Projects_Database/Project_Alpha.md:**
```markdown
---
name: Project Alpha
status: In Progress
priority: High
start_date: 2025-01-01
end_date: 2025-03-31
budget: 50000
completed_percentage: 65
team_members: [Alice, Bob, Charlie]
tags:
  - database-item
  - project
---

# Project Alpha

*Major initiative for Q1 2025*
```

**Projects_Index.md:**
```markdown
​```dataview
TABLE status, priority, completed_percentage + "%" as "Progress", end_date as "Deadline"
FROM "Projects_Database"
WHERE contains(tags, "database-item")
SORT priority DESC, end_date ASC
​```
```

### Example 2: Contact List

**Contacts_Database/John_Doe.md:**
```markdown
---
name: John Doe
email: john@example.com
phone: 555-1234
company: Acme Corp
role: Developer
last_contact: 2025-12-01
tags:
  - database-item
  - contact
---

# John Doe

## Last Conversation

Met to discuss collaboration...
```

### Example 3: Reading List

**Books_Database/Atomic_Habits.md:**
```markdown
---
title: Atomic Habits
author: James Clear
status: Reading
rating: 5
pages: 320
started: 2025-12-01
finished:
genre: [Self-Help, Productivity]
tags:
  - database-item
  - book
---

# Atomic Habits

## Notes

Chapter 1: The power of tiny changes...
```

---

## Resources

### Official Documentation

- [Dataview Plugin](https://blacksmithgu.github.io/obsidian-dataview/)
- [Dataview Query Reference](https://blacksmithgu.github.io/obsidian-dataview/queries/structure/)
- [Obsidian Properties](https://help.obsidian.md/Editing+and+formatting/Properties)

### Helpful Plugins

- **Dataview** - Query your notes
- **Kanban** - Board view for tasks
- **DB Folder** - Spreadsheet-like editing
- **Templater** - Advanced templates
- **QuickAdd** - Quick entry forms

### Community

- [Obsidian Forum](https://forum.obsidian.md/)
- [Dataview Discussions](https://github.com/blacksmithgu/obsidian-dataview/discussions)
- [r/ObsidianMD](https://reddit.com/r/ObsidianMD)

---

## Next Steps

1. ✅ Convert your Notion database
2. 📦 Install Dataview plugin
3. 👀 Open the `_Index.md` file
4. 🎨 Customize views to your needs
5. ➕ Add new items
6. 🔍 Create custom queries
7. 🚀 Enjoy your local-first database!

---

**Questions?** Check the main [README.md](README.md) or [QUICKSTART.md](QUICKSTART.md)

**Need examples?** Run `python example_usage.py` for live demos

---

Happy database management! 📊✨
