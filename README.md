# Obsidian Investigation Vault

An Obsidian-based knowledge management system for documenting and organizing investigation research.

## Overview

This repository serves as a comprehensive investigation knowledge base built using [Obsidian](https://obsidian.md), containing research, analysis, and documentation related to network infrastructure investigations and technology research.

## Repository Structure

```
obsidian-vault/
├── Analysis/           # Investigation analysis documents
├── Entities/          # Entity profiles (people and organizations)
│   ├── Organizations/ # Organization profiles
│   └── People/        # Individual profiles
├── Patents/           # Patent research and documentation
├── Technical/         # Technical analysis and infrastructure reports
├── Welcome.md         # Vault entry point and navigation
└── Investigation Dashboard.md  # Central command center
```

## Getting Started

### Opening the Vault

1. Install [Obsidian](https://obsidian.md)
2. Clone this repository
3. Open Obsidian and select "Open folder as vault"
4. Navigate to the cloned repository directory

### Navigation

Start with these key documents:
- **[Welcome.md](Welcome.md)** - Main entry point with overview and quick links
- **[Investigation Dashboard.md](Investigation%20Dashboard.md)** - Central hub with current status
- **[INVESTIGATION_SUMMARY.md](INVESTIGATION_SUMMARY.md)** - Executive summary of findings

## Features

### Wiki-Style Linking
This vault uses Obsidian's wiki-style internal linking (`[[page name]]`) to create an interconnected knowledge graph. You can:
- Click on any `[[link]]` to navigate to that document
- Use the graph view to visualize connections
- Backlinks show where each document is referenced

### Organization

Documents are categorized by type:
- **Analysis/** - Deep-dive analysis and research findings
- **Entities/** - Profiles of people and organizations
- **Technical/** - Technical infrastructure and network analysis
- **Patents/** - Patent research and tracking

### Metadata

Documents include structured metadata:
- **Date** - Creation/update date
- **Status** - Current state (Active, Complete, etc.)
- **Classification** - Document type/importance
- **Priority** - Action priority level

## Automatic Sync

This vault is configured for automatic GitHub synchronization:
- Changes sync every 5 minutes via `.sync-vault.sh`
- Bidirectional sync (push and pull)
- See [SYNC_SETUP.md](SYNC_SETUP.md) for configuration details

## Key Documents

### Investigation Hub
- [Investigation Dashboard](Investigation%20Dashboard.md) - Central command center
- [Evidence Repository](Evidence%20Repository.md) - Evidence index
- [Timeline](Timeline.md) - Chronological discoveries

### Framework Documents
- [UNIFIED_EVIDENCE_FRAMEWORK.md](UNIFIED_EVIDENCE_FRAMEWORK.md) - Master investigation synthesis
- [LEGAL_CASE_FRAMEWORK.md](LEGAL_CASE_FRAMEWORK.md) - Legal documentation structure
- [ENTITY_NETWORK_MAP.md](ENTITY_NETWORK_MAP.md) - Entity relationship mapping

### Cross-References
- [CROSS_REFERENCE_INDEX.md](CROSS_REFERENCE_INDEX.md) - Complete navigation index

## Quality & Maintenance

For repository quality assessment and recommendations, see:
- [REPOSITORY_REVIEW.md](REPOSITORY_REVIEW.md) - Comprehensive quality review

## Contributing

This is a personal investigation vault. If you have access:
1. Make changes locally in Obsidian
2. Changes will auto-sync via the sync script
3. Or manually commit and push changes

## Technical Notes

### File Types
- `.md` - Markdown notes (main content)
- `.canvas` - Obsidian canvas files (visual organization)
- `.obsidian/` - Obsidian settings and configuration

### Exclusions
The following are excluded from version control (see `.gitignore`):
- Workspace files (prevent sync conflicts)
- Cache directories
- Log files (may contain sensitive paths)
- System files (`.DS_Store`, etc.)

## Privacy & Security

⚠️ **Important:**
- Log files are excluded from the repository
- Personal filesystem paths are not tracked
- Review the [REPOSITORY_REVIEW.md](REPOSITORY_REVIEW.md) for security recommendations

## License

Private investigation vault - not for public distribution.

---

**Last Updated:** 2025-11-17  
**Vault Version:** Obsidian-compatible  
**Status:** Active Investigation
