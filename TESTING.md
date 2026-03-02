# Testing Instructions — Pre-IPO Compliance Gate

## Testing Architecture

Testing is organized into four layers, each validating a different boundary:

```
Layer 4: End-to-End        GitHub PR → API Gateway → Airia → Lambda → GitHub Comment
Layer 3: Airia Pipeline    Airia editor "Run" with mock JSON input
Layer 2: Lambda Integration  Invoke deployed Lambdas with test payloads via AWS CLI
Layer 1: Unit Tests         Local Python tests with mocked GitHub API responses
```

Run from the bottom up. Don't move to the next layer until the current one passes.

---

## Layer 1: Unit Tests (Local, No AWS/GitHub Required)

Unit tests validate classification logic, pattern matching, and output schema
without calling any external APIs. All GitHub responses are mocked.

### Prerequisites

```bash
pip install pytest --break-system-packages
```

### Run All Unit Tests

```bash
cd pre-ipo-compliance-gate/
python -m pytest tests/ -v
```

### What's Tested

| Test File | Covers | Key Assertions |
|-----------|--------|----------------|
| `tests/test_license_scanner.py` | License classification, manifest parsing, verdict logic | GPL→CRITICAL, MIT→LOW, unknown→CRITICAL, verdict escalation |
| `tests/test_secrets_scanner.py` | Secret pattern matching, financial file detection, PII, gitignore | AWS key detected, values redacted, .xlsx flagged, SSN caught |
| `tests/test_pr_reporter.py` | Output schema, verdict aggregation, action routing | BLOCKED→issue created, PASS→no issue, audit record schema |

### Expected Results

```
tests/test_license_scanner.py::test_gpl3_classified_critical          PASSED
tests/test_license_scanner.py::test_mit_classified_low                PASSED
tests/test_license_scanner.py::test_unknown_license_classified_critical PASSED
tests/test_license_scanner.py::test_agpl_classified_critical          PASSED
tests/test_license_scanner.py::test_lgpl_classified_high              PASSED
tests/test_license_scanner.py::test_verdict_blocked_on_critical       PASSED
tests/test_license_scanner.py::test_verdict_review_on_high            PASSED
tests/test_license_scanner.py::test_verdict_pass_on_low_only          PASSED
tests/test_license_scanner.py::test_npm_manifest_parsing              PASSED
tests/test_license_scanner.py::test_python_requirements_parsing       PASSED
tests/test_license_scanner.py::test_empty_pr_returns_pass             PASSED
tests/test_license_scanner.py::test_missing_params_returns_400        PASSED

tests/test_secrets_scanner.py::test_aws_key_detected                  PASSED
tests/test_secrets_scanner.py::test_aws_key_redacted_in_output        PASSED
tests/test_secrets_scanner.py::test_github_token_detected             PASSED
tests/test_secrets_scanner.py::test_google_api_key_detected           PASSED
tests/test_secrets_scanner.py::test_stripe_key_detected               PASSED
tests/test_secrets_scanner.py::test_private_key_detected              PASSED
tests/test_secrets_scanner.py::test_database_url_detected             PASSED
tests/test_secrets_scanner.py::test_generic_password_detected         PASSED
tests/test_secrets_scanner.py::test_jwt_detected_as_high              PASSED
tests/test_secrets_scanner.py::test_xlsx_financial_file_detected      PASSED
tests/test_secrets_scanner.py::test_csv_in_finance_dir_detected       PASSED
tests/test_secrets_scanner.py::test_ssn_detected                      PASSED
tests/test_secrets_scanner.py::test_gitignore_gap_detection           PASSED
tests/test_secrets_scanner.py::test_clean_file_no_findings            PASSED
tests/test_secrets_scanner.py::test_values_never_in_output            PASSED

tests/test_pr_reporter.py::test_blocked_verdict_creates_issue         PASSED
tests/test_pr_reporter.py::test_pass_verdict_no_issue                 PASSED
tests/test_pr_reporter.py::test_audit_record_schema                   PASSED
tests/test_pr_reporter.py::test_missing_params_returns_400            PASSED
```

