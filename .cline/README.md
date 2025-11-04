# Cline Configuration for Obsidian Vault

This directory contains configuration and custom instructions for the Cline AI coding assistant.

## 📁 Directory Contents

- **config.json** - Project configuration with Google OAuth integration
- **custom-instructions.md** - Detailed instructions for AI assistance
- **README.md** - This file

## 🎯 Purpose

This configuration enables Cline to:

1. **Understand Project Context**
   - Investigation and research vault structure
   - Entity relationship mapping
   - Timeline and evidence organization

2. **Use Google APIs**
   - Access Google Drive for file backups
   - Query YouTube API for video analysis
   - OAuth authentication with pre-configured credentials

3. **Follow Project Conventions**
   - Markdown formatting standards
   - Note organization patterns
   - Cross-referencing with WikiLinks
   - Evidence documentation practices

## 🔧 Configuration Details

### Google OAuth Setup

**Client ID**: `988966010493-43du2fbcltpeuaet86398p962boak66u.apps.googleusercontent.com`

**Credentials Location**: `scripts/google-api/credentials.json`

**Authorized Scopes**:
- `https://www.googleapis.com/auth/drive` - Full Drive access
- `https://www.googleapis.com/auth/youtube.readonly` - Read YouTube data
- `https://www.googleapis.com/auth/youtube.force-ssl` - SSL-enforced access

### Project Structure

```
obsidian-vault/
├── .cline/                    # Cline configuration
├── scripts/google-api/        # API integration scripts
├── Entities/                  # Entity profiles
├── Analysis/                  # Research analysis
├── Patents/                   # Patent documentation
├── Technical/                 # Technical docs
├── INVESTIGATION_SUMMARY.md   # Main summary
├── ENTITY_NETWORK_MAP.md      # Relationship diagram
├── Timeline.md                # Event timeline
└── Evidence Repository.md     # Evidence catalog
```

## 🚀 Using Cline with This Project

### First Time Setup

1. **Install Cline Extension** (in VS Code)
   ```
   Extensions → Search "Cline" → Install
   ```

2. **Cline Will Automatically Load** this configuration when you open the project

3. **Authenticate APIs** (when needed)
   ```bash
   cd scripts/google-api
   python3 example_usage.py
   ```
   This will open a browser for OAuth authentication

### Common Use Cases

#### 1. Research YouTube Videos

Ask Cline:
> "Analyze this YouTube video: https://youtube.com/watch?v=VIDEO_ID"

Cline will use `scripts/google-api/review_video.py` to fetch detailed information.

#### 2. Backup Documents to Drive

Ask Cline:
> "Backup the investigation summary to Google Drive"

Cline will use the Drive API to upload and organize files.

#### 3. Add New Research Entities

Ask Cline:
> "Create a new entity profile for [Organization Name]"

Cline will create a properly formatted entity file and update relationship maps.

#### 4. Update Timeline

Ask Cline:
> "Add this event to the timeline: [event description] on [date]"

Cline will update Timeline.md with proper formatting.

#### 5. Organize Evidence

Ask Cline:
> "Add this evidence to the repository with source [URL]"

Cline will properly document evidence with citations.

## 📋 Custom Instructions Summary

Cline is configured to:

✅ Maintain consistent markdown formatting
✅ Update entity relationships automatically
✅ Keep timeline synchronized with events
✅ Properly cite sources and evidence
✅ Use Google APIs for research automation
✅ Follow git best practices
✅ Respect API quotas and rate limits
✅ Never commit sensitive token files

## 🔒 Security Notes

### Safe to Commit
- ✅ config.json (contains only OAuth client ID)
- ✅ custom-instructions.md (no secrets)
- ✅ This README

### Never Commit
- ❌ Any .env files in .cline/
- ❌ Token or session files
- ❌ API keys beyond OAuth client ID

The project's main .gitignore is configured to exclude sensitive files.

## 🛠️ Modifying Configuration

### Add New API Integration

1. Update `config.json`:
   ```json
   "apis": {
     "newApi": {
       "enabled": true,
       "scriptPath": "scripts/new-api/script.py"
     }
   }
   ```

2. Update `custom-instructions.md` with usage guidelines

3. Commit changes to repository

### Update OAuth Scopes

1. Edit `config.json` → `googleOAuth.scopes`
2. Delete token files: `rm scripts/google-api/*.pickle`
3. Re-authenticate: `python3 scripts/google-api/example_usage.py`

### Customize Instructions

Edit `custom-instructions.md` to add:
- Project-specific conventions
- New task templates
- Additional guidelines
- Code style preferences

## 📖 Documentation

For detailed API usage, see:
- `scripts/google-api/README.md` - Google API integration guide
- `INVESTIGATION_SUMMARY.md` - Project overview
- `Investigation Dashboard.md` - Central navigation

## 🔗 Related Resources

- [Cline Documentation](https://github.com/cline/cline)
- [Google Drive API Docs](https://developers.google.com/drive/api)
- [YouTube Data API Docs](https://developers.google.com/youtube/v3)
- [Obsidian Documentation](https://help.obsidian.md/)

## 💡 Tips

1. **Use Natural Language**: Ask Cline questions as if talking to a research assistant
2. **Reference Files**: Mention specific files by name for context
3. **Multi-step Tasks**: Break complex research into smaller steps
4. **API Awareness**: Cline knows about the integrated APIs and how to use them
5. **Context Preservation**: Custom instructions ensure consistent behavior

## 📞 Support

If Cline isn't following instructions:
1. Verify VS Code has the latest Cline extension
2. Check that `.cline/` directory is in the project root
3. Restart VS Code to reload configuration
4. Review custom-instructions.md for any conflicts

---

**Last Updated**: November 2025
**Configuration Version**: 1.0.0
**Project**: Obsidian Vault - Investigation & Research
