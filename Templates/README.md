# Templates Guide

This folder contains templates for consistent entity and document creation across the investigation vault.

## Available Templates

### Entity Templates

#### Person Template
**File**: [[Person Template]]
**Use For**: Individual people in the investigation
**Key Sections**:
- Connection confidence percentage
- Role and status
- Identifiers (email, GitHub, LinkedIn, etc.)
- Connections to other entities
- Evidence and sources
- Investigation notes

**When to Use**:
- Discovering a new person of interest
- Documenting a suspect or associate
- Mapping family connections
- Recording technical personnel

#### Organization Template
**File**: [[Organization Template]]
**Use For**: Companies, nonprofits, government entities
**Key Sections**:
- Registration information
- Key people
- Business activities
- Technical infrastructure
- Threat assessment
- Financial information

**When to Use**:
- Company registration discovery
- New business entity identified
- Educational institution connection
- Front organization suspected

#### Technical Infrastructure Template
**File**: [[Technical Infrastructure Template]]
**Use For**: Networks, domains, servers, services
**Key Sections**:
- Technical details (IPs, domains, AS numbers)
- Registration information
- Network analysis
- Capabilities and IOCs
- Obfuscation techniques
- Monitoring status

**When to Use**:
- New domain discovered
- Network infrastructure identified
- Server or service analysis
- Relay or infrastructure documentation

### Investigation Templates

#### Investigation Note Template
**File**: [[Investigation Note Template]]
**Use For**: Recording investigation sessions and findings
**Key Sections**:
- Summary and background
- Findings with confidence levels
- Evidence collected
- Analysis and connections
- Next steps and verification status

**When to Use**:
- Completing an investigation session
- Documenting specific findings
- Recording hypothesis testing
- Tracking verification progress

## How to Use Templates

### Method 1: Copy and Paste (Manual)
1. Open the template file
2. Copy all content
3. Create new note in appropriate location
4. Paste template content
5. Replace all `{{PLACEHOLDER}}` text with actual information
6. Update tags at bottom

### Method 2: Obsidian Templates Plugin
1. Enable Templates core plugin in Obsidian
2. Set template folder to `/Templates`
3. Use Ctrl/Cmd + T to insert template
4. Choose appropriate template
5. Fill in placeholder information

### Method 3: Templater Plugin (Advanced)
If you have Templater community plugin:
- Templates can be enhanced with dynamic date insertion
- Auto-populate some fields
- Interactive prompts for key fields

## Template Placeholders

### Common Placeholders
Replace these with actual information:
- `{{PERSON NAME}}` - Full name of individual
- `{{ORGANIZATION NAME}}` - Legal or common name
- `{{PERCENTAGE}}` - Connection confidence (0-100)
- `{{ROLE}}` - Function or position
- `{{STATUS}}` - Current investigation status
- `{{DATE}}` - Relevant date (YYYY-MM-DD format)
- `{{LOCATION}}` - Geographic location
- `{{EVIDENCE}}` - Evidence description
- `{{custom-tags}}` - Specific tags for this entity

### Status Values
Standardized status values:
- CRITICAL THREAT
- HIGH THREAT
- MEDIUM THREAT
- LOW THREAT
- UNDER INVESTIGATION
- PENDING VERIFICATION
- VERIFIED
- REMOVED FROM INVESTIGATION

### Connection Confidence
Use percentage to indicate confidence:
- 100%: Absolute confirmation
- 90-99%: Very high confidence
- 70-89%: High confidence
- 50-69%: Medium confidence
- 30-49%: Low-medium confidence
- 10-29%: Low confidence
- <10%: Speculative

## Template Maintenance

### Updating Templates
- Edit template files as investigation methodology evolves
- Add new sections if needed
- Update placeholder names for clarity
- Document changes in this README

### Version History
- **2025-10-27**: Initial template creation
  - Person Template
  - Organization Template
  - Technical Infrastructure Template
  - Investigation Note Template

## Best Practices

### Consistency
- Use templates for all new entities
- Don't skip sections (use "Unknown" or "N/A" if needed)
- Maintain consistent formatting
- Use standardized tags

### Linking
- Always link to related entities using `[[Entity Name]]`
- Reference [[Evidence Repository]] for evidence files
- Link to [[Investigation Dashboard]] and [[Timeline]]
- Cross-reference related documents

### Evidence Standards
- Include source for each claim
- Note confidence level for findings
- Link to evidence files when available
- Document verification status

### Tags
- Always include relevant tags at bottom
- Use hierarchical tags: `#entity/person`, `#entity/organization`
- Include threat level tags: `#critical-threat`, `#high-threat`
- Add date tags for time-sensitive items

## Template Usage Examples

### Example 1: New Person Discovery
```markdown
Scenario: Discovered "John Smith" in GitHub commits

1. Create new file: /Entities/People/John Smith.md
2. Use [[Person Template]]
3. Fill in:
   - Connection Confidence: 30% (initial discovery)
   - Role: Developer (from GitHub activity)
   - GitHub: johnsmith123
   - Email: (from commits)
   - Connection to [[SalmonCloud Ltd]]
4. Add to [[Entity Index]]
5. Reference in [[Timeline]]
```

### Example 2: New Domain Found
```markdown
Scenario: Discovered "suspicious-domain.com" in network scan

1. Create: /Technical/suspicious-domain.com.md
2. Use [[Technical Infrastructure Template]]
3. Document:
   - IP addresses
   - Registration date
   - Nameservers
   - Connection to known entities
4. Add IOCs
5. Set monitoring status
```

## Integration with Investigation Workflow

### Discovery → Documentation → Analysis
1. **Discovery**: Find new entity or information
2. **Template**: Use appropriate template
3. **Document**: Fill in all known information
4. **Link**: Connect to related entities
5. **Index**: Add to [[Entity Index]]
6. **Timeline**: Add discovery to [[Timeline]]
7. **Dashboard**: Update [[Investigation Dashboard]] if significant

### Quality Checklist
Before considering an entity document complete:
- [ ] Template structure followed
- [ ] All placeholders replaced or marked N/A
- [ ] Links to related entities created
- [ ] Evidence sources documented
- [ ] Tags added
- [ ] Added to Entity Index
- [ ] Referenced in Timeline (if significant)
- [ ] Verification status noted

## Related Documents
- [[Entity Index]] - Complete entity list
- [[Investigation Dashboard]] - Central hub
- [[Evidence Repository]] - Evidence files
- [[Timeline]] - Chronological record

## Questions?

For template questions or suggestions:
1. Document in [[Action Items]]
2. Consider creating custom template variant
3. Update this README with clarifications

---
Tags: #templates #guide #documentation #workflow
