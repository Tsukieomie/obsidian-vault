# Vault Upgrade - Investigation Optimization System

## Overview

Your Obsidian vault has been upgraded with a comprehensive investigation workflow system designed to speed up research, evidence gathering, cross-referencing, and analysis.

## What's New

### 1. Maps of Content (MOC) System

Four specialized navigation hubs for quick access:

- **[[Entities MOC]]** - All people and organizations under investigation
- **[[Technical MOC]]** - Infrastructure, networks, and technical findings
- **[[Analysis MOC]]** - Analytical work and threat assessments
- **[[Evidence MOC]]** - Evidence tracking and documentation

**Why**: MOCs provide instant access to specific areas of your investigation without searching.

### 2. Investigation Templates

Standardized templates for rapid, consistent data entry:

- `person-template` - Person investigation notes
- `organization-template` - Organization investigation notes
- `technical-finding-template` - Technical discoveries
- `evidence-entry-template` - Evidence documentation
- `quick-lead-template` - Fast lead capture

**How to use**:
1. Create new note
2. Open Command Palette (`Ctrl/Cmd + P`)
3. Type "Templates: Insert Template"
4. Choose appropriate template

**Why**: Templates ensure you capture all important information consistently and save time.

### 3. Enhanced Dashboard

Your [[Investigation Dashboard]] now includes:
- Quick Navigation section linking to all MOCs
- Direct access to methodology and reference guides
- All existing investigation tracking

### 4. Dynamic Tracking

**[[Live Dashboard]]** - Auto-updating views powered by Dataview:
- Critical threats list
- Recent activity feed
- Investigation status tracking
- Evidence metrics
- Network analysis views
- Quality control checks

**Note**: Requires Dataview plugin (install from Obsidian Community Plugins)

### 5. Reference Guides

- **[[Quick Reference Guide]]** - Search patterns, shortcuts, workflows
- **[[Investigation Methodology]]** - Standards and best practices
- **[[Search Patterns]]** - Saved searches and query templates

### 6. Enhanced Cross-Referencing

Templates include:
- Automatic linking to related entities
- Timeline integration
- Evidence linking
- Dataview queries for relationship mapping

## How to Use This System

### Starting a New Investigation

1. **Capture the lead**: Use `quick-lead-template`
2. **Create entity notes**: Use `person-template` or `organization-template`
3. **Document evidence**: Use `evidence-entry-template`
4. **Track technical findings**: Use `technical-finding-template`
5. **Update the timeline**: Add to [[Timeline]]
6. **Link everything**: Use `[[entity-name]]` syntax
7. **Tag appropriately**: Use standardized tags (see below)

### Daily Workflow

1. **Start here**: [[Investigation Dashboard]]
2. **Check activity**: [[Live Dashboard]] for recent updates
3. **Work on tasks**: Check pending verifications and open tasks
4. **Document findings**: Use appropriate templates
5. **Cross-reference**: Link to related entities and evidence
6. **Update MOCs**: Ensure new notes are accessible from MOCs

### Quick Search

Instead of manually searching:
1. Use [[Search Patterns]] for common queries
2. Use [[Quick Reference Guide]] for shortcuts
3. Use MOCs for categorical browsing
4. Use [[Live Dashboard]] for filtered views

### Evidence Workflow

1. **Capture**: Create note with `evidence-entry-template`
2. **Classify**: Set type, source, confidence
3. **Link**: Connect to entities and technical findings
4. **Store**: Upload to Google Drive
5. **Index**: Update [[Evidence Repository]]
6. **Timeline**: Add to [[Timeline]] if relevant

## Tag System

### Standard Tags

**Threat Levels:**
- `#threat-critical`
- `#threat-high`
- `#threat-medium`
- `#threat-low`

**Confidence:**
- `#confidence-100` (Confirmed)
- `#confidence-high` (70-99%)
- `#confidence-medium` (40-69%)
- `#confidence-low` (0-39%)

**Status:**
- `#confirmed`
- `#under-investigation`
- `#pending-verification`
- `#cleared`
- `#on-hold`

