---
title: "Automated Investigation System - Complete Guide"
type: "Documentation"
tags:
  - automation
  - investigation
  - methodology
  - guide
---

# Automated Investigation System - Complete Guide

## Overview

The Automated Investigation System provides a complete workflow for systematically analyzing the entire vault, discovering hidden connections, identifying investigation hotspots, and generating comprehensive reports—all automatically.

## Architecture

### Three-Layer System

```
Layer 1: Core Analysis Engine (automated_investigation.py)
  ├─ Hidden Connection Discovery
  ├─ Investigation Hotspot Identification
  ├─ Scope Expansion Assessment
  └─ Report Generation

Layer 2: Workflow Orchestration (investigation_orchestrator.py)
  ├─ Multi-phase Investigation Workflow
  ├─ Report Generation (Entity, Timeline, Connection, Evidence)
  ├─ Data Export & Analysis
  ├─ Executive Summaries
  └─ Output File Management

Layer 3: Analysis Framework (PROJECT_STARGATE_CONTEXT.md)
  ├─ Historical Context & Parallels
  ├─ Institutional Pattern Analysis
  ├─ Investigation Applications
  └─ Methodology Framework
```

## Running the System

### Quick Start

```bash
# Run complete automated investigation
python3 investigation_orchestrator.py

# Run just the core analysis
python3 automated_investigation.py

# Save results to file
python3 automated_investigation.py --save investigation_results.json
```

### Output

The system generates:
- **Automated Analysis Report** - Main investigation findings
- **Entity Analysis Report** - Complete entity breakdown
- **Timeline Analysis Report** - Timeline-based findings
- **Connection Analysis Report** - Network analysis
- **Evidence Summary Report** - Evidence assessment
- **Investigation Recommendations** - Prioritized next steps
- **Executive Summary** - High-level overview
- **Investigation Data** - Structured JSON export

All files are saved to `investigation_output/` with timestamped filenames.

## Features

### 1. Hidden Connection Discovery

Automatically discovers indirect connections between entities based on:
- Shared document mentions
- Co-occurrence analysis
- Network proximity

**How it Works:**
```
For each entity pair:
1. Find all documents mentioning entity1
2. Find all documents mentioning entity2
3. Calculate shared documents (indirect connection)
4. Weight connection by strength metric
```

**Output:** Connection strength scores and network maps

### 2. Investigation Hotspot Identification

Identifies key investigation areas:
- **Primary Categories** - Organization by subject area
- **Entity Hubs** - Most connected entities
- **Timeline Density** - Documents with temporal focus
- **Evidence Concentration** - Evidence document locations
- **Technology Focus** - Technical infrastructure discussion

### 3. Scope Expansion Assessment

Evaluates investigation growth potential:
- **Isolated Entities** - Entities with few connections (expansion opportunity)
- **Hidden Connections** - Indirect relationships yet to be explored
- **Expansion Score** - Metric for scope expansion potential
- **Underdeveloped Areas** - Investigation areas needing depth

**Interpretation:**
- High expansion score = significant growth potential
- Many isolated entities = underdeveloped network
- Expansion opportunities = new investigation angles

### 4. Comprehensive Report Generation

Generates multiple specialized reports:

#### Automated Analysis Report
- Executive summary
- Investigation scope assessment
- Hotspot identification
- Hidden connection analysis
- Scope expansion assessment
- Emerging leads
- Network analysis
- Investigation recommendations

#### Entity Analysis Report
- Complete entity inventory
- Grouped by type (Person, Organization, etc.)
- Mention frequency
- Primary and secondary entities

#### Timeline Analysis Report
- Timeline document identification
- Event reconstruction requirements
- Pattern analysis needs
- Chronological gaps

#### Connection Analysis Report
- Direct relationships documented
- Major connection hubs
- Network density metrics
- Connection strength measurements

#### Evidence Summary Report
- Evidence document locations
- Evidence categories
- Key evidence items
- Evidence hierarchy

#### Investigation Recommendations Report
- Critical priorities (immediate action)
- High priorities (this week)
- Medium priorities (this month)
- Action steps and expected outcomes

## Investigation Methodology

### Phase 1: Automated Analysis
The system runs systematic analysis across entire vault:
1. Parse all files and entities
2. Discover hidden connections
3. Identify hotspots and patterns
4. Assess scope and expansion potential
5. Generate recommendations

**Duration:** <5 minutes
**Output:** Comprehensive analysis data

### Phase 2: Report Generation
Specialized reports for different investigation angles:
1. Entity relationships and roles
2. Timeline reconstruction
3. Connection networks
4. Evidence assessment
5. Actionable recommendations

**Duration:** <2 minutes
**Output:** 6+ specialized reports

