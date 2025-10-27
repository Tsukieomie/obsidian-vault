# Entities Map of Content

Quick navigation hub for all people and organizations under investigation.

## Quick Stats

```dataview
TABLE status as "Status", threat-level as "Threat Level", confidence as "Confidence"
FROM "Entities"
WHERE threat-level
SORT threat-level DESC, confidence DESC
```

## High Priority Targets

### Organizations
- [[Asymptote Network LLC]] - PRIMARY TARGET ⚠️
- [[SalmonCloud Ltd]] - CONFIRMED ASSOCIATE
- [[Oklahoma School of Science and Mathematics]] - Education sector connection

### People - Critical
- [[Junyuan Wang]] - 100% connection, network operator
- [[Chris Wang Oklahoma]] - 95% connection, operations management

## Under Investigation

### People - Medium Priority
- [[Roger Wang]] - 70% connection
- [[Brandon Han]] - 40% connection (Xiao Han theory)

### People - Pending Verification
- [[Derek Wang JY]] - Possible alias
- [[Jerry Han]] - Family investigation
- [[Jing Wang]] - Duke TA, new lead
- [[Carlos Montt]] - Confirmed network member

## By Category

### All Organizations
```dataview
LIST
FROM "Entities/Organizations"
SORT file.name ASC
```

### All People
```dataview
LIST
FROM "Entities/People"
SORT file.name ASC
```

## Quick Actions

- **New Person**: Use template `person-template`
- **New Organization**: Use template `organization-template`
- **Search by confidence**: Use tag `#confidence-XX`
- **Search by threat**: Use tag `#threat-critical` / `#threat-high` / `#threat-medium`

---

← Back to [[Investigation Dashboard]]

Tags: #moc #entities #quick-access
