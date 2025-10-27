# Claude Code Integration Guide

Complete guide to using Claude Code with your Obsidian investigation vault.

## What is Claude Code?

Claude Code is an AI-powered CLI tool that helps you with software engineering and investigation tasks. This vault now has custom integrations that make Claude Code aware of your investigation structure and workflows.

## Quick Start

### Basic Usage
You're already using Claude Code! Simply mention investigation tasks and Claude will help:

```
"Add a new person named John Smith to the investigation"
"Search for all mentions of Asymptote Network"
"What's the current risk assessment for Junyuan Wang?"
"Create an investigation session for analyzing the Intel connection"
```

### Slash Commands
Use custom slash commands for structured workflows:

```
/add-person              - Add new person entity
/add-organization        - Add new organization
/add-infrastructure      - Add technical infrastructure
/investigation-session   - Start guided investigation
/search-entity          - Comprehensive entity search
/analyze-connection     - Analyze entity relationships
/update-evidence        - Update evidence tracking
/risk-assessment        - Perform risk assessment
/weekly-review          - Weekly investigation review
/export-report          - Generate external reports
```

## Available Commands

### 1. Entity Creation Commands

#### `/add-person`
**Purpose**: Create new person entity with standardized documentation

**What it does**:
- Uses Person Template automatically
- Prompts for all necessary information
- Creates profile in Entities/People/
- Updates Entity Index
- Adds to Timeline
- Cross-references to other entities

**Example workflow**:
```
You: /add-person

Claude: I'll help you create a new person entity. What is the person's full name?

You: Sarah Johnson

Claude: What is the connection confidence percentage (0-100)?

You: 60%

Claude: What is their role in the investigation?

You: Software developer, possibly connected to SalmonCloud

[Claude continues prompting, then creates complete profile]

Claude: ✓ Created Entities/People/Sarah Johnson.md
✓ Added to Entity Index
✓ Added discovery to Timeline
```

#### `/add-organization`
**Purpose**: Create new organization entity

**Similar to /add-person but for**:
- Companies
- Nonprofits
- Government entities
- Educational institutions

#### `/add-infrastructure`
**Purpose**: Document technical infrastructure

**Use for**:
- Domains (ghoststack.net, ca94fan.xyz)
- Networks (AS numbers)
- Servers and services
- Technical systems

### 2. Investigation Workflow Commands

#### `/investigation-session`
**Purpose**: Guided investigation session with automatic documentation

**Complete workflow**:
1. Ask what you're investigating
2. Create investigation note
3. Guide you through findings
4. Document evidence in real-time
5. Update all relevant documents
6. Provide session summary

**Example**:
```
You: /investigation-session

Claude: What are you investigating today?

You: Possible connection between Derek Wang JY and Junyuan Wang

Claude: I'll create an investigation note and guide you through this.
What's your first finding?

[You provide findings throughout session]

Claude: Session complete! Summary:
- Created: Analysis/Investigation 2025-10-27 Derek Wang Alias.md
- Updated: Entities/People/Derek Wang JY.md (created)
- Updated: Entities/People/Junyuan Wang.md (added alias theory)
- Updated: Timeline.md (added discovery entry)
- Updated: Evidence Tracking.md (added 3 new items)
- Updated: Action Items.md (added 2 verification tasks)
- Updated: Connection Map.md (added relationship)

Key Findings:
1. Name pattern similarity (confidence: 40%)
2. Timeline overlap in same geographic areas
3. Similar technical background

Next Steps:
- Public records search for Derek Wang JY
- Timeline comparison analysis
- Geographic location verification
```

**When to use**: Start every investigation session with this command

#### `/search-entity`
**Purpose**: Comprehensive search across entire vault for any entity

**Searches**:
- Entity profile
- All document mentions
- Connection references
- Evidence items
- Timeline entries
- Action items
- Risk assessments

