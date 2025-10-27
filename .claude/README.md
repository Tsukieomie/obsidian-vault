# Claude Code Integration Guide

This directory contains Claude Code integrations for the Obsidian investigation vault.

## Available Slash Commands

Claude Code slash commands are custom commands you can run by typing `/command-name` in your conversation with Claude.

### Entity Management

#### `/add-person`
Create a new person entity profile using the standardized template.
- Prompts for all necessary information
- Creates file in Entities/People/
- Updates Entity Index and Timeline
- Ensures consistent documentation

**Example**: `/add-person`

#### `/add-organization`
Create a new organization entity profile.
- Supports companies, nonprofits, government entities
- Captures registration information
- Links to key people
- Documents technical infrastructure

**Example**: `/add-organization`

#### `/add-infrastructure`
Create a new technical infrastructure profile (domains, networks, servers).
- Documents technical details (IPs, AS numbers, domains)
- Tracks registration information
- Records capabilities and IOCs
- Sets up monitoring status

**Example**: `/add-infrastructure`

### Investigation Workflows

#### `/investigation-session`
Start a guided investigation session with automatic documentation.
- Creates investigation note from template
- Guides you through the investigation process
- Documents findings in real-time
- Updates all relevant vault documents automatically
- Provides session summary at completion

**Example**: `/investigation-session`
**Use when**: Starting any new investigation work

#### `/search-entity`
Comprehensive search for any entity across the entire vault.
- Finds all mentions and references
- Compiles profile information
- Shows connections to other entities
- Lists related evidence
- Displays timeline entries
- Shows pending action items

**Example**: `/search-entity`
**Use when**: Need complete view of any person, org, or infrastructure

#### `/analyze-connection`
Analyze relationships between two or more entities.
- Maps direct and indirect connections
- Assesses connection strength and confidence
- Identifies connection type (family, business, technical)
- Generates connection diagrams
- Recommends verification steps

**Example**: `/analyze-connection`
**Use when**: Investigating relationships between entities

### Evidence & Tracking

#### `/update-evidence`
Update evidence tracking with new items or verification status.
- Add new evidence items
- Update verification status (verified/pending/investigating)
- Assess evidence quality
- Link to entities and sources
- Update Evidence Repository

**Example**: `/update-evidence`
**Use when**: Discovering new evidence or verifying existing evidence

### Analysis & Assessment

#### `/risk-assessment`
Perform comprehensive risk assessment using the Risk Matrix methodology.
- Uses Likelihood × Impact = Risk Score formula
- Assesses threats on 1-5 scales
- Calculates risk scores (1-25)
- Recommends mitigations
- Updates Risk Matrix document

**Example**: `/risk-assessment`
**Use when**: Evaluating new threats or updating existing risk assessments

### Reporting & Review

#### `/weekly-review`
Conduct comprehensive weekly investigation review.
- Reviews all Action Items progress
- Checks Evidence Tracking updates
- Summarizes Timeline discoveries
- Updates all analysis documents
- Generates weekly report
- Plans next week priorities

**Example**: `/weekly-review`
**Use when**: Weekly (recommended every 7 days)

#### `/export-report`
Generate comprehensive reports for external use.
- Executive summaries
- Legal reports (court-ready)
- Law enforcement reports
- Technical reports
- Entity-specific reports
- Full investigation reports

**Example**: `/export-report`
**Use when**: Need to share information with attorneys, law enforcement, or courts

## Command Usage

### Basic Usage
Simply type the slash command in your Claude Code conversation:

```
/add-person
```

Claude will then guide you through the process with prompts.

### Command Workflow Example

```
You: /investigation-session

Claude: I'll help you start a new investigation session. What are you investigating today?

You: I want to investigate the connection between Junyuan Wang and Intel

Claude: Great! I'll create an investigation note and guide you through this.
[Creates investigation note, asks for findings, documents evidence, etc.]

Claude: Session complete! Here's your summary:
- Investigation: Junyuan Wang Intel connection
- Key findings: 3 items documented
- Evidence: 2 new items added to tracking
- Next steps: 4 action items created
- Updated: Timeline, Evidence Tracking, Junyuan Wang profile
```