**Entity Types:**
- `#person`
- `#organization`
- `#family`
- `#alias`

**Evidence:**
- `#evidence`
- `#document`
- `#screenshot`
- `#technical-data`

**Technical:**
- `#infrastructure`
- `#network`
- `#domain`
- `#forensics`

See [[Quick Reference Guide]] for complete taxonomy.

## Folder Structure

```
obsidian-vault/
├── MOC/                      # Maps of Content
│   ├── Entities MOC.md
│   ├── Technical MOC.md
│   ├── Analysis MOC.md
│   └── Evidence MOC.md
│
├── Templates/                # Investigation templates
│   ├── person-template.md
│   ├── organization-template.md
│   ├── technical-finding-template.md
│   ├── evidence-entry-template.md
│   └── quick-lead-template.md
│
├── Entities/                 # People and organizations
│   ├── People/
│   └── Organizations/
│
├── Technical/                # Technical infrastructure
├── Analysis/                 # Analytical work
│
├── Investigation Dashboard.md   # Main hub
├── Live Dashboard.md           # Dynamic tracking
├── Quick Reference Guide.md    # Shortcuts and patterns
├── Investigation Methodology.md # Standards
├── Search Patterns.md          # Saved searches
├── Timeline.md                 # Chronological record
└── Evidence Repository.md      # Evidence index
```

## Key Features

### 1. Faster Navigation
- MOC system: 2 clicks to any area
- Quick Navigation in Dashboard
- Dataview filtered views

### 2. Faster Data Entry
- Templates auto-fill structure
- Consistent formatting
- Pre-built linking sections

### 3. Better Cross-Referencing
- Template-based linking
- Dataview relationship queries
- Bidirectional links
- Timeline integration

### 4. Enhanced Search
- Saved search patterns
- Tag-based filtering
- Dataview dynamic queries
- Graph view filters

### 5. Quality Control
- Standardized tags
- Template consistency
- Orphan note detection
- Completeness checking

## Installation Requirements

### Required Plugin: Dataview

1. Open Obsidian Settings
2. Go to Community Plugins
3. Browse and search "Dataview"
4. Install and Enable

**Why**: Powers [[Live Dashboard]] and dynamic queries in MOCs

### Recommended Plugins

- **Templater** - Advanced template features
- **Excalidraw** - Visual network mapping
- **Graph Analysis** - Enhanced graph view
- **QuickAdd** - Rapid note creation
- **Tag Wrangler** - Tag management

## Workflow Examples

### Example 1: New Person Discovery

1. Find information about "Jane Doe" on LinkedIn
2. Create new note: `Entities/People/Jane Doe.md`
3. Insert `person-template`
4. Fill in known information
5. Set confidence: Medium (60%)
6. Set threat: To be determined
7. Link to related entities: `[[Organization Name]]`
8. Create evidence entry for LinkedIn profile
9. Link evidence to person
10. Update [[Timeline]] with discovery date
11. Entity automatically appears in [[Entities MOC]]

### Example 2: Technical Finding

1. Discover new domain in network scan
2. Create `Technical/example-domain.md`
3. Insert `technical-finding-template`
4. Document WHOIS, DNS, hosting info
5. Link to associated entities
6. Add IoCs (Indicators of Compromise)
7. Update [[Technical MOC]]
8. Create evidence entry for scan results

### Example 3: Evidence Collection

1. Find company registration document
2. Create evidence entry
3. Fill metadata: type=Document, source=Companies House
4. Upload to Google Drive
5. Add Drive link to note
6. Link to organization entity
7. Link to any mentioned people
8. Add to [[Evidence Repository]]
9. Update timeline if significant

## Tips for Maximum Efficiency

### 1. Use Templates Always
Even for quick notes - they're faster than starting from scratch.

### 2. Link As You Go
Don't defer linking - do it while creating notes.

### 3. Tag Consistently
Use the standard tag taxonomy in [[Quick Reference Guide]].

### 4. Update the Dashboard Weekly
Keep [[Investigation Dashboard]] current with active investigations.