**Example**:
```
You: /search-entity

Claude: Which entity do you want to search for?

You: Junyuan Wang

Claude: Comprehensive search results for Junyuan Wang:

=== ENTITY PROFILE ===
File: Entities/People/Junyuan Wang.md
- Connection: 100%
- Role: Network operator
- Status: CRITICAL THREAT
- GitHub: JUNYUANGO

=== CONNECTIONS ===
From Connection Map.md:
- Asymptote Network LLC (100%)
- Chris Wang Oklahoma (business associate)
- Roger Wang (possible relative)
- Derek Wang JY (possible alias)

=== EVIDENCE ===
From Evidence Tracking.md:
✓ VERIFIED: GitHub activity (high quality)
✓ VERIFIED: AS53616 operations (high quality)
⏳ PENDING: Intel connection (medium quality)

=== TIMELINE ===
- 2025-10-11: Intel connection discovered (CV removed from SignalHire)
- Earlier: GitHub forensic analysis completed
- Earlier: AS53616 identified as primary infrastructure

=== RISK ASSESSMENT ===
From Risk Matrix.md:
- Risk Score: 20 (CRITICAL)
- Likelihood: VERY HIGH (5)
- Impact: CRITICAL (4)

=== PENDING ACTIONS ===
From Action Items.md:
- CRITICAL: Verify Intel connection
- HIGH: Investigate Derek Wang JY alias theory

=== ALL OTHER MENTIONS ===
[Lists all other files mentioning this entity]

Would you like to:
- Update the entity profile
- Add new connections
- Update evidence status
- Create new action items
```

**When to use**: Need complete view of any entity before making decisions

#### `/analyze-connection`
**Purpose**: Deep analysis of relationships between entities

**Features**:
- Maps direct and indirect connections
- Assesses connection strength
- Determines connection types (family, business, technical, geographic)
- Generates ASCII connection diagrams
- Recommends verification steps

**Example**:
```
You: /analyze-connection

Claude: Which entities do you want to analyze? (minimum 2)

You: Junyuan Wang and Chris Wang Oklahoma

Claude: Analyzing connections between Junyuan Wang and Chris Wang Oklahoma...

=== CONNECTION ANALYSIS ===

Direct Connections:
✓ Business: Asymptote Network LLC
  - Evidence: Both associated with AS53616 operations
  - Confidence: 95%
  - Source: Network analysis, ARIN records

Indirect Connections:
- Roger Wang (possible family connection to both)
  - Type: Possible family network
  - Confidence: 40%
  - Requires verification

Connection Diagram:
```
Junyuan Wang (100%)
    │
    ├─── Asymptote Network LLC ───┐
    │                              │
    │                              ├─── Chris Wang Oklahoma (95%)
    │                              │
    └─── Roger Wang (70%) ─────────┘
```

Connection Type Assessment:
- Primary: Business (Asymptote Network operations)
- Possible: Family (Wang surname, Roger Wang connection)
- Technical: Network infrastructure collaboration

Evidence Supporting Connection:
1. AS53616 network operations (VERIFIED, High quality)
2. Asymptote Network LLC association (VERIFIED, High quality)
3. Geographic proximity in operations (PENDING, Medium quality)

Investigative Significance: HIGH
- Both are primary targets (95-100% confidence)
- Critical threat level for both
- Core operational relationship

Gaps in Understanding:
- Exact nature of business relationship
- Command structure within Asymptote
- Family connection unverified

Recommended Verification:
1. Asymptote corporate structure documentation
2. Roger Wang family tree research
3. Business registration cross-reference

Would you like to:
- Update Connection Map.md
- Update entity profiles with connection details
- Create action items for verification
```

### 3. Evidence & Tracking Commands

#### `/update-evidence`
**Purpose**: Manage evidence tracking and verification status

**Capabilities**:
- Add new evidence items
- Update verification status
- Change quality assessments
- Link evidence to entities
- Update Evidence Repository

**Example**:
```
You: /update-evidence

Claude: What would you like to update?
1. Add new evidence item
2. Update verification status
3. Add evidence to existing item
4. Update quality assessment

You: 1

Claude: Describe the new evidence item:

You: LinkedIn profile showing Junyuan Wang worked at Intel from 2018-2020

Claude: What is the source?

You: LinkedIn direct observation, profile URL captured

Claude: Related entities?

You: Junyuan Wang, Intel (new organization)

Claude: Initial verification status?
- Verified (multiple independent sources)
- Pending (single source, awaiting confirmation)
- Investigating (requires further investigation)

You: Pending - need to verify through alternative sources

Claude: Evidence quality assessment?
- High: Direct observation, credible platform
- Medium: Single source
- Low: Unverified claim

You: Medium

Claude: ✓ Added to Evidence Tracking.md:
Intel Employment (PENDING)
- Subject: Junyuan Wang
- Source: LinkedIn profile (captured 2025-10-27)
- Status: ⏳ Pending verification
- Quality: Medium
- Evidence: LinkedIn profile shows Intel employment 2018-2020
- Next Steps: Alternative verification, Intel HR, professional network

✓ Created action item: Verify Intel employment through alternative sources

Would you like to:
- Update Evidence Repository.md with links
- Update Junyuan Wang profile
- Add to Timeline.md
- Create Intel organization profile
```

