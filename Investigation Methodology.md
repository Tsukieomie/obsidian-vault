# Investigation Methodology

Comprehensive guide for systematic investigation workflows and best practices.

## Investigation Framework

### Phase 1: Discovery
**Goal**: Identify potential leads and gather initial information

#### Activities
- Monitor for new indicators
- Collect public information
- Document initial findings
- Create preliminary assessments

#### Documentation
- Use `quick-lead-template` for rapid capture
- Tag with `#discovery`
- Link to potential entities
- Set priority level

#### Quality Checks
- [ ] Source documented
- [ ] Date/time recorded
- [ ] Initial assessment made
- [ ] Priority assigned

### Phase 2: Verification
**Goal**: Confirm initial findings and establish facts

#### Activities
- Cross-reference information
- Verify sources
- Confirm identities
- Validate technical data

#### Documentation
- Update confidence levels
- Document verification methods
- Link corroborating evidence
- Note contradictions

#### Quality Checks
- [ ] Multiple sources confirmed
- [ ] Technical data validated
- [ ] Contradictions investigated
- [ ] Confidence level updated

### Phase 3: Analysis
**Goal**: Deep investigation and connection mapping

#### Activities
- Map relationships
- Analyze patterns
- Identify infrastructure
- Assess capabilities and intent

#### Documentation
- Create detailed entity profiles
- Document technical infrastructure
- Map connection networks
- Develop threat assessments

#### Quality Checks
- [ ] Relationships mapped
- [ ] Patterns identified
- [ ] Capabilities assessed
- [ ] Threat level assigned

### Phase 4: Monitoring
**Goal**: Track ongoing activity and updates

#### Activities
- Monitor for changes
- Track new developments
- Update assessments
- Maintain situational awareness

#### Documentation
- Regular updates to entity pages
- Timeline maintenance
- Evidence collection
- Dashboard updates

#### Quality Checks
- [ ] Regular reviews scheduled
- [ ] Changes documented
- [ ] Assessments updated
- [ ] New leads tracked

## Source Verification Standards

### Public Records
- **Reliability**: High
- **Verification**: Direct source access
- **Documentation**: URL, access date, screenshot

### Social Media/GitHub
- **Reliability**: Medium-High
- **Verification**: Profile verification, cross-platform confirmation
- **Documentation**: Archive links, screenshots, metadata

### Third-Party Databases (SignalHire, etc.)
- **Reliability**: Medium
- **Verification**: Cross-reference with other sources
- **Documentation**: Note limitations, verify key details

### Anonymous Sources
- **Reliability**: Low-Medium
- **Verification**: Require corroboration
- **Documentation**: Treat as leads, not confirmed facts

## Evidence Standards

### Evidence Collection
1. **Preserve Original**: Screenshot, archive, download
2. **Document Context**: URL, date, how found
3. **Maintain Chain of Custody**: Track all handling
4. **Store Securely**: Google Drive + local backup

### Evidence Classification
- **Direct Evidence**: Directly proves connection
- **Circumstantial Evidence**: Suggests connection
- **Corroborating Evidence**: Supports other findings
- **Contradictory Evidence**: Challenges findings

### Evidence Quality
- **Verified**: Multiple sources confirm
- **Probable**: Strong single source
- **Possible**: Reasonable but unconfirmed
- **Speculative**: Theory requiring investigation

## Confidence Assessment Scale

### 100% - Confirmed
- Multiple independent sources
- Direct evidence
- No contradictions
- Verified through authoritative sources

### 70-99% - High Confidence
- Strong evidence from reliable sources
- Some corroboration
- Minor gaps or questions
- Likely accurate

### 40-69% - Medium Confidence
- Reasonable evidence
- Limited corroboration
- Some gaps or contradictions
- Plausible but not certain

### 0-39% - Low Confidence
- Limited evidence
- Single source or questionable sources
- Significant gaps
- Requires verification

## Threat Assessment Framework

### Critical
- Confirmed capability to cause harm
- Active operations detected
- Immediate threat indicators
- Requires urgent action

### High
- Likely capability to cause harm
- Evidence of planning or preparation
- Significant threat indicators
- Requires close monitoring

### Medium
- Possible capability
- Indirect threat indicators
- Monitoring recommended
- Warrants investigation

### Low
- Minimal capability
- Weak indicators
- Low priority
- Periodic review

## Technical Investigation Methods

### Network Infrastructure Analysis
1. **ARIN/WHOIS Lookup**: Registration details
2. **BGP Analysis**: Routing and peering
3. **DNS Investigation**: Domain history and configuration
4. **IP Geolocation**: True location vs. claimed
5. **Hosting Analysis**: Provider and infrastructure

### Domain Investigation
1. **WHOIS History**: Registration timeline
2. **DNS Records**: Current and historical
3. **Website Archive**: Content over time
4. **SSL Certificates**: Ownership validation
5. **Subdomain Discovery**: Full infrastructure