---

## Layer 2: Lambda Integration Tests (Deployed Lambdas, Real AWS)

Tests invoke deployed Lambda functions with controlled payloads.
Requires: Lambdas deployed (`tools/deploy_all.sh`), GitHub token configured.

### 2a. Create a Test Repository

Create a **private** GitHub repo with known compliance issues:

```bash
# Create test repo
gh repo create pre-ipo-test-fixtures --private --clone
cd pre-ipo-test-fixtures

# Scenario A: GPL dependency
cat > package.json << 'EOF'
{
  "name": "test-gpl-dep",
  "dependencies": {
    "express": "^4.18.2",
    "readline": "^7.0.0"
  }
}
EOF

# Scenario B: Exposed AWS key (use EXAMPLE key — never real)
cat > config/settings.js << 'EOF'
const AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE";
const AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY";
const API_URL = "https://api.example.com";
EOF

# Scenario C: Financial file
echo "placeholder" > docs/financial_model_q4.xlsx

# Scenario D: PII in test fixtures
cat > tests/fixtures/users.csv << 'EOF'
name,email,ssn
Jane Doe,jane@example.com,123-45-6789
EOF

# Minimal .gitignore (intentionally missing patterns)
echo "node_modules/" > .gitignore

git add -A && git commit -m "test: compliance test fixtures"
git push origin main

# Create PR
git checkout -b test/compliance-scan
echo "// trigger scan" >> config/settings.js
git add -A && git commit -m "test: trigger compliance scan"
git push origin test/compliance-scan
gh pr create --title "Test: Compliance Scan" --body "Testing pre-IPO compliance gate"
```

Note the PR number (e.g., `1`).

### 2b. Test License Scanner Lambda

```bash
# Invoke directly
aws lambda invoke \
  --function-name pre-ipo-license-scanner \
  --payload '{"owner":"YOUR_ORG","repo_name":"pre-ipo-test-fixtures","pr_number":1}' \
  --cli-binary-format raw-in-base64-out \
  /tmp/license_result.json

cat /tmp/license_result.json | python3 -m json.tool
```

**Expected output:**
```json
{
  "statusCode": 200,
  "body": {
    "scan_type": "license_audit",
    "pr_number": 1,
    "findings": [
      {
        "severity": "CRITICAL",
        "dependency": "readline",
        "license": "UNKNOWN",
        "file": "package.json"
      }
    ],
    "summary": {
      "critical_count": 1,
      "verdict": "BLOCKED"
    }
  }
}
```

**Validation checklist:**
- [ ] `statusCode` is 200
- [ ] `scan_type` is "license_audit"
- [ ] `readline` dependency found in findings
- [ ] `verdict` is "BLOCKED" or "REVIEW_REQUIRED" (UNKNOWN license = CRITICAL)
- [ ] All findings have: severity, dependency, version, license, file, ipo_impact, remediation

### 2c. Test Secrets Scanner Lambda

```bash
aws lambda invoke \
  --function-name pre-ipo-secrets-scanner \
  --payload '{"owner":"YOUR_ORG","repo_name":"pre-ipo-test-fixtures","pr_number":1}' \
  --cli-binary-format raw-in-base64-out \
  /tmp/secrets_result.json

cat /tmp/secrets_result.json | python3 -m json.tool
```

**Expected output includes:**
```json
{
  "findings": [
    {"severity": "CRITICAL", "category": "secret", "pattern_matched": "AKIA****XXXX"},
    {"severity": "CRITICAL", "category": "secret", "pattern_matched": "aws_secret_****XXXX"},
    {"severity": "CRITICAL", "category": "financial_data", "file": "docs/financial_model_q4.xlsx"},
    {"severity": "HIGH", "category": "pii", "pattern_matched": "***-**-****"}
  ],
  "gitignore_gaps": ["*.xlsx", "*.pem", "*.key", "financial_model*"],
  "summary": {"verdict": "BLOCKED"}
}
```

