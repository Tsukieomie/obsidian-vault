# Entity Relationship Map

## Network Visualization

Visual representation of all entities, connections, and confidence levels in the investigation.

**Last Updated:** 2025-10-27
**Status:** Active mapping

## Primary Network Structure

```
Asymptote Network LLC (PRIMARY TARGET - CRITICAL THREAT)
    |
    |-- Junyuan Wang (100% confidence) [CRITICAL]
    |   |-- Role: Network operator
    |   |-- GitHub: JUNYUANGO
    |   |-- Intel connection: UNVERIFIED (CV removed from SignalHire)
    |   |-- Possible alias: Derek Wang JY (THEORY - needs verification)
    |   |
    |   |-- SalmonCloud Ltd (CONFIRMED ASSOCIATE)
    |       |-- Role: Operations
    |       |-- UK Companies House: 10063474
    |
    |-- Chris Wang Oklahoma (95% confidence) [CRITICAL]
    |   |-- Role: Operations management
    |   |-- Family: Dr. Frank Wang (OSSM President)
    |   |   |-- Oklahoma School of Science and Mathematics
    |   |   |-- Education sector influence (NOT research access)
    |   |
    |   |-- NOT: Christopher Wang MIT CSAIL (REMOVED - 0% connection)
    |
    |-- Roger Wang (70% confidence) [PERSON OF INTEREST]
    |   |-- Possible family connection to Chris Wang Oklahoma
    |   |-- Role: Associate (unclear)
    |
    |-- Brandon Han (40% confidence) [HIGH INTEREST]
        |-- Possible identity: Xiao Han (THEORY - needs verification)
        |-- SalmonCloud Ltd shareholder (as Xiao Han)
        |-- Possible family: Jerry Han (UNDER INVESTIGATION)
```

## SalmonCloud Ltd Network

```
SalmonCloud Ltd (UK Companies House 10063474)
    |-- CONFIRMED ASSOCIATE of Asymptote Network
    |
    |-- Shareholders:
    |   |-- Xiao Han (possibly Brandon Han)
    |   |-- [Other shareholders - to be documented]
    |
    |-- GitHub Activity:
    |   |-- frank2002 (SalmonCloud repositories)
    |   |-- JUNYUANGO (Junyuan Wang)
    |   |-- CarlosalbertoMontt (Carlos Montt)
    |
    |-- Personnel:
        |-- Junyuan Wang (Operations - 100% confidence)
        |-- Carlos Montt (Developer - CONFIRMED)
        |   |-- GitHub: CarlosalbertoMontt
        |   |-- Code contributions documented
        |
        |-- Brandon Han / Xiao Han (Shareholder - needs verification)
```

## Technical Infrastructure Network

```
AS53616 (Asymptote Network LLC)
    |-- Autonomous System Number
    |-- ARIN Registration
    |
    |-- Geographic Operations:
    |   |-- United States
    |   |-- United Kingdom
    |   |-- Hong Kong (PRC jurisdiction under NSL)
    |
    |-- Geographic Deception:
    |   |-- UAE/Romania IPs → Actually Hong Kong
    |   |-- IPXO IP leasing service
    |   |-- Location masking operations
    |
    |-- Active Infrastructure:
    |   |-- ghoststack.net
    |   |   |-- Status: ACTIVE
    |   |   |-- AWS Global Accelerator
    |   |   |-- Function: Network relay
    |   |
    |   |-- ca94fan.xyz
    |       |-- Status: ABANDONED (pendingDelete)
    |       |-- Operational security: Domain abandoned when exposed
    |
    |-- Pending Analysis:
        |-- Z-File Infrastructure
            |-- 5 Chinese documentation files
            |-- Language: Chinese
            |-- Location: /Users/kennyrodrigues/investigations/
            |-- Status: Translation required
```

## Under Investigation Connections

