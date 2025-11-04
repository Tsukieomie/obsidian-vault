# Cline Quick Start Guide

Get started with Cline AI assistant in this Obsidian vault.

## ⚡ 5-Minute Setup

### 1. Install Cline (if not already installed)

**In VS Code:**
1. Press `Ctrl+Shift+X` (or `Cmd+Shift+X` on Mac)
2. Search for "Cline"
3. Click Install
4. Reload VS Code

### 2. Open This Project

```bash
code /path/to/obsidian-vault
```

Cline will automatically detect the `.cline/` configuration.

### 3. Authenticate Google APIs (First Time Only)

```bash
cd scripts/google-api
pip install -r requirements.txt
python3 example_usage.py
```

A browser will open for OAuth authentication. Sign in and grant access.

### 4. Start Using Cline

Open Cline panel in VS Code (usually on the left sidebar) and start asking questions!

## 🎯 Example Prompts

### Research Tasks

**Analyze a YouTube video:**
```
Analyze this YouTube video and extract key information:
https://youtube.com/watch?v=VIDEO_ID
```

**Add a new research entity:**
```
Create a new entity profile for "Organization Name"
with the following information: [details]
```

**Update the timeline:**
```
Add this event to the timeline:
"DARPA announces BRAIN Initiative" on 2013-04-02
```

### File Operations

**Backup to Google Drive:**
```
Backup these files to Google Drive:
- INVESTIGATION_SUMMARY.md
- ENTITY_NETWORK_MAP.md
```

**Search Drive for documents:**
```
Search Google Drive for documents containing "neuroscience"
```

**Organize research:**
```
Review the Analysis/ folder and create a master index
of all research documents
```

### Content Creation

**Create entity relationship map:**
```
Based on the entities in Entities/, update the
ENTITY_NETWORK_MAP.md to show all connections
```

**Generate summary:**
```
Create a summary of all entities related to
"DARPA BRAIN Initiative"
```

**Consolidate evidence:**
```
Review Evidence Repository.md and organize evidence
by category with proper citations
```

## 🔧 Common Workflows

### Workflow 1: Video Research Pipeline

```
1. "Analyze this YouTube video: [URL]"
2. "Extract the key claims and timestamps"
3. "Add relevant information to Evidence Repository"
4. "Update any related entity profiles"
5. "Backup the analysis to Google Drive"
```

### Workflow 2: Entity Deep Dive

```
1. "Create a new entity profile for [Name]"
2. "Search Google Drive for existing materials about [Name]"
3. "Add connections to ENTITY_NETWORK_MAP.md"
4. "Update Timeline.md with relevant dates"
5. "Generate a relationship summary"
```

### Workflow 3: Evidence Organization

```
1. "Review all evidence in Evidence Repository.md"
2. "Categorize by: documents, videos, patents, articles"
3. "Add missing citations"
4. "Cross-reference with entity profiles"
5. "Create an evidence summary report"
```

### Workflow 4: Documentation Backup

```
1. "List all main documentation files"
2. "Check last backup date for each"
3. "Upload updated files to Google Drive"
4. "Create backup manifest with timestamps"
```

## 🎨 Cline Features You Can Use

### Contextual Understanding

Cline knows about:
- ✅ Project structure and organization
- ✅ Google API integration and scripts
- ✅ Markdown formatting conventions
- ✅ Entity relationships and network mapping
- ✅ Investigation workflow and best practices

### Automated Tasks

Cline can automatically:
- ✅ Format markdown consistently
- ✅ Update cross-references and WikiLinks
- ✅ Maintain timeline chronology
- ✅ Cite sources properly
- ✅ Organize evidence by category
- ✅ Backup files to Google Drive
- ✅ Analyze YouTube videos with API

### Code Execution

Cline can run:
- ✅ Python scripts in `scripts/google-api/`
- ✅ Shell commands for git operations
- ✅ API calls to Drive and YouTube
- ✅ File search and organization tasks

## 📚 Pro Tips

### 1. Be Specific

❌ "Update the timeline"
✅ "Add this event to Timeline.md: DARPA BRAIN Initiative launched on 2013-04-02"

### 2. Reference Files

❌ "Update the entity"
✅ "Update Entities/DARPA.md to include this new information"

### 3. Multi-Step Tasks

✅ "Search YouTube for DARPA BRAIN videos, analyze the top 3,
   and create entity profiles for any new organizations mentioned"

### 4. Use Context

✅ "Based on the ENTITY_NETWORK_MAP.md, which entities are
   most connected to DARPA?"

### 5. Iterate

✅ Follow up with: "Now expand on that analysis" or
   "Add more details about the connections"

## 🔍 Troubleshooting

### Cline doesn't see configuration

**Solution**: Ensure `.cline/` is in the workspace root
```bash
ls -la .cline/
# Should show: config.json, custom-instructions.md, etc.
```

### API authentication fails

**Solution**: Re-run authentication
```bash
cd scripts/google-api
rm *.pickle  # Clear old tokens
python3 example_usage.py
```

### Python scripts fail

**Solution**: Install dependencies
```bash
cd scripts/google-api
pip install -r requirements.txt
```

### Cline doesn't follow instructions

**Solution**: Reference the custom instructions
```
"Read .cline/custom-instructions.md and follow the
guidelines for adding entities"
```

## 📖 Learn More

- **Custom Instructions**: `.cline/custom-instructions.md`
- **Full Configuration**: `.cline/config.json`
- **API Documentation**: `scripts/google-api/README.md`
- **Project Overview**: `Investigation Dashboard.md`

## 🎓 Advanced Usage

### Create Custom Shortcuts

Edit `.cline/settings.json` to add shortcuts:
```json
"cline.shortcuts": {
  "myTask": "python3 ${workspaceFolder}/scripts/my-script.py"
}
```

### Batch Operations

```
Process all files in Entities/:
1. Validate markdown formatting
2. Check for missing metadata
3. Verify all WikiLinks resolve
4. Generate a completeness report
```

### Integration Testing

```
Test the Google API integration:
1. List 5 files from Google Drive
2. Search YouTube for "DARPA BRAIN"
3. Backup INVESTIGATION_SUMMARY.md to Drive
4. Report on API quota usage
```

## 💬 Getting Help

If you're stuck:

1. **Ask Cline**: "What can you help me with in this project?"
2. **Review docs**: `.cline/README.md` has detailed information
3. **Check examples**: This file has many example prompts
4. **Experiment**: Cline understands natural language - just ask!

---

**Ready to start?** Try this first prompt:

```
"Give me an overview of this Obsidian vault and suggest
3 ways I could use your help with the research"
```

Happy researching! 🚀
