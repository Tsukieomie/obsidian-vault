# Analysis Map of Content

Central hub for all analytical work, threat assessments, and investigative findings.

## Current Analysis Files

```dataview
TABLE file.mtime as "Last Modified", status
FROM "Analysis"
SORT file.mtime DESC
```

## Active Investigations

### High Priority
1. Asymptote Network LLC operations analysis
2. Intel connection verification (Junyuan Wang CV)
3. Xiao Han = Brandon Han identity confirmation
4. Z-file infrastructure documentation analysis
5. Family network mapping (Han, Wang families)

### Pending Verification
- [ ] Derek Wang JY alias theory
- [ ] Xiao Han identity confirmation
- [ ] Jerry Han family connection
- [ ] Intel employment verification
- [ ] Z-file documentation translation

## Analysis Types

### Threat Assessments
- [[Threat Assessment]] - Current threat evaluation

### Network Analysis
- Link to [[Technical MOC]] for technical analysis

### Timeline Analysis
- [[Timeline]] - Chronological discoveries

## Investigation Methodology

### Successful Techniques
- GitHub forensic analysis
- Network infrastructure analysis (AS53616)
- ARIN record analysis
- Domain registration investigation
- Geographic IP analysis
- Company registration searches

## Quick Actions

- **New Analysis**: Use template `analysis-template`
- **New Threat Assessment**: Use template `threat-assessment-template`
- **Track investigation**: Add to [[Investigation Dashboard]]

## Cross-References

### By Entity
```dataview
TABLE entity-type, confidence, status
FROM "Analysis"
WHERE entity-type
SORT confidence DESC
```

### By Investigation Phase
- **Discovery**: Initial finding identification
- **Verification**: Confirming findings
- **Analysis**: Deep-dive investigation
- **Reporting**: Documentation and evidence compilation

---

← Back to [[Investigation Dashboard]]

Tags: #moc #analysis #methodology