```
New Leads (Low to Medium Confidence)
    |
    |-- Jing Wang
    |   |-- Affiliation: Duke University (Teaching Assistant)
    |   |-- Email: j***@duke.edu (partial)
    |   |-- Connection to Wang network: UNKNOWN
    |   |-- Status: NEW LEAD
    |   |-- Priority: LOW
    |
    |-- Derek Wang JY
    |   |-- Theory: Alias for Junyuan Wang
    |   |-- Evidence: "JY" could be initials
    |   |-- Status: UNVERIFIED THEORY
    |   |-- Priority: MEDIUM
    |   |-- Action: Search public records, compare digital footprints
    |
    |-- Jerry Han
        |-- Theory: Family of Brandon Han
        |-- Evidence: Surname match
        |-- Status: UNDER INVESTIGATION
        |-- Priority: MEDIUM
        |-- Action: Verify family relationships
```

## Connection Type Legend

| Symbol | Meaning |
|--------|---------|
| 100% | Confirmed with documentation |
| 90-99% | Multiple corroborating sources |
| 70-89% | Strong circumstantial evidence |
| 50-69% | Reasonable inference |
| 30-49% | Weak correlation |
| 0-29% | Speculation |
| THEORY | Hypothesis requiring verification |
| CONFIRMED | Documented proof |
| UNVERIFIED | Claim without proof |

## Relationship Types

### Organizational
- **Employment:** Confirmed work relationship
- **Operations:** Operational role in network
- **Shareholder:** Ownership stake
- **Association:** Business relationship

### Family
- **Confirmed:** Documented family relationship
- **Possible:** Surname or other indicators suggest family connection
- **Unrelated:** Confirmed different people despite name similarity

### Technical
- **Network Operator:** Controls network infrastructure
- **Developer:** Code contributor
- **Administrator:** System administration role

### Geographic
- **Operations Location:** Where entity operates from
- **Jurisdiction:** Legal jurisdiction
- **Obfuscation:** Fake location used for deception

## Key Removals from Investigation

### Entities Confirmed NOT Involved
1. **Christopher Wang MIT CSAIL**
   - Website: czlwang.com
   - Reason: 0% connection to Chris Wang Oklahoma
   - Status: REMOVED from investigation
   - Note: Different person entirely, no involvement

## Confidence Assessment Breakdown

### 100% Confidence (Documented Proof)
- Junyuan Wang → Asymptote Network LLC
- Carlos Montt → SalmonCloud Ltd (GitHub evidence)
- SalmonCloud Ltd UK registration (Companies House)
- AS53616 → Asymptote Network LLC (ARIN records)

### 90-99% Confidence (Multiple Sources)
- Chris Wang Oklahoma → Asymptote Network LLC
- Chris Wang Oklahoma → Dr. Frank Wang (family)
- Junyuan Wang → SalmonCloud Ltd operations

### 70-89% Confidence (Strong Circumstantial)
- Roger Wang → Asymptote Network LLC
- Roger Wang → Chris Wang Oklahoma (possible family)

### 50-69% Confidence (Reasonable Inference)
- None currently

### 30-49% Confidence (Weak Correlation)
- Brandon Han → Asymptote Network LLC
- Xiao Han = Brandon Han identity theory
- Jerry Han → Brandon Han (family theory)

### Under 30% (Speculation/Unverified)
- Derek Wang JY = Junyuan Wang alias
- Jing Wang connection to investigation

## Geographic Distribution

### United States
- Asymptote Network LLC (operations)
- Chris Wang Oklahoma (location)
- Oklahoma School of Science and Mathematics (Dr. Frank Wang connection)

### United Kingdom
- SalmonCloud Ltd (registered entity)
- UK Companies House 10063474

### Hong Kong / PRC
- Real location of "UAE/Romania" IPs
- PRC jurisdiction (Hong Kong NSL)
- Operations consolidated under PRC legal framework

## Timeline of Key Connections

| Date | Event | Entities | Significance |
|------|-------|----------|--------------|
| [TBD] | Asymptote Network LLC registered | Asymptote | Primary target established |
| [TBD] | SalmonCloud Ltd registered | SalmonCloud, UK Companies House | UK entity confirmed |
| [TBD] | GitHub activity documented | Junyuan Wang, Carlos Montt | Code forensics evidence |
| 2025-10-11 | CV removed from SignalHire | Junyuan Wang | Operational security indicator |
| 2025-10-11 | Christopher Wang MIT removed | Investigation | Confirmed different person |
| 2025-10-27 | Investigation methodology created | N/A | Formalized process |

