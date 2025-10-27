# Search Patterns & Saved Searches

Quick reference for common search patterns and filters.

## Entity Searches

### By Threat Level
```
tag:#threat-critical
tag:#threat-high
tag:#threat-medium
tag:#threat-low
```

### By Confidence
```
tag:#confidence-100
tag:#confidence-high
tag:#confidence-medium
tag:#confidence-low
```

### By Status
```
tag:#confirmed
tag:#under-investigation
tag:#pending-verification
tag:#cleared
tag:#on-hold
```

### By Type
```
path:"Entities/People"
path:"Entities/Organizations"
tag:#person
tag:#organization
```

## Investigation Searches

### Active Investigations
```
tag:#under-investigation AND tag:#threat-critical
tag:#pending-verification
tag:#discovery
```

### Leads and Theories
```
tag:#lead
tag:#theory
tag:#alias
```

### Family Networks
```
tag:#family
content:"family connection"
content:"possible family"
```

## Technical Searches

### Infrastructure
```
path:"Technical"
tag:#infrastructure
tag:#network
tag:#domain
```

### Specific Systems
```
content:"AS53616"
content:"ghoststack.net"
content:"ca94fan.xyz"
content:"IPXO"
```

### Capabilities
```
content:"DDoS"
content:"BGP"
content:"harassment"
content:"geographic obfuscation"
```

## Evidence Searches

### By Type
```
tag:#evidence
tag:#document
tag:#screenshot
tag:#technical-data
tag:#communication
```

### By Source
```
content:"Google Drive"
content:"GitHub"
content:"Companies House"
content:"ARIN"
```

### Recent Evidence
```
path:"Evidence" modified:[this week]
tag:#evidence modified:[today]
```

## Name Searches

### Wang Network
```
content:"Wang" AND (tag:#person OR tag:#organization)
content:"Junyuan Wang"
content:"Chris Wang"
content:"Roger Wang"
content:"Derek Wang"
content:"Jing Wang"
```

### Han Network
```
content:"Han" AND tag:#person
content:"Brandon Han"
content:"Xiao Han"
content:"Jerry Han"
```

### Organizations
```
content:"Asymptote Network"
content:"SalmonCloud"
content:"OSSM"
content:"Duke"
```

## Geographic Searches

### By Location
```
content:"Hong Kong"
content:"United Kingdom"
content:"Oklahoma"
content:"Dubai" OR content:"UAE"
content:"Romania"
```

### Geographic Deception
```
content:"IPXO"
content:"geographic obfuscation"
content:"location masking"
```

## Time-Based Searches

### Recent Activity
```
modified:[today]
modified:[this week]
modified:[this month]
created:[today]
```

### Date Ranges
```
modified:[2025-10-01 TO 2025-10-31]
created:[2025-09-01 TO 2025-09-30]
```

## Combined Searches

### High-Priority Entities
```
(tag:#threat-critical OR tag:#threat-high) AND tag:#confirmed
```

### Unverified High-Threat
```
tag:#threat-high AND tag:#pending-verification
```

### Recent Critical Findings
```
tag:#threat-critical modified:[this week]
```

### Technical Infrastructure by Entity
```
path:"Technical" AND content:"Junyuan Wang"
path:"Technical" AND content:"Asymptote"
```

### Evidence by Entity
```
tag:#evidence AND content:"Junyuan Wang"
tag:#evidence AND content:"SalmonCloud"
```

## Complex Searches

### Identity Theories
```
(content:"alias" OR content:"identity") AND tag:#person
```

### Family Connections
```
tag:#family OR content:"family connection"
```

### Employment/Education
```
content:"Intel" OR content:"Duke" OR content:"OSSM"
```

### Intelligence Indicators
```
content:"operational security" OR content:"OPSEC"
content:"intelligence" AND tag:#analysis
```

## Dataview Query Templates

### All Critical Threats
```dataview
TABLE threat-level, confidence, status
FROM "Entities"
WHERE threat-level = "Critical"
SORT confidence DESC
```

### Pending Verifications
```dataview
TABLE entity-type, status, priority
FROM ""
WHERE status = "Pending Verification"
SORT priority DESC
```

### Recent Updates
```dataview
TABLE file.mtime as "Modified"
FROM ""
WHERE file.mtime >= date(today) - dur(7 days)
SORT file.mtime DESC
```

### Investigation Tasks
```dataview
TASK
FROM ""
WHERE !completed AND contains(text, "[ ]")
```

### Evidence by Type
```dataview
TABLE entity, source, date
FROM #evidence
GROUP BY evidence-type
SORT date DESC
```

## Search Tips

### Wildcards
- Use `*` for any characters: `Wang*` matches Wang, Wangster, etc.
- Use `?` for single character: `W?ng` matches Wang, Wing, etc.

### Boolean Operators
- `AND` - both terms must appear
- `OR` - either term must appear
- `NOT` - term must not appear
- Use parentheses for grouping: `(Wang OR Han) AND NOT cleared`

### Case Sensitivity
- Most searches are case-insensitive
- Use quotes for exact phrases: `"Xiao Han"`

### Regular Expressions
- Use `/pattern/` for regex searches
- Example: `/Wang|Han/` matches either Wang or Han

## Obsidian Search Operators

### File Paths
```
path:"Entities/People"
path:"Technical"
file:"Dashboard"
```

### Tags
```
tag:#threat-critical
tag:#evidence
-tag:#cleared (exclude tag)
```

### Content
```
content:"exact phrase"
content:/regex pattern/
```

### Properties
```
modified:[date]
created:[date]
size:[>10kb]
```

## Quick Access Bookmarks

Create bookmarks for frequently used searches:

1. **Critical Active**: `tag:#threat-critical AND tag:#under-investigation`
2. **Pending Verification**: `tag:#pending-verification AND (tag:#threat-critical OR tag:#threat-high)`
3. **Recent Evidence**: `tag:#evidence modified:[this week]`
4. **Wang Network**: `content:"Wang" AND tag:#person`
5. **Technical Infrastructure**: `path:"Technical" AND tag:#infrastructure`

## Graph View Filters

### High Priority Network
```
tag:#threat-critical OR tag:#threat-high
```

### Entity Network Only
```
path:"Entities"
```

### Technical Infrastructure
```
path:"Technical" OR tag:#infrastructure
```

### Evidence Links
```
tag:#evidence
```

---

← Back to [[Quick Reference Guide]]
← Back to [[Investigation Dashboard]]

Tags: #reference #search #patterns #quick-access