**Validation checklist:**
- [ ] AWS key detected with `AKIA****XXXX` redaction (NEVER the real key)
- [ ] .xlsx file flagged as CRITICAL financial_data
- [ ] SSN pattern detected as HIGH pii
- [ ] `.gitignore_gaps` lists missing patterns
- [ ] No actual secret values appear anywhere in output
- [ ] `verdict` is "BLOCKED"

### 2d. Test PR Reporter Lambda

```bash
aws lambda invoke \
  --function-name pre-ipo-pr-reporter \
  --payload '{
    "owner": "YOUR_ORG",
    "repo_name": "pre-ipo-test-fixtures",
    "pr_number": 1,
    "verdict": "BLOCKED",
    "report_markdown": "## 🔒 Test Report\n\n**Verdict:** ⛔ BLOCKED\n\nThis is a test.",
    "create_blocking_issue": true,
    "issue_title": "⛔ Test: Compliance BLOCKED — PR #1",
    "issue_body": "Test blocking issue from compliance gate.",
    "labels": ["compliance:blocked"],
    "send_alert": false
  }' \
  --cli-binary-format raw-in-base64-out \
  /tmp/reporter_result.json

cat /tmp/reporter_result.json | python3 -m json.tool
```

**Validation checklist:**
- [ ] PR comment posted (check GitHub PR — should see compliance report)
- [ ] Blocking issue created (check GitHub Issues tab)
- [ ] Labels applied to PR
- [ ] `audit_id` is a valid UUID
- [ ] S3 audit log written: `aws s3 ls s3://pre-ipo-compliance-audit/audits/ --recursive`
- [ ] Audit JSON contains: audit_id, timestamp, repo, pr_number, verdict

### 2e. Verify S3 Audit Trail

```bash
# List audit records
aws s3 ls s3://pre-ipo-compliance-audit/audits/ --recursive

# Read latest audit record
aws s3 cp s3://pre-ipo-compliance-audit/audits/2026/03/02/AUDIT_ID.json - | python3 -m json.tool
```

---

## Layer 3: Airia Pipeline Tests (Full Agent Chain)

Tests the complete Airia pipeline in the visual editor using mock and real inputs.

### 3a. Smoke Test — Pipeline Execution

1. Open Airia pipeline `Pre-IPO Compliance Gate`
2. Click **Run** / **Test**
3. Paste this input:

```
Analyze this pull request:
Repository: YOUR_ORG/pre-ipo-test-fixtures
PR Number: 1

Scan for license compliance, secrets, financial data, and PII issues.
```

4. Verify the pipeline executes all three agents sequentially
5. Check Airia **Sessions** / **Execution Log** for:
   - [ ] License Audit Agent ran and produced JSON output
   - [ ] Secrets Scanner Agent ran and produced JSON output
   - [ ] Compliance Reporter Agent ran and called pr_reporter tool
   - [ ] Memory Write node stored results

### 3b. Agent-by-Agent Validation

Test each agent individually by running the pipeline with breakpoints or testing
each AI Operation node in isolation.

**Agent 1 (License Audit) — verify:**
- [ ] Called `license_scanner` tool with correct params
- [ ] Output is valid JSON (not markdown-wrapped)
- [ ] Findings array contains expected dependencies
- [ ] Severity classifications match license_policy.yml
- [ ] Summary includes critical_count, high_count, low_count, verdict

**Agent 2 (Secrets Scanner) — verify:**
- [ ] Received Agent 1's JSON output in chat history
- [ ] Called `secrets_scanner` tool
- [ ] Output is valid JSON
- [ ] Secret values are REDACTED (no actual keys in output)
- [ ] Financial files detected by extension
- [ ] .gitignore gaps listed

