# Investigation Methodology

## Overview
Comprehensive methodology for conducting network harassment investigation with focus on evidence quality, legal admissibility, and operational security.

**Version:** 1.0
**Created:** 2025-10-27
**Status:** Active methodology guide

## Core Principles

### 1. Evidence-Based Analysis
- All claims must be supported by verifiable evidence
- Distinguish between facts, theories, and speculation
- Document chain of custody for all evidence
- Maintain high standards for court admissibility

### 2. Technical Accuracy
- Use precise technical terminology
- Verify technical claims through multiple sources
- Acknowledge limitations of analysis
- Correct errors promptly and transparently

### 3. Operational Security
- Minimize digital footprint during investigation
- Secure evidence storage and handling
- Protect investigator identity when appropriate
- Document activities for legal accountability

### 4. Legal Compliance
- Conduct all investigation within legal boundaries
- No unauthorized access to systems or data
- Respect privacy laws and regulations
- Prepare evidence for potential legal proceedings

## Investigation Phases

### Phase 1: Discovery and Reconnaissance

**Objective:** Identify subjects, infrastructure, and connections

**Methods:**
1. **Open Source Intelligence (OSINT)**
   - Public records searches
   - Company registrations
   - Domain registrations (WHOIS)
   - Social media analysis (public posts only)
   - Academic publications
   - Professional networking sites

2. **Network Infrastructure Analysis**
   - ARIN/RIPE database queries
   - BGP routing information
   - DNS records and history
   - IP geolocation analysis
   - AS (Autonomous System) relationships

3. **Digital Footprint Mapping**
   - GitHub repositories and commits
   - Code repositories (public)
   - Email patterns in public data
   - Username correlation
   - Cross-platform identity linking

**Documentation Requirements:**
- Source URLs and timestamps
- Screenshot evidence
- Wayback Machine archives
- Export and preserve data locally

**Tools:**
- WHOIS lookup services
- ARIN/RIPE databases
- BGPView, Hurricane Electric BGP Toolkit
- GitHub advanced search
- Google Dorks for targeted searches
- Archive.org Wayback Machine

### Phase 2: Evidence Collection and Preservation

**Objective:** Secure and document all evidence with proper chain of custody

**Methods:**
1. **Digital Evidence Collection**
   - Full page screenshots with visible URL and timestamp
   - PDF exports of web pages
   - Git repository cloning with verification
   - Archive.org preservation requests
   - Local backups with checksums

2. **Metadata Documentation**
   - Collection timestamp
   - Source URL
   - Collector identity
   - Collection method
   - File integrity hashes (SHA-256)

3. **Chain of Custody**
   - Initial collection record
   - Storage location
   - Access log
   - Any transfers or copies
   - Final disposition

**Best Practices:**
- Never modify original evidence
- Create working copies for analysis
- Store originals in write-protected media
- Maintain offline backups
- Document every evidence handling step

**Tools:**
- Screenshot tools with metadata preservation
- Git with verification (git fsck)
- SHA-256 hash generation
- Cloud storage with versioning (Google Drive)
- Local encrypted storage

### Phase 3: Analysis and Correlation

**Objective:** Identify patterns, relationships, and significance of collected evidence

**Methods:**
1. **Entity Relationship Mapping**
   - Document all connections between entities
   - Assign confidence levels (0-100%)
   - Note source of connection claim
   - Update as new evidence emerges

2. **Timeline Construction**
   - Chronological ordering of events
   - Cross-reference multiple sources
   - Identify gaps requiring investigation
   - Note discrepancies

3. **Technical Analysis**
   - Network infrastructure relationships
   - Code analysis and attribution
   - Infrastructure change tracking
   - Operational pattern identification

4. **Threat Assessment**
   - Capability evaluation
   - Intent indicators
   - Opportunity analysis
   - Risk level determination

**Confidence Level Guidelines:**
- 100%: Documented proof (court records, official documents)
- 90-99%: Multiple corroborating sources, high reliability
- 70-89%: Strong circumstantial evidence
- 50-69%: Reasonable inference from available data
- 30-49%: Weak correlation, requires verification
- 0-29%: Speculation, insufficient evidence

