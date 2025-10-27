# Live Dashboard

Dynamic, auto-updating investigation dashboard powered by Dataview queries.

**Note**: This dashboard requires the Dataview plugin to be installed and enabled in Obsidian.

## Critical Threats

### Entities - Critical Threat Level
```dataview
TABLE threat-level as "Threat", confidence as "Confidence", status as "Status"
FROM "Entities"
WHERE threat-level = "Critical" OR threat-level = "CRITICAL"
SORT confidence DESC
```

### High Priority Entities
```dataview
TABLE threat-level as "Threat", confidence as "Confidence", status as "Status"
FROM "Entities"
WHERE threat-level = "High" OR confidence >= 70
SORT threat-level DESC, confidence DESC
```

## Investigation Status

### Active Investigations
```dataview
TABLE status, priority, file.mtime as "Last Updated"
FROM ""
WHERE status = "Under Investigation" OR status = "Active"
SORT priority DESC, file.mtime DESC
```

### Pending Verification
```dataview
TABLE confidence, priority, file.mtime as "Last Updated"
FROM ""
WHERE status = "Pending Verification" OR status = "Needs Verification"
SORT priority DESC
```

### Open Investigation Tasks
```dataview
TASK
FROM ""
WHERE !completed
GROUP BY file.link
```

## Recent Activity

### Modified This Week
```dataview
TABLE file.mtime as "Modified", file.folder as "Folder"
FROM ""
WHERE file.mtime >= date(today) - dur(7 days)
SORT file.mtime DESC
LIMIT 20
```

### New Entities (Last 30 Days)
```dataview
TABLE file.ctime as "Created", threat-level as "Threat", confidence as "Confidence"
FROM "Entities"
WHERE file.ctime >= date(today) - dur(30 days)
SORT file.ctime DESC
```

### Recent Evidence
```dataview
TABLE evidence-type as "Type", entity as "Entity", source as "Source", date
FROM #evidence
WHERE file.ctime >= date(today) - dur(30 days)
SORT date DESC
LIMIT 15
```

## Entities Overview

### All People
```dataview
TABLE confidence as "Conf%", threat-level as "Threat", status as "Status"
FROM "Entities/People"
SORT confidence DESC
```

### All Organizations
```dataview
TABLE confidence as "Conf%", threat-level as "Threat", status as "Status"
FROM "Entities/Organizations"
SORT threat-level DESC, confidence DESC
```

## Technical Infrastructure

### All Technical Assets
```dataview
TABLE status, capabilities, threat-level as "Threat"
FROM "Technical"
SORT threat-level DESC, file.name ASC
```

### Active Infrastructure
```dataview
TABLE status, capabilities
FROM "Technical"
WHERE status = "Active"
SORT file.name ASC
```

## Evidence Tracking

### Evidence by Type
```dataview
TABLE count(rows) as "Count"
FROM #evidence
GROUP BY evidence-type
SORT count(rows) DESC
```

### Evidence by Entity
```dataview
TABLE evidence-type as "Type", source as "Source", date
FROM #evidence
GROUP BY entity
SORT date DESC
```

### Unverified Evidence
```dataview
TABLE evidence-type as "Type", entity as "Entity", source as "Source"
FROM #evidence
WHERE confidence = "Low" OR confidence = "Unverified"
SORT file.ctime DESC
```

## Investigation Metrics

### Confidence Distribution
```dataview
TABLE count(rows) as "Count"
FROM "Entities"
GROUP BY confidence
SORT confidence DESC
```

### Threat Level Distribution
```dataview
TABLE count(rows) as "Count"
FROM "Entities"
GROUP BY threat-level
SORT threat-level DESC
```

### Investigation Phase Status
```dataview
TABLE count(rows) as "Count"
FROM ""
GROUP BY status
SORT count(rows) DESC
```

## Network Analysis

### Wang Network Members
```dataview
TABLE confidence, threat-level, status
FROM "Entities/People"
WHERE contains(file.name, "Wang")
SORT confidence DESC
```

### Han Network Members
```dataview
TABLE confidence, threat-level, status
FROM "Entities/People"
WHERE contains(file.name, "Han")
SORT confidence DESC
```

### Primary Organizations
```dataview
TABLE confidence, threat-level, status
FROM "Entities/Organizations"
WHERE threat-level = "Critical" OR threat-level = "High"
SORT threat-level DESC
```

## Timeline Overview

### Recent Timeline Events
```dataview
TABLE date, event, entities, source
FROM "Timeline"
SORT date DESC
LIMIT 10
```

## Analysis Progress

### Analysis Files
```dataview
TABLE status, file.mtime as "Last Modified"
FROM "Analysis"
SORT file.mtime DESC
```

### Completed Analyses
```dataview
TABLE file.mtime as "Completed"
FROM "Analysis"
WHERE status = "Completed" OR status = "Final"
SORT file.mtime DESC
```

### In-Progress Analyses
```dataview
TABLE status, priority
FROM "Analysis"
WHERE status = "In Progress" OR status = "Draft"
SORT priority DESC
```

## Geographic Distribution

### Entities by Location
```dataview
TABLE location, threat-level, confidence
FROM "Entities"
WHERE location
GROUP BY location
SORT count(rows) DESC
```

## Alias Tracking

### Potential Aliases
```dataview
TABLE alias-of as "Alias Of", confidence, status
FROM "Entities/People"
WHERE alias-of OR contains(file.content, "alias")
SORT confidence DESC
```

## Family Networks

### Family Connections
```dataview
TABLE family-connections as "Family", confidence
FROM "Entities/People"
WHERE family-connections
SORT confidence DESC
```

## Technical Capabilities

### Confirmed Capabilities
```dataview
TABLE entity, capability, confidence
FROM ""
WHERE capability AND confidence = "Confirmed"
```

## Investigation Workload

### By Priority
```dataview
TABLE count(rows) as "Items"
FROM ""
WHERE priority
GROUP BY priority
SORT priority DESC
```

### By Investigator/Focus Area
```dataview
TABLE count(rows) as "Items", status
FROM ""
WHERE assigned-to
GROUP BY assigned-to
```

## Quality Metrics

### Notes Without Tags
```dataview
TABLE file.folder
FROM ""
WHERE !file.tags OR length(file.tags) = 0
WHERE file.folder != "Templates" AND file.folder != "MOC"
SORT file.mtime DESC
```

### Notes Without Links
```dataview
TABLE file.folder
FROM ""
WHERE length(file.outlinks) = 0
WHERE file.folder != "Templates" AND file.folder != "MOC"
SORT file.mtime DESC
```

### Orphan Notes
```dataview
TABLE file.folder, file.mtime as "Modified"
FROM ""
WHERE length(file.inlinks) = 0 AND length(file.outlinks) = 0
WHERE file.folder != "Templates" AND file.folder != "MOC"
SORT file.mtime DESC
```

## Quick Stats

### Total Counts
```dataview
TABLE count(rows) as "Count"
FROM ""
GROUP BY file.folder
SORT count(rows) DESC
```

---

**Refresh**: This page auto-updates when you switch to preview mode or reopen the note.

← Back to [[Investigation Dashboard]]

Tags: #dashboard #dataview #live #metrics
