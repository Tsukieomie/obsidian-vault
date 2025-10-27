# Evidence Map of Content

Quick access to all evidence documentation and tracking.

## Evidence Repository

Main index: [[Evidence Repository]]

## Evidence by Type

### Executive Reports
- Executive briefs and summaries
- Intelligence reports
- Master reports

### Legal Documentation
- Court-ready materials
- Legal reports
- Company records

### Technical Evidence
- Network analysis reports
- Forensic analysis
- Infrastructure documentation

### Entity Evidence
- SalmonCloud Ltd documentation
- Asymptote Network LLC records
- GitHub forensics

## Evidence Intake Workflow

### 1. Initial Capture
Use template: `evidence-entry-template`

### 2. Classification
- **Type**: Document, Screenshot, Recording, Network Data, etc.
- **Source**: Web, Drive, Local, etc.
- **Entities**: Tag relevant people/organizations
- **Confidence**: Low/Medium/High/Confirmed

### 3. Cross-Reference
- Link to related entities
- Link to timeline entries
- Link to technical findings

### 4. Storage
- Add to [[Evidence Repository]]
- Update Google Drive links
- Tag appropriately

## Quick Searches

### By Entity
```dataview
TABLE evidence-type, source, confidence, date
FROM #evidence
WHERE entity
SORT date DESC
```

### By Type
```dataview
TABLE entity, source, date
FROM #evidence
WHERE evidence-type
SORT evidence-type, date DESC
```

### Recent Evidence
```dataview
TABLE evidence-type, entity, source
FROM #evidence
SORT file.ctime DESC
LIMIT 10
```

## Evidence Standards

### Documentation Requirements
- [ ] Source identified and verified
- [ ] Date/timestamp recorded
- [ ] Related entities linked
- [ ] Storage location noted
- [ ] Confidence level assessed

### Chain of Custody
- Original source preserved
- Modification history tracked
- Access logged
- Integrity verified

## Quick Actions

- **New Evidence Entry**: Use template `evidence-entry-template`
- **Link Evidence**: Use `[[entity-name]]` linking
- **Tag Evidence**: Use `#evidence` + type tags
- **Add to Repository**: Update [[Evidence Repository]]

---

← Back to [[Investigation Dashboard]]

Tags: #moc #evidence #documentation
