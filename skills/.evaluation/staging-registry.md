# Staging Registry

> **Purpose:** Track all skills and modifications currently in evaluation.

---

## Active Evaluations

| Eval ID | Skill Name | Submitted | Status | Tests Passed | Assigned Validator |
|---------|------------|-----------|--------|--------------|-------------------|
| (empty) | - | - | - | - | - |

---

## Evaluation Lifecycle

```
Submitted → In Review → Testing → Decision → [Promoted | Rejected | Revise]
```

---

## Registry Entry Format

```markdown
### Eval: [ID]
- **Skill:** [Name]
- **Submitted By:** [Agent / Human]
- **Submitted At:** [ISO-8601]
- **Status:** [Submitted | In Review | Testing | Decision Pending | Promoted | Rejected]
- **Location:** `staging/[skill-name]/`
- **Change Type:** [New / Update / Refactor]
- **Description:** [What changed]
- **Security Scan:** [Pending / Passed / Failed]
- **Test Results:** See `results-log.md` entry for [Eval ID]
- **Validator:** [Agent ID]
- **Decision:** [Pending / Approved / Rejected]
- **Decision At:** [ISO-8601]
- **Notes:** [Any special considerations]
```

---

## Promoted to Production

| Eval ID | Skill Name | Promoted At | Production Location |
|---------|------------|-------------|---------------------|
| (empty) | - | - | - |

---

## Rejected

| Eval ID | Skill Name | Rejected At | Reason |
|---------|------------|-------------|--------|
| (empty) | - | - | - |

---

## Lessons from Rejections

Document patterns that caused rejections to improve future submissions:

```markdown
### Pattern: [Description]
- **First Seen:** [Date]
- **Frequency:** [How many rejections]
- **Issue:** [What went wrong]
- **Prevention:** [How to avoid in future]
```

---

*Last updated: 2026-02-12*