### 5. Review the Live Dashboard Daily
Check [[Live Dashboard]] for pending tasks and recent activity.

### 6. Use MOCs for Navigation
Bookmark the four MOCs for instant access to any area.

### 7. Leverage Dataview
Learn basic Dataview queries to create custom views.

### 8. Cross-Reference Everything
Every entity should link to evidence, other entities, and timeline.

### 9. Regular Quality Checks
Use [[Live Dashboard]] orphan and quality sections to find gaps.

### 10. Follow the Methodology
Reference [[Investigation Methodology]] for standards and workflows.

## Common Tasks - Quick Guide

### How do I create a new person?
1. New note in `Entities/People/`
2. Insert `person-template`
3. Fill in details
4. Link and tag

### How do I find all high-priority targets?
- Check [[Entities MOC]] High Priority section
- Or: [[Live Dashboard]] Critical Threats section
- Or: Search `tag:#threat-critical`

### How do I track new evidence?
1. Create note with `evidence-entry-template`
2. Link to entities
3. Add to [[Evidence Repository]]
4. Update [[Timeline]] if significant

### How do I see what I worked on this week?
Check [[Live Dashboard]] "Modified This Week" section

### How do I find all information about a person?
1. Open person's note
2. Check linked entities, evidence, timeline
3. Or search: `content:"Person Name"`

### How do I track pending investigations?
[[Live Dashboard]] "Pending Verification" section

## Keyboard Shortcuts

- `Ctrl/Cmd + O`: Quick file switcher
- `Ctrl/Cmd + P`: Command palette
- `Ctrl/Cmd + F`: Search current file
- `Ctrl/Cmd + Shift + F`: Search all files
- `Ctrl/Cmd + K`: Insert link
- `Ctrl/Cmd + Click`: Open link in new pane

## Getting Help

### New to Obsidian?
- Check [[Quick Reference Guide]] for basics
- Review [[Investigation Methodology]] for workflows

### Need a Specific Search?
- Check [[Search Patterns]] for saved searches
- Use [[Quick Reference Guide]] for search syntax

### Want to Customize?
- Modify templates in `Templates/` folder
- Add custom Dataview queries to [[Live Dashboard]]
- Create new MOCs for specific focus areas

## Benefits Summary

| Before | After |
|--------|-------|
| Manual searching for entities | Instant access via MOCs |
| Inconsistent note formats | Standardized templates |
| Difficult to track relationships | Automatic link tracking |
| Manual evidence tracking | Structured evidence workflow |
| Static views | Dynamic Dataview dashboards |
| Time-consuming navigation | 2-click access to any area |
| Unclear search terms | Saved search patterns |
| No quality control | Automated quality checks |

## Next Steps

1. **Install Dataview plugin** (if not already installed)
2. **Review [[Quick Reference Guide]]** - Learn shortcuts
3. **Read [[Investigation Methodology]]** - Understand standards
4. **Start using templates** - Try creating a test note
5. **Bookmark the MOCs** - Quick access
6. **Review [[Live Dashboard]]** - See your data dynamically
7. **Update existing notes** - Gradually add tags and links

## Migration Tips

### For Existing Notes

You don't need to rewrite everything immediately:

1. **Start fresh**: Use templates for all new notes
2. **Gradual updates**: Add tags to existing notes over time
3. **Link as you go**: Add links when you revisit notes
4. **Priority first**: Update high-priority entity notes first
5. **Quality checks**: Use [[Live Dashboard]] to find notes needing updates

### Batch Updates

To quickly improve existing notes:
1. Add basic tags (threat, confidence, status)
2. Link to [[Investigation Dashboard]]
3. Link to relevant MOC
4. Cross-link related entities

## Questions?

Refer to:
- [[Quick Reference Guide]] - General usage
- [[Investigation Methodology]] - Standards and practices
- [[Search Patterns]] - Finding information
- [[Investigation Dashboard]] - Current investigations

---

**System created**: {{date}}
**Version**: 1.0
**Purpose**: Optimize investigation workflow for speed and thoroughness

Tags: #readme #documentation #guide #system
