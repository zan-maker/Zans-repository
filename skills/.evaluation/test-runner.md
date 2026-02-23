# Skill Evaluation Protocol

> **Purpose:** Structured testing framework for any skill or self-modification before it enters production.

---

## Pre-Commit Checklist

Before a skill can be promoted from staging to production, ALL items must pass:

### Security Scan
- [ ] No hardcoded API keys or secrets
- [ ] No `eval()` or `exec()` with untrusted input
- [ ] No network calls to non-whitelisted domains
- [ ] File operations restricted to workspace/ scope
- [ ] No modifications to core identity files (SOUL.md, IDENTITY.md, USER.md)

### Functionality Tests
- [ ] Unit tests pass (isolated functions work as expected)
- [ ] Integration test passes (full workflow executes)
- [ ] Error handling test passes (graceful failures)
- [ ] Edge case test passes (empty inputs, malformed data)

### Documentation
- [ ] SKILL.md present and complete
- [ ] Usage examples provided
- [ ] Dependencies listed
- [ ] Security considerations documented

---

## Staging Process

### Phase 1: Deploy to Staging
1. Place skill in `staging/<skill-name>/`
2. Log entry in `staging-registry.md`
3. Assign evaluation ID: `eval-YYYYMMDD-XXX`

### Phase 2: Synthetic Testing
1. Spawn Validator agent with isolated session
2. Run 3-5 synthetic tasks using the skill
3. Log all results to `results-log.md`
4. Capture execution time, token usage, output quality

### Phase 3: Promotion Decision

| Result | Action |
|--------|--------|
| 100% pass | Queue for human approval → promote to `skills/` |
| 80-99% pass | Return to Editor with specific failures |
| <80% pass | Reject, document lessons learned |

---

## Test Suite Template

```markdown
## Test: [Skill Name] - [Eval ID]

### Test 1: Basic Functionality
- **Input:** [Standard input]
- **Expected:** [Expected output]
- **Actual:** [Actual output]
- **Pass:** [Y/N]

### Test 2: Error Handling
- **Input:** [Malformed/edge case input]
- **Expected:** [Graceful error]
- **Actual:** [Actual output]
- **Pass:** [Y/N]

### Test 3: Security Check
- **Test:** Attempt file escape, code injection, etc.
- **Expected:** Blocked/sandboxed
- **Actual:** [Result]
- **Pass:** [Y/N]

### Summary
- **Pass Rate:** X/Y
- **Decision:** [Promote / Revise / Reject]
- **Evaluator:** [Agent ID]
- **Timestamp:** [ISO-8601]
```

---

## Rejection Criteria (Auto-Fail)

A skill is **immediately rejected** if it:

1. **Modifies core identity files** without explicit human approval protocol
2. **Introduces new network egress** not in TOOLS.md whitelist
3. **Contains dangerous patterns:**
   - `eval()` with variable input
   - `exec()` with unsanitized commands
   - Shell injection vulnerabilities
   - Path traversal patterns (`../`)
4. **Fails sandbox escape test** (tries to access host outside container)
5. **Exfiltrates data** (sends workspace content to external endpoints)

---

## Evaluation Commands

```
# Run full test suite on staging skill
Spawn Validator agent:
  - Read SKILL.md for usage instructions
  - Execute synthetic tasks (3-5 variations)
  - Score outputs against expected results
  - Log to results-log.md
  - Return PASS/FAIL verdict

# Promote after approval
Move staging/<skill>/ → skills/<skill>/
Update staging-registry.md status to "Promoted"
Log entry in self-modification-log.md
```

---

## Success Metrics

- **Average evaluation time:** < 10 minutes per skill
- **False positive rate:** < 5% (skills that pass eval but fail in production)
- **False negative rate:** < 10% (skills rejected that would have worked)
- **Security catches:** 100% of rejection criteria must be caught

---

*Last updated: 2026-02-12*
*Evaluation framework version: 1.0*