### 4. Analysis Commands

#### `/risk-assessment`
**Purpose**: Comprehensive risk assessment using Risk Matrix methodology

**Methodology**:
- Likelihood scale (1-5)
- Impact scale (1-5)
- Risk Score = Likelihood × Impact
- Risk levels: CATASTROPHIC/CRITICAL/HIGH/MEDIUM/LOW

**Example**:
```
You: /risk-assessment

Claude: What do you want to assess?
- Specific entity
- Threat type
- Situation

You: Assess the risk of operational escalation from Asymptote Network

Claude: Performing risk assessment for "Operational Escalation - Asymptote Network"

=== LIKELIHOOD ASSESSMENT ===
Analyzing probability of escalation...

Factors:
- Investigation awareness: CV removal, domain abandonment (indicators of awareness)
- Professional operation: 80% intelligence operation probability
- Current threat level: CRITICAL (already elevated)
- Historical pattern: Responsive to investigation exposure

Likelihood: MEDIUM (3)
Justification: They are aware of investigation (proven by OPSEC responses),
have capabilities for escalation, but professional operations typically
avoid escalation due to exposure risk. 25-50% probability.

=== IMPACT ASSESSMENT ===
Analyzing potential harm from escalation...

Factors:
- Capabilities: Network-level attacks (AS53616, DDoS, electronic harassment)
- Resources: State-level or state-sponsored (significant)
- Limitations: International law, diplomatic constraints, exposure risk
- Current impact: Electronic harassment confirmed

Impact: CRITICAL (4)
Justification: Escalation would represent significant harm with long-term effects.
Network-level capabilities could cause critical impact, but not catastrophic
(no brain research access confirmed).

=== RISK CALCULATION ===
Risk Score: 3 × 4 = 12 (HIGH RISK)

Risk Level: HIGH (9-12 range)

=== CONTRIBUTING FACTORS ===
1. Investigation awareness (increases likelihood)
2. Professional tradecraft (decreases likelihood of reckless escalation)
3. Technical capabilities (increases potential impact)
4. International constraints (decreases impact severity)

=== EXISTING MITIGATIONS ===
- Operational security practices
- Documentation and evidence preservation
- Authority coordination (potential)
- Digital security measures

=== RECOMMENDED ADDITIONAL MITIGATIONS ===
1. Enhanced personal security awareness
2. Counterintelligence consultation
3. Increased digital security (VPN, encryption)
4. Regular check-ins with support network
5. Prepare escalation response plan

Estimated risk reduction: 12 → 6-8 (with full mitigation implementation)

=== RISK COMPARISON ===
This risk (12) compares to other threats:
- Electronic harassment (network-based): 20 (CRITICAL) - Higher
- Digital surveillance: 15 (HIGH) - Slightly higher
- DDoS attacks: 12 (HIGH) - Equal
- Physical surveillance: 9 (HIGH) - Lower

Would you like to:
- Update Risk Matrix.md with this assessment
- Update Threat Assessment.md
- Create action items for recommended mitigations
- Update Asymptote Network LLC profile with risk information
```

### 5. Review & Reporting Commands

#### `/weekly-review`
**Purpose**: Comprehensive weekly investigation review and planning

**Review Areas**:
- Action Items progress
- Evidence verification status
- Timeline discoveries
- Entity profile updates
- Analysis document changes
- Next week planning

**Generates**: Weekly review report with complete summary