## Automation Scripts

### Coming Soon
- Automatic daily backups
- Evidence file organizer
- Graph visualization generator
- Connection strength calculator

## Integration Benefits

### Consistency
- All entities documented with same structure
- Templates automatically applied
- Standard formatting maintained

### Efficiency
- Guided workflows save time
- Automatic cross-document updates
- No manual navigation needed
- Reduced errors

### Completeness
- Commands ensure all relevant documents updated
- No forgotten cross-references
- Complete documentation trails
- Proper evidence tracking

### Analysis Support
- Built-in risk assessment methodology
- Connection analysis tools
- Evidence quality tracking
- Timeline maintenance

## Best Practices

### Daily Use
1. Start work with `/investigation-session`
2. Use entity commands as you discover new people/orgs/infrastructure
3. Use `/update-evidence` as you find or verify evidence
4. End session with automatic documentation

### Weekly Use
1. Run `/weekly-review` every 7 days
2. Review and update action items
3. Check evidence verification progress
4. Plan next week priorities

### As Needed
- `/search-entity` - When you need comprehensive entity view
- `/analyze-connection` - When investigating relationships
- `/risk-assessment` - When evaluating threats
- `/export-report` - When preparing for meetings or legal proceedings

### Investigation Workflow Pattern
```
Daily:
/investigation-session → [work] → automatic updates

Weekly:
/weekly-review → assess progress → plan next week

As Needed:
/search-entity → understand entity
/analyze-connection → understand relationships
/risk-assessment → understand threats
/export-report → share findings
```

## Command Development

### Creating New Commands

Commands are markdown files in `.claude/commands/` with:
- YAML frontmatter with description
- Detailed instructions for Claude
- Clear steps and workflows
- Examples and use cases

Example structure:
```markdown
---
description: Brief description of what this command does
---

Detailed instructions for Claude on how to execute this command.

Steps:
1. First step
2. Second step
3. etc.
```

### Command Ideas
Suggestions for additional commands:
- `/check-todos` - Review and update action items
- `/verify-source` - Verify evidence source credibility
- `/map-family` - Map family network relationships
- `/track-domain` - Set up domain monitoring
- `/update-confidence` - Recalculate connection confidence

## Technical Details

### File Locations
- Commands: `.claude/commands/*.md`
- This guide: `.claude/README.md`
- Vault root: `/home/user/obsidian-vault/`

### Document Integration
Commands automatically work with:
- Entity profiles (Entities/People/, Entities/Organizations/)
- Analysis documents (Analysis/)
- Technical profiles (Technical/)
- Templates (Templates/)
- Core documents (Timeline, Evidence Repository, Dashboard)

### Cross-References
Commands maintain proper wiki-link formatting:
- `[[Entity Name]]` for entity references
- `[[Document Name]]` for document references
- Proper tags: `#entity #person #organization #technical`

## Troubleshooting

### Command Not Found
- Ensure you're in the vault directory: `/home/user/obsidian-vault/`
- Check command exists: `ls .claude/commands/`
- Verify filename ends with `.md`

### Updates Not Reflecting
- Commands read current file state before updating
- Check file permissions
- Verify git status shows changes

### Getting Help
- Type the command to see Claude's prompts
- Check this README for command descriptions
- Review command file itself in `.claude/commands/`

## Future Enhancements

### Planned Features
1. **Hooks** - Automatic actions on file changes
2. **Scripts** - Python/shell automation
3. **Monitoring** - Automated infrastructure monitoring
4. **Backups** - Automatic evidence backup
5. **Visualizations** - Graph generation
6. **Alerts** - Risk threshold notifications

### Community Commands
Consider creating commands for:
- Your specific investigation workflows
- Custom reporting formats
- Specialized analysis techniques
- Integration with external tools

## Related Documentation

- [[Quick Start Guide]] - Vault getting started
- [[Templates]] - Template documentation
- [[Investigation Dashboard]] - Central command
- [[Analysis Index]] - Analysis documents

---

**Getting Started**: Type `/investigation-session` to begin your first guided investigation session!

---
Tags: #claude-code #integration #automation #commands #workflows
