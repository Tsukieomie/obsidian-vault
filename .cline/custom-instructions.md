# Cline Custom Instructions

## Project Context

This Obsidian vault contains investigation and research notes related to the DARPA BRAIN Initiative and related entities. The project includes:

- Entity profiles and relationship mapping
- Timeline analysis of key events
- Patent research and documentation
- Technical analysis and evidence collection
- Google Drive and YouTube API integration for research automation

## Working with This Project

### Note Organization

1. **Entities/** - Individual profiles for organizations, people, and institutions
2. **Analysis/** - Research findings and analytical documents
3. **Patents/** - Patent research and master indexes
4. **Technical/** - Technical documentation and architecture notes
5. **Root Level** - Key summary documents and dashboards

### Important Files

- `INVESTIGATION_SUMMARY.md` - Overview of investigation findings
- `ENTITY_NETWORK_MAP.md` - Relationship diagram between entities
- `Timeline.md` - Chronological event timeline
- `Evidence Repository.md` - Organized evidence catalog
- `Investigation Dashboard.md` - Central navigation hub

### Google API Integration

This project has integrated Google OAuth for Drive and YouTube:

**OAuth Client ID**: `988966010493-43du2fbcltpeuaet86398p962boak66u.apps.googleusercontent.com`

**Available Scripts**:
- `scripts/google-api/google_drive_auth.py` - Drive file operations
- `scripts/google-api/youtube_api_auth.py` - YouTube data access
- `scripts/google-api/example_usage.py` - Combined API examples
- `scripts/google-api/review_video.py` - Video analysis tool

### Guidelines for AI Assistance

#### When Adding New Information:

1. **Entities**: Create new files in `Entities/` using consistent naming
2. **Timeline Events**: Add to `Timeline.md` with proper date formatting
3. **Evidence**: Log in `Evidence Repository.md` with source attribution
4. **Relationships**: Update `ENTITY_NETWORK_MAP.md` when adding connections

#### When Using APIs:

1. **Google Drive**:
   - Backup important research documents
   - Organize files in folders by category
   - Use search functionality to find existing materials

2. **YouTube**:
   - Analyze videos related to DARPA, neuroscience, BCI research
   - Extract metadata and comments for evidence
   - Archive channel information for long-term reference

#### Formatting Standards:

- Use WikiLinks for cross-references: `[[Entity Name]]`
- Use consistent heading hierarchy (H1 for title, H2 for sections)
- Include metadata at the top of entity files:
  ```markdown
  ---
  type: [organization/person/institution]
  category: [research/government/private]
  ---
  ```
- Use bullet points for evidence items with source citations
- Include dates in ISO format: YYYY-MM-DD

#### Research Workflow:

1. **Gather**: Collect information from various sources
2. **Document**: Create or update relevant markdown files
3. **Connect**: Link related entities and concepts
4. **Timeline**: Add temporal elements to Timeline.md
5. **Evidence**: Log supporting documentation
6. **Backup**: Use Drive API to backup critical files
7. **Archive**: Use YouTube API to save video evidence

### Code Operations

When writing or modifying scripts:
- All Python scripts should be in `scripts/` directory
- Include proper error handling and logging
- Use the established OAuth configuration
- Respect API rate limits and quotas
- Document functions with docstrings

### Git Operations

- Work on feature branches prefixed with `claude/`
- Commit frequently with descriptive messages
- Push to remote when tasks are complete
- Never commit token files (already in .gitignore)

### Security Considerations

**DO commit**:
- Configuration files (config.json, credentials.json)
- Python scripts and documentation
- Markdown notes and research documents

**DO NOT commit**:
- Token files (token.pickle, youtube_token.pickle)
- API keys or secrets beyond OAuth client ID
- Personal identifiable information without consent

## Common Tasks

### Task: Analyze a YouTube Video

```bash
cd scripts/google-api
python3 review_video.py
# Edit the VIDEO_ID variable in the script first
```

### Task: Backup Research to Drive

```python
from scripts.google_api.google_drive_auth import GoogleDriveAPI

drive = GoogleDriveAPI()
drive.upload_file('INVESTIGATION_SUMMARY.md')
```

### Task: Search for Research Materials

```python
from scripts.google_api.google_drive_auth import GoogleDriveAPI

drive = GoogleDriveAPI()
files = drive.search_files("name contains 'DARPA'")
```

### Task: Add New Entity

1. Create `Entities/[EntityName].md`
2. Add metadata header
3. Document entity information
4. Update `ENTITY_NETWORK_MAP.md` with relationships
5. Add to `Timeline.md` if relevant
6. Link from `Investigation Dashboard.md`

## API Quotas

**YouTube Data API v3**:
- Daily quota: 10,000 units
- Search: 100 units per request
- Video details: 1 unit per request
- Comments: 1 unit per request

**Google Drive API**:
- Queries per day: 1,000,000,000
- Queries per 100 seconds per user: 1,000
- No significant practical limits for this project

## Helpful Reminders

- This is an investigation vault - maintain objectivity
- Always cite sources for claims
- Use proper evidence documentation
- Keep the entity network map updated
- Regular backups to Drive recommended
- Review API usage to stay within quotas