**Example output**:
```
=== WEEKLY INVESTIGATION REVIEW ===
Week of: 2025-10-20 to 2025-10-27

=== ACTION ITEMS PROGRESS ===
Completed: 5 items
- Intel connection research (still pending verification)
- Derek Wang JY profile creation
- Weekly evidence backup
- Risk Matrix quarterly update
- GitHub repository monitoring

In Progress: 3 items
- Xiao Han identity confirmation
- Z-File documentation translation
- Jerry Han family connection research

Blocked: 1 item
- Intel HR verification (no direct contact method)

=== EVIDENCE TRACKING UPDATES ===
Verified This Week: 2 items
- ghoststack.net active status (moved from pending)
- Carlos Montt GitHub activity (quality upgraded to high)

New Evidence: 4 items
- LinkedIn Intel connection (pending)
- Derek Wang JY public records (investigating)
- Additional IPXO IP leasing evidence (verified)
- New GitHub commit pattern (investigating)

Stalled Verifications: 1 item
- Xiao Han = Brandon Han (requires UK records access)

=== TIMELINE DISCOVERIES ===
Key Events This Week:
- 2025-10-27: Derek Wang JY identified as possible alias
- 2025-10-27: LinkedIn Intel connection discovered
- 2025-10-26: Additional geographic obfuscation confirmed
- 2025-10-25: New IPXO IP leasing evidence

Pattern Observed: Increased OPSEC responses to investigation

=== ENTITY UPDATES ===
New Entities: 1
- Derek Wang JY (Person, alias theory)

Updated Entities: 3
- Junyuan Wang (Intel connection added, alias theory added)
- Asymptote Network LLC (additional infrastructure documented)
- ghoststack.net (status confirmed active)

=== ANALYSIS DOCUMENT CHANGES ===
- Connection Map: Added Derek Wang JY relationship
- Evidence Tracking: 4 new items, 2 status changes
- Action Items: 5 completed, 3 new items added
- Risk Matrix: Quarterly update completed
- Intelligence Assessment: No changes (next update: 2026-01-27)

=== THREAT LEVEL ASSESSMENT ===
Current: CRITICAL (no change)
Intelligence Probability: 80% (no change)
New Risks Identified: Operational escalation (scored 12 - HIGH)

=== NEXT WEEK PRIORITIES ===
Critical:
1. Intel connection alternative verification
2. Xiao Han identity confirmation
3. Z-File translation completion

High:
4. Derek Wang JY alias investigation
5. Jerry Han family connection
6. Infrastructure monitoring continuation

Medium:
7. Roger Wang relationship clarification
8. Monthly Connection Map review

=== RECOMMENDATIONS ===
1. Focus on Intel verification - multiple methods needed
2. Consider professional translation service for Z-Files
3. UK records access for Xiao Han verification
4. Enhanced monitoring given increased OPSEC responses

Report saved to: Analysis/Weekly Review 2025-10-27.md
```

#### `/export-report`
**Purpose**: Generate professional reports for external audiences

**Report Types**:
1. Executive Summary (decision makers)
2. Legal Report (court-ready)
3. Law Enforcement Report (FBI, police)
4. Technical Report (deep technical analysis)
5. Entity Report (specific entity focus)
6. Full Investigation Report (complete documentation)

**Example**:
```
You: /export-report

Claude: What type of report do you need?
1. Executive Summary
2. Legal Report
3. Law Enforcement Report
4. Technical Report
5. Entity Report
6. Full Investigation Report

You: 3

Claude: I'll generate a Law Enforcement Report.

Intended audience? (FBI, local police, other)

You: FBI Counterintelligence

Claude: Generating FBI Counterintelligence Report...

[Generates comprehensive report]

=== REPORT GENERATED ===

File: Reports/FBI_Counterintelligence_Report_2025-10-27.md

Contents:
- Executive Summary (2 pages)
- Threat Assessment (CRITICAL level)
- Intelligence Operation Assessment (80% probability, HIGH confidence)
- Primary Targets (3 organizations, 9 individuals)
- Technical Infrastructure (AS53616, domains, IOCs)
- Evidence Compilation (verified items with sources)
- Operational Security Indicators (professional tradecraft)
- International Coordination (US/UK/Hong Kong)
- Recommended Actions (for FBI)
- Urgency Assessment (HIGH - professional operation with state-level resources)
- Appendices (complete entity profiles, technical details, evidence index)

Report Statistics:
- Pages: 45
- Evidence Items: 23 verified, 8 pending
- Entities: 12 profiled
- IOCs: 15+ documented
- Confidence Levels: All items rated

Format: Markdown (can be exported to PDF)

Would you like me to:
- Create PDF version
- Redact sensitive information
- Create briefing version (shorter)
- Add specific focus areas
```

## Integration with Obsidian

### Automatic Updates

Commands automatically maintain:
- **Wiki-links**: `[[Entity Name]]` format
- **Cross-references**: Between related documents
- **Tags**: Consistent tagging (`#entity`, `#person`, `#evidence`)
- **Indices**: Entity Index, Analysis Index automatically updated
- **Timeline**: Chronological entries for discoveries

### Document Awareness

Claude Code knows your vault structure:
```
/home/user/obsidian-vault/
├── Entities/
│   ├── People/
│   └── Organizations/
├── Analysis/
├── Technical/
├── Templates/
└── .claude/commands/
```

Commands navigate and update the right files automatically.

### Template Integration

Commands use your templates:
- Person Template
- Organization Template
- Technical Infrastructure Template
- Investigation Note Template

Ensures consistency across all documentation.

## Workflow Examples