Note: Many dates to be determined through further evidence collection.

## Network Capabilities by Entity

### Asymptote Network LLC
**Confirmed Capabilities:**
- AS53616 network infrastructure control
- BGP routing manipulation
- DDoS capabilities
- International operations coordination
- Geographic obfuscation (IPXO)

**Threat Level:** CRITICAL

### SalmonCloud Ltd
**Confirmed Capabilities:**
- Software development
- International coordination with Asymptote
- Cross-jurisdiction operations

**Threat Level:** HIGH (as associate of Asymptote)

### Individual Actors

**Junyuan Wang:**
- Network operations expertise
- GitHub activity (code development)
- Operational security awareness (CV removal)
- International operations
- **Threat Level:** CRITICAL

**Chris Wang Oklahoma:**
- Operations management
- Education sector proximity (not access)
- **Threat Level:** CRITICAL

**Carlos Montt:**
- Software development
- Code contributions documented
- **Threat Level:** MEDIUM (confirmed member)

**Roger Wang:**
- Role unclear
- **Threat Level:** MEDIUM (70% confidence)

**Brandon Han:**
- Role unclear, identity uncertain
- **Threat Level:** LOW-MEDIUM (40% confidence)

## Priority Investigation Targets

### Immediate Priority
1. Verify Junyuan Wang Intel connection
2. Confirm Xiao Han = Brandon Han identity
3. Analyze Z-File documentation (Chinese files)

### Secondary Priority
4. Derek Wang JY alias verification
5. Jerry Han family connection
6. Jing Wang Duke TA connection assessment

### Ongoing Monitoring
7. AS53616 infrastructure changes
8. Domain status (ghoststack.net, ca94fan.xyz)
9. GitHub activity patterns

## Evidence Gaps

### High Priority Gaps
- Intel connection verification (Junyuan Wang)
- Brandon Han / Xiao Han identity confirmation
- Z-File documentation translation and analysis
- Dr. Frank Wang relationship to Chris Wang Oklahoma (documented proof)

### Medium Priority Gaps
- Roger Wang role and connection type
- Derek Wang JY records
- Jerry Han family verification
- Complete SalmonCloud shareholder list

### Low Priority Gaps
- Jing Wang relevance to investigation
- Full timeline of Asymptote operations
- Complete GitHub repository analysis

## Attack Surface and Threat Vectors

### Confirmed Capabilities
1. **Network Infrastructure (AS53616)**
   - BGP manipulation
   - DDoS attacks
   - Traffic routing control

2. **Digital Operations**
   - Surveillance capabilities
   - Cyberstalking infrastructure
   - International coordination

3. **Operational Security**
   - Geographic obfuscation
   - Domain abandonment when exposed
   - CV/information removal
   - Multi-jurisdiction operations

### No Evidence Found
- Advanced neurotechnology
- V2K deployment (despite military research existence)
- Remote neural monitoring
- Brain research facility access
- Exotic weapons systems

## Relationship Strength Indicators

### Strong Indicators (High Confidence)
- GitHub commit collaboration
- Company registration documents
- ARIN network registration
- Official records

### Medium Indicators (Medium Confidence)
- Name patterns
- Geographic proximity
- Operational timing correlation
- Shared infrastructure

### Weak Indicators (Low Confidence)
- Surname matching
- Possible aliases (without verification)
- Unverified claims
- Single-source information

## Next Steps for Mapping

1. Verify all HIGH PRIORITY entities and connections
2. Document complete timeline with dates
3. Obtain Dr. Frank Wang relationship documentation
4. Complete SalmonCloud shareholder analysis
5. Verify or remove low-confidence connections
6. Add newly discovered entities as they emerge

## Related Documents
- [[Investigation Dashboard]] - Central command
- [[Threat Assessment]] - Detailed threat analysis
- [[Next Steps]] - Prioritized actions
- All entity profiles in Entities/ directory

---
Tags: #network-map #visualization #entities #relationships #investigation