**Documentation:**
- Analysis notes with reasoning
- Source citations
- Confidence assessments
- Alternative explanations considered
- Gaps in evidence identified

### Phase 4: Verification and Validation

**Objective:** Ensure accuracy and reliability of findings

**Methods:**
1. **Source Verification**
   - Confirm authenticity of documents
   - Verify claims through independent sources
   - Check for disinformation or planted evidence
   - Validate technical findings

2. **Peer Review**
   - Technical review by qualified individuals
   - Legal review for admissibility
   - Red team challenge of conclusions
   - Expert consultation when needed

3. **Alternative Hypothesis Testing**
   - Consider alternative explanations
   - Attempt to disprove conclusions
   - Identify confirmation bias
   - Document why alternatives rejected

**Quality Control:**
- Regular review of evidence quality
- Update confidence levels as evidence changes
- Remove or downgrade unreliable information
- Correct errors promptly

### Phase 5: Documentation and Reporting

**Objective:** Create clear, accurate, actionable reports

**Report Types:**
1. **Executive Summary**
   - High-level overview for non-technical audience
   - Key findings and recommendations
   - Risk assessment
   - Next steps

2. **Technical Report**
   - Detailed technical analysis
   - Network infrastructure documentation
   - Code forensics results
   - Methodology description

3. **Legal Evidence Package**
   - Court-admissible evidence only
   - Chain of custody documentation
   - Expert analysis suitable for court
   - Timeline of incidents

4. **Operational Intelligence**
   - Actionable intelligence for defensive measures
   - Threat indicators
   - Detection methods
   - Response recommendations

**Report Standards:**
- Clear, concise language
- Technical accuracy
- Proper citations
- Visual aids (diagrams, charts)
- Executive summary for each section
- Glossary of technical terms

## Specific Methodologies

### Network Infrastructure Investigation

**AS (Autonomous System) Analysis:**
1. Identify ASN from ARIN/RIPE database
2. Document organization and contacts
3. Map BGP relationships and peering
4. Track announced prefixes over time
5. Identify connected networks
6. Monitor for changes

**Domain Investigation:**
1. WHOIS lookup (current and historical)
2. DNS records (A, MX, TXT, NS)
3. Subdomain enumeration
4. SSL certificate analysis
5. Web technology fingerprinting
6. Archive.org historical snapshots

**IP Address Analysis:**
1. Geolocation (with caveats about accuracy)
2. Reverse DNS lookup
3. Port scanning (only if legally authorized)
4. WHOIS information
5. IP reputation checks
6. Associated domains and services

**Tools:**
```bash
# WHOIS lookup
whois domain.com
whois -h whois.arin.net AS53616

# DNS enumeration
dig domain.com ANY
nslookup domain.com

# BGP analysis
# Use online tools: bgpview.io, bgp.he.net

# Historical DNS
# Use online tools: securitytrails.com, dnshistory.org
```

### GitHub Forensic Analysis

**Repository Analysis:**
1. Clone repository with full history
2. Extract commit history
3. Identify all contributors
4. Analyze commit patterns and timing
5. Extract email addresses
6. Review code for indicators
7. Document cross-repository connections

**Commit Forensics:**
```bash
# Clone repository
git clone https://github.com/user/repo.git
cd repo

# Verify integrity
git fsck --full

# Extract all commits with details
git log --all --pretty=format:"%H|%an|%ae|%ad|%s" > commits.txt

# List all authors
git log --all --format='%an <%ae>' | sort -u

# Find commits by specific author
git log --author="name"

# Check file history
git log --follow -- filename

# Extract all email addresses
git log --all --format='%ae' | sort -u

# Timing analysis
git log --all --pretty=format:"%ad" --date=iso
```

**Documentation:**
- Repository URLs and clone dates
- Commit hashes for reference
- Author identification
- Email pattern analysis
- Cross-repository collaboration evidence

### Company and Entity Research

**Public Records:**
1. Corporation registration (Secretary of State)
2. UK Companies House (for UK entities)
3. DUNS number lookup
4. Business licenses
5. Trademark registrations
6. Patent filings

**Financial Records:**
1. Public filings (if applicable)
2. Credit reports (if authorized)
3. Bankruptcy records
4. Liens and judgments
5. Property records

