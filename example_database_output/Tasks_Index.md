# Tasks Database

*Converted from Notion database*

## All Items

```dataview
TABLE status as "Status", priority as "Priority", due_date as "Due Date", completed as "Completed"
FROM "example_database_output"
WHERE contains(tags, "database-item")
SORT file.name ASC
```

## Quick Views

### By Status

**Completed = Yes:**
```dataview
TABLE status as "Status", priority as "Priority", due_date as "Due Date"
FROM "example_database_output"
WHERE completed = true
```

### Timeline

**Sorted by Due Date:**
```dataview
TABLE due_date as "Date", status as "Status", priority as "Priority"
FROM "example_database_output"
WHERE due_date
SORT due_date DESC
```

### List View

```dataview
LIST
FROM "example_database_output"
WHERE contains(tags, "database-item")
SORT file.name ASC
```

## How to Use

1. Install the [Dataview plugin](https://github.com/blacksmithgu/obsidian-dataview) in Obsidian
2. Enable Dataview in Settings → Community Plugins
3. The tables above will automatically populate with your data
4. Click on any item to edit it
5. Modify frontmatter properties to update the database

## Available Properties

- **Name** (`name`) - text
- **Status** (`status`) - select
- **Priority** (`priority`) - select
- **Due Date** (`due_date`) - date
- **Completed** (`completed`) - checkbox
- **Tags** (`tags`) - multi-select
- **Assigned To** (`assigned_to`) - text
- **Notes** (`notes`) - text

## Custom Queries

You can create your own Dataview queries. Examples:

```dataview
# Search for specific text
TABLE
FROM "example_database_output"
WHERE contains(file.name, "search-term")
```

```dataview
# Count items
TABLE length(rows) as "Count"
FROM "example_database_output"
GROUP BY tags
```
