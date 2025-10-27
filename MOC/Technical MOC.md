# Technical Infrastructure Map of Content

Central hub for all technical infrastructure, network analysis, and digital forensics.

## Active Infrastructure

### Network Assets
- [[AS53616 Network Analysis]] - Primary infrastructure
  - **Operations**: US/UK/Hong Kong
  - **Capabilities**: BGP, DDoS, geographic obfuscation

### Active Domains
- [[ghoststack.net]] - AWS Global Accelerator relay
  - **Status**: Active
  - **Function**: Network relay

### Abandoned/Inactive
- [[ca94fan.xyz]] - pendingDelete status

### Pending Analysis
- [[Z-File Infrastructure]] - 5 Chinese documentation files

## Technical Categories

### Network Infrastructure
```dataview
TABLE status, capabilities, threat-level
FROM "Technical"
WHERE contains(file.name, "Network") OR contains(file.name, "AS53")
```

### Domains & Hosting
```dataview
LIST
FROM "Technical"
WHERE contains(file.tags, "#domain") OR contains(file.tags, "#hosting")
```

### Forensic Analysis
```dataview
LIST
FROM "Technical"
WHERE contains(file.tags, "#forensics") OR contains(file.tags, "#analysis")
```

## Key Findings

### Geographic Deception
- UAE/Romania IPs → Actually Hong Kong
- IPXO IP leasing for location masking
- PRC jurisdiction consolidation (Hong Kong NSL)

### Confirmed Capabilities
- Traditional electronic harassment
- Network infrastructure control (AS53616)
- DDoS capabilities
- BGP routing manipulation
- International coordination
- Geographic obfuscation

## Quick Actions

- **New Technical Finding**: Use template `technical-finding-template`
- **New Network Analysis**: Use template `network-analysis-template`
- **Search infrastructure**: `#infrastructure`
- **Search forensics**: `#forensics`

## Related

- [[Investigation Dashboard]] - Main hub
- [[Evidence Repository]] - Technical evidence files

---

Tags: #moc #technical #infrastructure #forensics