**Personnel Research:**
1. LinkedIn profiles (public information only)
2. Professional publications
3. Academic credentials verification
4. Employment history (public sources)
5. Social media (public posts only)

**Important:** Only use publicly available information. Do not attempt unauthorized access.

### OSINT Best Practices

**Search Techniques:**
1. **Google Dorks**
   ```
   site:github.com "email@domain.com"
   site:linkedin.com "Company Name" "Title"
   inurl:profile "Full Name"
   filetype:pdf site:domain.com
   ```

2. **Username Correlation**
   - Search username across platforms
   - Use tools like Namechk, Sherlock
   - Document cross-platform presence
   - Note patterns and reuse

3. **Email Pattern Analysis**
   - Common patterns: firstname.lastname@, first.last@
   - Extract from public sources
   - Verify through multiple confirmations
   - Use for further searches

**OSINT Tools:**
- theHarvester (email/subdomain enumeration)
- Maltego (relationship mapping)
- SpiderFoot (automated OSINT)
- Shodan (internet device search)
- Censys (internet-wide scanning data)
- Hunter.io (email finding)

**Operational Security for OSINT:**
- Use VPN for searches
- Clear browser cookies/cache between searches
- Use separate browser/profile for investigation
- Don't log into personal accounts during OSINT
- Document all searches for legal defensibility

## Evidence Quality Standards

### High Quality (Court Admissible)
- Official government records
- Company registrations
- Court documents
- Verified public records
- Technical logs with proper authentication
- Digital evidence with chain of custody
- Expert analysis with credentials

### Medium Quality (Investigative Value)
- Corroborated circumstantial evidence
- Technical analysis requiring expert interpretation
- Social media public posts
- Archived web pages
- Multiple consistent sources

### Low Quality (Requires Verification)
- Single-source claims
- Unverified social media
- Hearsay or secondhand information
- Speculation without supporting evidence
- Anonymous sources without corroboration

### Inadmissible (Do Not Use)
- Illegally obtained evidence
- Evidence without chain of custody
- Fabricated or planted evidence
- Subjective interpretations presented as fact
- Unverifiable claims

## Threat Assessment Framework

### Capability Assessment
**Questions to Answer:**
- What infrastructure do they control?
- What technical skills are demonstrated?
- What resources are available?
- What tools/methods are employed?

**Evidence Required:**
- Technical infrastructure documentation
- Code analysis showing skill level
- Resource indicators (company size, funding)
- Observed methods and techniques

### Intent Analysis
**Indicators:**
- Targeting patterns
- Operational security measures
- Coordination level
- Persistence over time
- Escalation patterns

**Important:** Intent is harder to prove than capability. Focus on observable behaviors.

### Opportunity Evaluation
**Factors:**
- Geographic proximity or reach
- Network access
- System vulnerabilities
- Timing of activities
- Resource availability

### Risk Level Determination
**Framework:**
- CRITICAL: Demonstrated capability + clear targeting + ongoing activity
- HIGH: Strong capability + probable intent + opportunity
- MEDIUM: Some capability + unclear intent + limited opportunity
- LOW: Minimal capability + no clear intent + no demonstrated opportunity

## Legal and Ethical Guidelines

### Legal Boundaries
**ALLOWED:**
- Public records searches
- Analysis of publicly available information
- WHOIS and DNS lookups
- Company registration searches
- Social media public post review
- Archive.org historical research

**NOT ALLOWED:**
- Unauthorized access to computer systems
- Password guessing or cracking
- Social engineering to obtain private information
- Intercepting communications
- Trespassing (physical or digital)
- Harassment or threats
- Impersonation

### Evidence Handling
**Requirements:**
- Maintain chain of custody
- Document all collection methods
- Preserve original evidence
- Never modify evidence
- Store securely
- Provide to law enforcement when appropriate

### Privacy Considerations
**Balance:**
- Legitimate investigation interests
- Privacy rights of subjects
- Public interest
- Legal requirements

**Best Practice:** Focus on publicly available information and conduct investigation as if it will be scrutinized in court.

## Tools and Resources

### Network Analysis
- ARIN WHOIS: whois.arin.net
- RIPE Database: apps.db.ripe.net
- BGPView: bgpview.io
- Hurricane Electric BGP: bgp.he.net
- ViewDNS.info: viewdns.info