**Agent 3 (Compliance Reporter) — verify:**
- [ ] Received both Agent 1 and Agent 2 JSON outputs
- [ ] Overall verdict = WORST of both agent verdicts
- [ ] Called `pr_reporter` tool with markdown report
- [ ] Report contains severity tables, remediation steps, audit ID
- [ ] Blocking issue creation triggered for BLOCKED verdict
- [ ] Labels applied correctly

### 3c. Verdict Logic Tests

Run three separate pipeline executions to validate all verdict paths:

| Test | Input | Expected Verdict | Expected Actions |
|------|-------|-----------------|-----------------|
| BLOCKED | PR with GPL dep + AWS key | ⛔ BLOCKED | Comment + Issue + Labels + Alert |
| REVIEW_REQUIRED | PR with LGPL dep only | ⚠️ REVIEW_REQUIRED | Comment + Labels (no issue) |
| PASS | PR with only MIT deps, no secrets | ✅ PASS | Comment + Labels (no issue) |

---

## Layer 4: End-to-End Test (Full Webhook Flow)

Tests the complete production path: GitHub PR event → API Gateway → Airia pipeline → GitHub comment.

### 4a. Prerequisites

- [ ] All 3 Lambdas deployed and tested (Layer 2 passing)
- [ ] Airia pipeline built with 3 agents and tools connected (Layer 3 passing)
- [ ] GitHub webhook configured pointing to API Gateway
- [ ] SNS topic created and subscribed (optional)

### 4b. E2E Test Procedure

**Step 1:** Create a fresh PR with known issues:

```bash
cd pre-ipo-test-fixtures
git checkout -b test/e2e-blocked

# Add GPL dependency
cat > package.json << 'EOF'
{
  "dependencies": {
    "express": "^4.18.2",
    "readline": "^7.0.0"
  }
}
EOF

# Add exposed secret (EXAMPLE key only!)
cat > config/keys.js << 'EOF'
const AWS_KEY = "AKIAIOSFODNN7EXAMPLE";
EOF

# Add financial file
touch docs/cap_table_2026.xlsx

git add -A && git commit -m "test: e2e blocked scenario"
git push origin test/e2e-blocked
gh pr create --title "E2E Test: Should be BLOCKED" --body "Compliance gate e2e test"
```

**Step 2:** Watch for automated response (allow 30–90 seconds):

- [ ] GitHub PR receives a compliance report comment
- [ ] Comment contains severity tables (License + Secrets)
- [ ] Overall verdict is ⛔ BLOCKED
- [ ] Blocking issue created in repo Issues tab
- [ ] PR label `compliance:blocked` applied
- [ ] S3 audit record created

**Step 3:** Create a clean PR:

```bash
git checkout main
git checkout -b test/e2e-pass

cat > src/utils.js << 'EOF'
const API_URL = process.env.API_URL;
module.exports = { API_URL };
EOF

cat > package.json << 'EOF'
{
  "dependencies": {
    "express": "^4.18.2",
    "dotenv": "^16.3.0"
  }
}
EOF

git add -A && git commit -m "test: e2e pass scenario"
git push origin test/e2e-pass
gh pr create --title "E2E Test: Should PASS" --body "Clean PR test"
```

**Step 4:** Verify PASS response:

- [ ] PR receives compliance report comment
- [ ] Verdict is ✅ PASS
- [ ] No blocking issue created
- [ ] PR label `compliance:passed` applied
- [ ] S3 audit record created (even for PASS)

### 4c. Manual Trigger (Alternative to Webhook)

If the webhook isn't configured yet, trigger the pipeline manually:

```bash
python3 scripts/trigger_pipeline.py \
  --gateway-url https://YOUR_API_ID.execute-api.us-east-1.amazonaws.com/prod/compliance \
  --repo YOUR_ORG/pre-ipo-test-fixtures \
  --pr 1
```

---

## Layer 5: Regression & Edge Cases

### 5a. Edge Case Test Matrix

