# Quick Reference Guide

Essential shortcuts, search patterns, and workflows for rapid investigation.

## Fast Navigation

### Maps of Content (MOC)
- [[Entities MOC]] - All people and organizations
- [[Technical MOC]] - Infrastructure and technical findings
- [[Analysis MOC]] - Analytical work and assessments
- [[Evidence MOC]] - Evidence tracking and documentation

### Core Hubs
- [[Investigation Dashboard]] - Main command center
- [[Timeline]] - Chronological discoveries
- [[Evidence Repository]] - Master evidence index

## Quick Search Patterns

### By Status
```
tag:#threat-critical
tag:#threat-high
tag:#confirmed
tag:#under-investigation
```

### By Entity Type
```
path:"Entities/People"
path:"Entities/Organizations"
path:"Technical"
path:"Analysis"
```

### By Confidence Level
```
tag:#confidence-100
tag:#confidence-high
tag:#confidence-medium
tag:#confidence-low
```

### By Investigation Phase
```
tag:#discovery
tag:#verification
tag:#analysis
tag:#monitoring
```

## Search Operators

### Combining Searches
```
tag:#person AND tag:#threat-critical
path:"Entities" AND (Wang OR Han)
tag:#technical AND tag:#confirmed
```

### Date-Based Searches
```
created:[YYYY-MM-DD]
modified:[YYYY-MM-DD]
```

### Content Searches
```
content:"AS53616"
content:"github.com"
content:"signalhire"
```

## Rapid Data Entry

### Create New Entity
1. Use Command Palette: `Ctrl/Cmd + P`
2. Type "Templates: Insert Template"
3. Choose template:
   - `person-template`
   - `organization-template`
   - `technical-finding-template`
   - `evidence-entry-template`
   - `quick-lead-template`

### Quick Links
Use `[[entity-name]]` to create links
Use `#tag` for categorization

## Common Workflows

### New Lead Investigation
1. Create note using `quick-lead-template`
2. Document source and details
3. Link to related entities
4. Set priority and status
5. Add investigation steps
6. Update as findings develop

### New Evidence Capture
1. Create note using `evidence-entry-template`
2. Fill in metadata (date, source, type)
3. Describe content and significance
4. Link to related entities
5. Add to [[Evidence Repository]]
6. Upload to Google Drive
7. Update timeline if relevant

### New Entity (Person/Org)
1. Create note in appropriate folder
2. Use `person-template` or `organization-template`
3. Fill in known information
4. Set confidence and threat levels
5. Link to evidence and timeline
6. Add to appropriate MOC
7. Update [[Investigation Dashboard]]

### Technical Discovery
1. Create note using `technical-finding-template`
2. Document technical details
3. Analyze capabilities and connections
4. Link to entities
5. Add to [[Technical MOC]]
6. Update timeline

## Dataview Queries

### All High-Priority Entities
```dataview
TABLE confidence, threat-level, status
FROM "Entities"
WHERE threat-level = "Critical" OR threat-level = "High"
SORT confidence DESC
```

### Recent Activity
```dataview
TABLE file.mtime as "Modified"
FROM ""
SORT file.mtime DESC
LIMIT 10
```

### Pending Investigations
```dataview
TASK
FROM ""
WHERE !completed
```

### Evidence by Type
```dataview
TABLE evidence-type, entity, date
FROM #evidence
SORT date DESC
```

## Keyboard Shortcuts

### Essential Obsidian Commands
- `Ctrl/Cmd + P`: Command palette
- `Ctrl/Cmd + O`: Quick switcher (file search)
- `Ctrl/Cmd + F`: Search in current file
- `Ctrl/Cmd + Shift + F`: Search in all files
- `Ctrl/Cmd + E`: Toggle edit/preview
- `Ctrl/Cmd + Click`: Open link in new pane
- `Alt + Click`: Open link in new tab

### Navigation
- `Ctrl/Cmd + Alt + Left/Right`: Navigate back/forward
- `Ctrl/Cmd + K`: Insert link
- `Ctrl/Cmd + G`: Open graph view

## Tags Taxonomy

### Entity Tags
- `#person` - Individual person
- `#organization` - Company/group
- `#family` - Family connection
- `#alias` - Possible alternate identity

### Threat Tags
- `#threat-critical` - Critical threat level
- `#threat-high` - High threat level
- `#threat-medium` - Medium threat level
- `#threat-low` - Low threat level

### Confidence Tags
- `#confidence-100` - Confirmed/verified
- `#confidence-high` - High confidence (70-99%)
- `#confidence-medium` - Medium confidence (40-69%)
- `#confidence-low` - Low confidence (<40%)

### Status Tags
- `#confirmed` - Verified finding
- `#under-investigation` - Active investigation
- `#pending-verification` - Needs verification
- `#cleared` - No longer suspect
- `#on-hold` - Investigation paused

### Evidence Tags
- `#evidence` - Evidence item
- `#document` - Document evidence
- `#screenshot` - Screenshot evidence
- `#technical-data` - Technical/network data
- `#communication` - Email/message evidence

### Technical Tags
- `#infrastructure` - Network infrastructure
- `#domain` - Domain/DNS
- `#network` - Network analysis
- `#forensics` - Digital forensics
- `#github` - GitHub analysis

### Investigation Tags
- `#discovery` - Initial discovery phase
- `#verification` - Verification phase
- `#analysis` - Deep analysis phase
- `#monitoring` - Ongoing monitoring
- `#lead` - Investigation lead

## Cross-Reference Strategies

### Entity Cross-Referencing
When creating entity notes:
1. Link to all related entities
2. Link to evidence
3. Link to technical infrastructure
4. Link to timeline events
5. Link from MOC

### Evidence Cross-Referencing
When documenting evidence:
1. Link to all mentioned entities
2. Link to related technical findings
3. Add to timeline
4. Reference in MOC
5. Update Evidence Repository

### Technical Cross-Referencing
When documenting technical findings:
1. Link to associated entities
2. Link to related infrastructure
3. Cross-reference other technical notes
4. Add to Technical MOC
5. Update timeline

## Investigation Checklists

### Initial Entity Assessment
- [ ] Basic information gathered
- [ ] Confidence level assigned
- [ ] Threat level assessed
- [ ] Related entities identified
- [ ] Evidence linked
- [ ] Timeline updated
- [ ] MOC updated
- [ ] Dashboard updated

### Evidence Processing
- [ ] Metadata documented
- [ ] Source verified
- [ ] Content described
- [ ] Entities linked
- [ ] Timeline updated
- [ ] Stored in Drive
- [ ] Added to repository
- [ ] Confidence assessed

### Technical Discovery
- [ ] Technical details documented
- [ ] Capabilities analyzed
- [ ] Entities linked
- [ ] Infrastructure mapped
- [ ] IoCs extracted
- [ ] Cross-referenced
- [ ] Added to Technical MOC
- [ ] Timeline updated

## Quick Links

- [[Investigation Dashboard]]
- [[Entities MOC]]
- [[Technical MOC]]
- [[Analysis MOC]]
- [[Evidence MOC]]
- [[Timeline]]
- [[Evidence Repository]]
- [[Investigation Methodology]]

---

Tags: #guide #reference #quick-access #workflow