### Domain Investigation
- DomainTools: domaintools.com
- SecurityTrails: securitytrails.com
- DNS History: dnshistory.org
- Wayback Machine: archive.org/web

### Code/GitHub Analysis
- GitHub Advanced Search: github.com/search
- GitHub Code Search
- GitFive: OSINT tool for GitHub
- git-secrets: Prevent secrets in code

### Company Research
- OpenCorporates: opencorporates.com
- UK Companies House: beta.companieshouse.gov.uk
- EDGAR (SEC filings): sec.gov/edgar
- DUNS Lookup: dnb.com

### OSINT Frameworks
- OSINT Framework: osintframework.com
- IntelTechniques: inteltechniques.com/tools
- Bellingcat's Online Investigation Toolkit

## Investigation Workspace Setup

### Directory Structure
```
investigation/
├── Evidence/
│   ├── Screenshots/
│   ├── Documents/
│   ├── Repositories/
│   └── Logs/
├── Analysis/
│   ├── Network/
│   ├── Entities/
│   └── Technical/
├── Reports/
│   ├── Executive/
│   ├── Technical/
│   └── Legal/
├── Tools/
└── Documentation/
```

### Evidence Naming Convention
```
YYYY-MM-DD_Category_Subject_Description.ext
2025-10-27_WHOIS_domain.com_record.txt
2025-10-27_GitHub_username_commits.json
2025-10-27_Screenshot_linkedin_profile.png
```

### Metadata Template
```
Evidence ID: YYYYMMDD-NNN
Type: [Screenshot|Document|Log|Repository|Other]
Source: [URL or location]
Subject: [Entity or topic]
Collected By: [Investigator]
Collection Date: YYYY-MM-DD HH:MM:SS UTC
Collection Method: [How obtained]
Hash (SHA-256): [file hash]
Storage Location: [Path]
Chain of Custody: [Log of handling]
Notes: [Any relevant information]
```

## Reporting Templates

### Executive Summary Template
```markdown
# Executive Summary: [Title]

## Overview
[1-2 paragraph summary]

## Key Findings
1. [Finding with confidence level]
2. [Finding with confidence level]
3. [Finding with confidence level]

## Threat Assessment
- Threat Level: [CRITICAL|HIGH|MEDIUM|LOW]
- Capabilities: [Summary]
- Active Operations: [Yes/No with details]

## Recommendations
1. [Immediate actions]
2. [Short-term actions]
3. [Long-term strategy]

## Next Steps
[Prioritized list]
```

### Technical Report Template
```markdown
# Technical Analysis: [Subject]

## Methodology
[How analysis was conducted]

## Infrastructure Analysis
### Network
[AS, IP, routing details]

### Domains
[Domain analysis]

### Systems
[System details]

## Code Analysis
[If applicable]

## Findings
[Detailed technical findings]

## Evidence
[Links to evidence with IDs]

## Conclusions
[Technical conclusions]

## Appendices
[Technical details, logs, raw data]
```

## Quality Assurance Checklist

### Before Publishing Analysis
- [ ] All claims supported by evidence
- [ ] Sources properly cited
- [ ] Confidence levels assigned
- [ ] Alternative explanations considered
- [ ] Technical accuracy verified
- [ ] Legal compliance confirmed
- [ ] Chain of custody documented
- [ ] No speculation presented as fact
- [ ] Privacy considerations addressed
- [ ] Peer review completed (if available)

### Before Legal Submission
- [ ] Only court-admissible evidence included
- [ ] Chain of custody complete
- [ ] All evidence legally obtained
- [ ] Expert credentials documented
- [ ] Technical terms explained
- [ ] Timeline accurate and sourced
- [ ] No exaggeration or speculation
- [ ] Formatted for legal review
- [ ] Exhibits properly labeled
- [ ] Legal counsel review (if available)

## Related Documents
- [[Evidence Repository]] - Evidence index
- [[Investigation Dashboard]] - Current status
- [[Threat Assessment]] - Risk analysis
- [[Next Steps]] - Action items

---
Tags: #methodology #procedures #investigation #standards #quality-assurance