| # | Scenario | Input | Expected | Why It Matters |
|---|----------|-------|----------|----------------|
| 1 | Empty PR (no files changed) | PR with only commit message | PASS, empty findings | Shouldn't crash on empty diff |
| 2 | Binary-only PR | PR with .png, .woff files | PASS, files skipped | Binary files shouldn't trigger secrets scan |
| 3 | Massive PR (100+ files) | PR touching many files | Completes within Lambda 60s timeout | Performance under load |
| 4 | No package.json | PR with only .py files | License: PASS (no manifests) | Missing manifests ≠ failure |
| 5 | Dual copyleft | GPL + AGPL in same PR | BLOCKED, both listed | Both findings reported, not just first |
| 6 | .gitignore already complete | Repo with comprehensive .gitignore | gitignore_gaps = [] | No false positives on gaps |
| 7 | Secrets in comments | `// old key: AKIAIOSFODNN7EXAMPLE` | CRITICAL detected | Comments aren't safe — scanners flag them |
| 8 | Financial file deep in tree | `src/data/archive/old/cap_table.xlsx` | CRITICAL detected | Path depth shouldn't prevent detection |
| 9 | Deleted file in PR | File with status "removed" | Skipped (not scanned) | Don't scan files being deleted |
| 10 | No GitHub token | Lambda env var missing | 500 error with clear message | Graceful failure, not silent pass |

### 5b. Security Validation

**CRITICAL: Run these checks on every test output.**

```bash
# Check that no actual AWS keys appear in any Lambda response
cat /tmp/license_result.json /tmp/secrets_result.json /tmp/reporter_result.json | \
  grep -E "AKIA[0-9A-Z]{16}" && echo "⛔ FAIL: Real AWS key in output!" || echo "✅ PASS: No real keys"

# Check that no actual passwords appear
cat /tmp/secrets_result.json | \
  grep -E "wJalrXUtnFEMI" && echo "⛔ FAIL: Real secret in output!" || echo "✅ PASS: No real secrets"

# Verify all findings use redacted patterns
cat /tmp/secrets_result.json | python3 -c "
import json, sys
data = json.loads(json.loads(sys.stdin.read()).get('body', '{}'))
for f in data.get('findings', []):
    pm = f.get('pattern_matched', '')
    if 'AKIA' in pm and '****' not in pm:
        print(f'⛔ FAIL: Unredacted finding: {pm}')
        sys.exit(1)
print('✅ PASS: All findings properly redacted')
"
```

---

## Troubleshooting

| Symptom | Check | Fix |
|---------|-------|-----|
| Lambda returns 403 | GitHub token expired or wrong scopes | Regenerate token with `repo`, `issues` scopes |
| Lambda returns 404 | Wrong repo name or PR doesn't exist | Verify owner/repo_name/pr_number |
| Lambda timeout (60s) | Large PR with many files | Increase Lambda timeout to 120s or reduce file scan scope |
| Airia agent returns markdown instead of JSON | Prompt not set correctly | Re-paste prompt from `config/airia_agent_prompts.md` — must include "Return ONLY valid JSON" |
| Agent 2 re-analyzes licenses | Chat history passing issue | Verify Agent 2 prompt includes "Do NOT re-analyze licenses" |
| Reporter creates issue on PASS | Verdict logic error in prompt | Verify Agent 3 prompt: "create_blocking_issue: true ONLY if verdict is BLOCKED" |
| No PR comment appears | pr_reporter Lambda error | Check CloudWatch logs: `aws logs tail /aws/lambda/pre-ipo-pr-reporter` |
| S3 audit not written | Bucket permissions | Verify IAM role has `s3:PutObject` on audit bucket |
| SNS alert not sent | Topic ARN not set | Set `SNS_TOPIC_ARN` in Lambda env vars |
| Pipeline runs but no tool calls | Tools not registered in Airia | Re-register Lambda URLs as MCP tools, assign to correct agents |

---

## CI/CD Integration (Optional)

Add unit tests to your CI pipeline:

```yaml
# .github/workflows/test.yml
name: Compliance Gate Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install pytest
      - run: python -m pytest tests/ -v
```