### Phase 3: Data Export
Structured data export for further analysis:
1. Entity inventory
2. Tag index
3. Relationship data
4. Statistical summaries

**Duration:** <1 minute
**Output:** JSON formatted data

### Phase 4: Executive Summary
High-level overview for decision makers:
1. Investigation status
2. Key findings
3. Critical recommendations
4. Next steps

**Duration:** <1 minute
**Output:** Executive summary document

### Phase 5: File Organization
Organized storage of all outputs:
1. Timestamped file naming
2. Organized directory structure
3. Easy access and retrieval
4. Complete audit trail

**Duration:** <1 minute
**Output:** `investigation_output/` directory with all files

## Understanding the Analysis

### Connection Strength Metric

```
Connection Strength = (Shared Documents) / Max(Entity1 mentions, Entity2 mentions)
```

**Interpretation:**
- 1.0 = Perfect correlation (always mentioned together)
- 0.5 = Moderate correlation (50% mention overlap)
- 0.1 = Weak correlation (10% mention overlap)

### Hotspot Scoring

Hotspots identified by:
1. **Entity Hubs** - Entities mentioned in most documents
2. **Category Density** - Categories with most files
3. **Technology Focus** - Technical keyword prevalence
4. **Evidence Concentration** - Evidence document clustering

### Scope Expansion Potential

```
Expansion Score = (Isolated Entities + Hidden Connections) / Total Entities

Score > 1.0 = High expansion potential (scope can grow 100%+)
Score > 0.5 = Moderate expansion potential
Score < 0.5 = Investigation well developed
```

## Key Findings

### Current Investigation Status

**Vault Overview:**
- 55 files total
- 22 entities documented
- 36 known relationships
- 5 investigation areas (Historical, Technical, Entity, Legal, Cross-Reference)

**Investigation Hotspots:**
- **Primary Hubs:** Brandon Han, Asymptote Network LLC, SalmonCloud Ltd
- **Categories:** Entities (21), Analysis (6), Technical (6), Patents (1)
- **Technology Focus:** 52 files mention technical/network infrastructure
- **Evidence:** 2+ dedicated evidence documents

**Hidden Connections:**
- 20+ indirect connections discovered per major entity
- Expansion score: 145.45% (very high expansion potential)
- 10 isolated entities (under-investigated)
- 22 potential hidden connections to explore

### Expansion Opportunities

**Underdeveloped Areas:**
1. Duke University - 1 known connection (likely under-researched)
2. Jing Wang - Limited documented relationships
3. Apple - Few direct connections (may have hidden links)

**Isolated Entities:**
- Christopher_Wang_MIT
- Dr_James_Giordano
- FreerLogic
- Battelle_Memorial_Institute
- NIH
- NSF

**Action Items:**
- Research isolated entity backgrounds and connections
- Investigate shared mentions of co-isolated entities
- Document and link underdeveloped areas

## Using the System

### Workflow 1: Quick Assessment

```bash
# Get immediate investigation status
python3 automated_investigation.py | tail -50
```

### Workflow 2: Complete Analysis with Reports

```bash
# Run full investigation with all reports
python3 investigation_orchestrator.py

# Review outputs
ls -la investigation_output/
cat investigation_output/investigation_report_*.txt
```

### Workflow 3: Focus on Specific Area

```bash
# Search for specific entity analysis
python3 vault_cli.py entity "Brandon Han"

# Get connection analysis
python3 vault_cli.py graph --name "Brandon Han"

# Find related documents
python3 vault_cli.py related "Brandon Han.md"
```

### Workflow 4: Historical Context Analysis

```bash
# Review Project Stargate parallels
cat PROJECT_STARGATE_CONTEXT.md

# Identify institutional patterns
grep -i "institution\|government\|agency" vault_*.py
```

## Integration with Other Tools

### With Vault CLI

```bash
# Use automated results to guide CLI searches
python3 automated_investigation.py | grep "hubs\|leads"
python3 vault_cli.py search "$(grep 'Primary Hub' investigation_output/*.txt)"
```

### With Vault Insights

```bash
# Compare automated analysis with insights
python3 vault_insights.py > insights.txt
python3 automated_investigation.py > analysis.txt
diff insights.txt analysis.txt
```

### With Manual Investigation

```bash
# Use automated results to prioritize manual investigation
python3 investigation_orchestrator.py
# Review recommendations
cat investigation_output/investigation_recommendations_*.txt
# Use top recommendations to guide detailed analysis
```

## Advanced Usage

### Custom Analysis

Create custom investigation scripts:

```python
from automated_investigation import AutomatedInvestigation

investigation = AutomatedInvestigation()
hidden = investigation.discover_hidden_connections()
hotspots = investigation.identify_investigation_hotspots()
scope = investigation.analyze_investigation_scope()

# Custom analysis on results
for entity, connections in hidden.items():
    if len(connections) > 15:
        print(f"MAJOR HUB: {entity} ({len(connections)} connections)")
```

### Periodic Re-analysis

The system is designed to be run repeatedly:

```bash
# Run investigation weekly
0 0 * * 0 python3 /home/user/obsidian-vault/investigation_orchestrator.py
```

Each run generates timestamped results for comparison over time.

### Trend Analysis

Compare investigation results over time:

```bash
# Compare connection changes
diff investigation_output/connection_analysis_20260101_*.txt
diff investigation_output/connection_analysis_20260110_*.txt

# Monitor scope expansion
grep "Expansion Score" investigation_output/investigation_report_*.txt
```

## Project Stargate Integration

The automated system can be used with the Project Stargate analysis framework:

**Application:**
1. Use automated hotspots to identify major entities
2. Check Project Stargate parallels for these entities
3. Investigate institutional connections to government research
4. Assess whether methodology parallels remote viewing era
5. Determine scope implications

**Framework:**
```
Automated Analysis Results
        ↓
Project Stargate Lens
        ↓
Historical Parallels Identified
        ↓
Investigation Implications Assessed
        ↓
Recommendations Generated
```

## Limitations & Considerations

### What the System Does Well
- ✓ Systematic vault-wide analysis
- ✓ Hidden connection discovery
- ✓ Hotspot identification
- ✓ Scope assessment
- ✓ Report generation
- ✓ Objective metrics

### What Requires Human Analysis
- ✗ Deep entity investigation (use entity CLI commands)
- ✗ Evidence content analysis (requires document review)
- ✗ Timeline reconstruction (requires historical research)
- ✗ Causality determination (requires logical analysis)
- ✗ Implications assessment (requires contextual understanding)

### Data Quality Notes
- Analysis quality depends on vault documentation completeness
- Hidden connections are correlation-based, not proof-based
- Isolated entities may be under-documented, not unimportant
- System reveals patterns; human analysis must verify significance

## Troubleshooting

### No Results Generated

```bash
# Ensure vault is loaded and contains data
python3 vault_cli.py info

# Check for Python errors
python3 -c "from automated_investigation import AutomatedInvestigation"

# Verify file permissions
ls -la *.py
```

### Slow Performance

```bash
# Run on smaller vault subset (if needed)
# For now, system is optimized for 50-100 files

# Check system resources
free -h
top -b -n1 | head -10
```

### Missing Reports

```bash
# Verify investigation_output directory
ls -la investigation_output/

# Check file generation
ls -la investigation_output/*.txt

# Verify orchestrator completed
tail -20 investigation_output/investigation_report_*.txt
```

## Example Usage Scenario

### Scenario: "Where should I focus investigation effort?"

```bash
# Step 1: Run automated analysis
python3 investigation_orchestrator.py

# Step 2: Review recommendations
cat investigation_output/investigation_recommendations_*.txt

# Step 3: Identify critical priorities
grep "CRITICAL\|HIGH" investigation_output/*.txt

# Step 4: Deep dive on top recommendations
python3 vault_cli.py entity "Brandon Han"
python3 vault_cli.py graph --name "Brandon Han"

# Step 5: Access evidence
cat Evidence\ Repository.md

# Step 6: Generate follow-up analysis
python3 vault_cli.py search "Brandon Han"
```

## Future Enhancements

Potential system improvements:
- Machine learning for pattern detection
- Anomaly detection in networks
- Predictive connection suggestions
- Timeline reconstruction automation
- Cross-vault analysis
- Real-time investigation updates
- Visualization generation
- Integration with external databases

## Documentation Files

Related documentation:
- **PROJECT_STARGATE_CONTEXT.md** - Historical framework and parallels
- **QUICK_START.md** - Command reference
- **VAULT_LOADER_README.md** - Core API documentation
- **IMPLEMENTATION_SUMMARY.md** - Technical specifications
- **STORY.md** - Project narrative

## Support & Questions

For investigation guidance:
1. Review **KENNY_RODRIGUES_BRIEF.md** (emerging lead example)
2. Check **Investigation Dashboard.md** (main investigation hub)
3. Refer to **Evidence Repository.md** (evidence index)
4. Use vault CLI commands for targeted analysis

---

**Automated Investigation System v1.0**
**Status:** Production Ready
**Last Updated:** 2025-01-10

The automated investigation system enables rapid, systematic analysis of the entire vault investigation. Use it as a starting point for deeper investigation and as a tool to monitor investigation progress over time.