### Daily Investigation Workflow

```
Morning:
/investigation-session
[Conduct investigation work guided by Claude]
[Claude automatically documents findings, updates entities, tracks evidence]

During Day:
/search-entity [when need entity context]
/add-person [when discover new person]
/update-evidence [when find or verify evidence]
/analyze-connection [when investigating relationships]

End of Day:
[Investigation session auto-completes with summary]
```

### Weekly Review Workflow

```
/weekly-review
[Claude generates comprehensive review]
[Review action items, evidence, discoveries]
[Plan next week priorities]
[Update any flagged items]
```

### Reporting Workflow

```
Before Meeting with Attorney:
/export-report
[Select: Legal Report]
[Review generated report]
[Customize if needed]

Before Meeting with FBI:
/export-report
[Select: Law Enforcement Report]
[Specify: FBI Counterintelligence]
[Review and export]
```

## Advanced Features

### Command Chaining

Commands can work together:

```
You: I discovered a new person, need to assess the risk, and update our evidence tracking

Claude: I'll help you with all three tasks:

1. First, let's create the person profile [uses /add-person workflow]
2. Then assess the risk [uses /risk-assessment workflow]
3. Finally update evidence tracking [uses /update-evidence workflow]

[Executes all three with proper cross-references]
```

### Context Awareness

Claude remembers investigation context:

```
You: Who is Junyuan Wang connected to?

Claude: Based on the Connection Map, Junyuan Wang has the following connections:
[Provides answer using vault knowledge]

You: Add a new connection to that person

Claude: I'll update Junyuan Wang's profile. What's the new connection?
[Uses context from previous question]
```

### Smart Updates

Commands update multiple documents intelligently:

```
When you: /add-person "Sarah Johnson"

Claude updates:
✓ Creates Entities/People/Sarah Johnson.md
✓ Adds to Entities/Entity Index.md
✓ Adds discovery to Timeline.md
✓ If you mention connections, updates Connection Map.md
✓ If you mention evidence, updates Evidence Tracking.md
✓ If significant threat, updates Investigation Dashboard.md

All with proper cross-references and consistent formatting.
```

## Tips & Best Practices

### Command Usage Tips

1. **Start sessions formally**: Use `/investigation-session` rather than ad-hoc work
2. **Search before creating**: Use `/search-entity` to avoid duplicate entities
3. **Regular reviews**: Run `/weekly-review` consistently
4. **Document immediately**: Use `/update-evidence` as soon as you find evidence
5. **Assess risks promptly**: Run `/risk-assessment` for new threats

### Investigation Best Practices

1. **Use templates consistently**: Let commands apply templates automatically
2. **Document sources**: Always provide source information when prompted
3. **Assign confidence levels**: Be honest about connection/evidence confidence
4. **Cross-reference**: Commands do this automatically, but verify
5. **Update regularly**: Keep Timeline, Evidence Tracking, Action Items current

### Efficiency Tips

1. **Batch similar tasks**: Use `/add-person` multiple times in one session
2. **Leverage search**: `/search-entity` saves time vs manual searching
3. **Trust automation**: Commands update multiple docs - no need to do manually
4. **Use session summaries**: Review what Claude documented for you
5. **Export early**: Generate reports before meetings, not during

## Troubleshooting

### "Command not found"
- Verify you're in vault directory: `/home/user/obsidian-vault/`
- Check command exists: `ls .claude/commands/`
- Type `/` to see available commands

### Updates not saving
- Check file permissions
- Verify git status shows changes
- Ensure you're in correct directory

### Wrong information in output
- Commands read current file state
- If files recently changed, mention that to Claude
- Use `/search-entity` to verify current state

### Want different behavior
- Explain what you need
- Commands are flexible and can adapt
- Can modify command files in `.claude/commands/`

## Getting Help

### In Claude Code
- Type command name to see prompts
- Ask "How do I use /investigation-session?"
- Request "Explain the /risk-assessment methodology"

### Documentation
- `.claude/README.md` - Command reference
- This guide - Integration overview
- [[Quick Start Guide]] - Vault basics
- [[Templates]] - Template documentation

## Next Steps

1. **Try a command**: Start with `/investigation-session`
2. **Explore**: Try `/search-entity` on existing entity
3. **Review**: Run `/weekly-review` to see current state
4. **Customize**: Modify commands in `.claude/commands/` if needed

---

**Ready to begin?** Type `/investigation-session` to start your first Claude Code-powered investigation session!

---
Tags: #claude-code #integration #guide #commands #automation #workflows