### GitHub Forensics
1. **Commit History**: Contribution patterns
2. **Email Analysis**: Identity confirmation
3. **Repository Analysis**: Code and comments
4. **Collaboration Networks**: Associated users
5. **Deleted Content**: Repository history

### Company Records
1. **Registration Search**: Official records
2. **Filing History**: Changes and updates
3. **Officer/Director Search**: Key personnel
4. **Address Verification**: Physical locations
5. **Status Verification**: Active/dissolved

## Entity Investigation Workflows

### Person Investigation
1. Search public records
2. Check social media (LinkedIn, GitHub, etc.)
3. Search professional databases
4. Verify employment/education
5. Map relationships
6. Document findings
7. Assess confidence and threat

### Organization Investigation
1. Check company registries
2. Verify registration details
3. Identify key personnel
4. Map infrastructure
5. Analyze business activities
6. Document evidence
7. Assess threat level

### Technical Infrastructure Investigation
1. Identify asset (IP, domain, AS)
2. Perform lookups (WHOIS, DNS, etc.)
3. Map related infrastructure
4. Analyze capabilities
5. Link to entities
6. Document IoCs
7. Assess threat

## Cross-Referencing Techniques

### Entity-to-Entity
- Shared addresses
- Family relationships
- Business relationships
- Technical connections
- Timeline correlation

### Entity-to-Infrastructure
- Registration details
- GitHub commits
- Network ownership
- Domain registration
- Employment records

### Infrastructure-to-Infrastructure
- Shared hosting
- IP ranges
- DNS patterns
- SSL certificates
- Network peering

### Evidence-to-Everything
- Link evidence to all mentioned entities
- Reference in timeline
- Tag with relevant categories
- Cross-reference related evidence
- Update all MOCs

## Timeline Management

### Adding Timeline Entries
1. Determine significance
2. Verify date/time
3. Document event clearly
4. Link all related entities
5. Reference evidence
6. Tag appropriately

### Timeline Standards
- **Date Format**: YYYY-MM-DD
- **Precision**: As accurate as possible
- **Source**: Always cite
- **Entities**: Link all relevant
- **Evidence**: Reference all supporting

## Quality Control

### Regular Reviews
- Weekly dashboard review
- Monthly entity reassessment
- Quarterly full audit
- Update confidence levels
- Archive outdated leads

### Documentation Standards
- Clear, concise writing
- Proper linking
- Consistent tagging
- Source citation
- Date/time stamps

### Cross-Reference Checks
- Verify all links
- Check for orphaned notes
- Ensure MOC inclusion
- Validate evidence links
- Confirm timeline entries

## Common Pitfalls to Avoid

### Confirmation Bias
- Actively seek contradictory evidence
- Question assumptions
- Consider alternative explanations
- Document doubts and gaps

### Premature Conclusions
- Mark speculation as such
- Require verification before upgrading confidence
- Distinguish between facts and theories
- Don't let narratives drive evidence

### Source Reliability
- Always verify sources
- Note source limitations
- Cross-reference claims
- Document source reliability

### Link Saturation
- Not all connections are meaningful
- Distinguish strong vs. weak links
- Avoid conspiracy theory thinking
- Require evidence for connections

## Tools and Resources

### Essential Tools
- Obsidian with Dataview plugin
- Archive tools (archive.org, archive.is)
- WHOIS/DNS lookup tools
- BGP/Network analysis tools
- GitHub search and history tools

### Recommended Practices
- Regular backups
- Evidence preservation
- Systematic documentation
- Consistent methodology
- Peer review when possible

## Quick Checklists

### New Lead Checklist
- [ ] Source documented
- [ ] Initial assessment completed
- [ ] Priority assigned
- [ ] Related entities identified
- [ ] Investigation plan created
- [ ] Added to dashboard

### Evidence Checklist
- [ ] Original preserved
- [ ] Metadata documented
- [ ] Source verified
- [ ] Context captured
- [ ] Entities linked
- [ ] Repository updated
- [ ] Drive backup created

### Entity Profile Checklist
- [ ] Basic info gathered
- [ ] Evidence linked
- [ ] Relationships mapped
- [ ] Confidence assessed
- [ ] Threat evaluated
- [ ] Timeline updated
- [ ] MOC updated
- [ ] Dashboard updated

### Technical Finding Checklist
- [ ] Technical details documented
- [ ] Capabilities analyzed
- [ ] Entities linked
- [ ] Infrastructure mapped
- [ ] IoCs extracted
- [ ] Evidence preserved
- [ ] MOC updated

## Investigation Templates Reference

- [[person-template]] - Person investigation
- [[organization-template]] - Organization investigation
- [[technical-finding-template]] - Technical discoveries
- [[evidence-entry-template]] - Evidence documentation
- [[quick-lead-template]] - Rapid lead capture

## Quick Links

- [[Investigation Dashboard]]
- [[Quick Reference Guide]]
- [[Entities MOC]]
- [[Technical MOC]]
- [[Analysis MOC]]
- [[Evidence MOC]]

---

Tags: #methodology #guide #standards #workflow #best-practices
