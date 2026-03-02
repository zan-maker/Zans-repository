# Pre-IPO Compliance Gate — Project Context

## Company Profile
This repository belongs to a pre-IPO company preparing for public listing.
All code, dependencies, and data committed here may be subject to due diligence
review by investment banks, legal counsel, and regulatory bodies.

## Compliance Standards
- **IPO Readiness:** All code must be free of IP encumbrances that would
  require disclosure in S-1/F-1 filings or create material risk.
- **License Policy:** No strong copyleft licenses (GPL, AGPL, SSPL) in
  production dependencies. Weak copyleft (LGPL, MPL) requires legal sign-off.
  Permissive licenses (MIT, Apache-2.0, BSD) are approved.
- **Secrets Policy:** Zero tolerance for hardcoded credentials, API keys,
  private keys, or tokens in any branch. All secrets must use environment
  variables or a secrets manager (e.g., HashiCorp Vault, AWS Secrets Manager).
- **Financial Data Policy:** No financial models, cap tables, term sheets,
  investor communications, or board materials may exist in this repository.
  Financial data belongs in the secure data room only.
- **PII Policy:** No personally identifiable information in code or config.
  Test data must use synthetic/anonymized values.

## Repository Structure
```
├── src/                    # Application source code
├── tests/                  # Test suites
├── docs/                   # Documentation
├── config/                 # Application configuration (no secrets)
├── scripts/                # Build and deployment scripts
├── .gitlab/                # GitLab CI/CD and Duo configuration
│   └── duo/
│       └── agent-config.yml
├── flows/                  # Custom flow definitions
├── AGENTS.md               # This file
└── .gitignore              # Must include sensitive file patterns
```

## Required .gitignore Patterns
The following patterns MUST be present in .gitignore:
```
# Secrets
.env
.env.*
*.pem
*.key
*.p12
*.pfx
*credentials*
*secret*

# Financial data
*.xlsx
*.xls
*.csv
!tests/fixtures/*.csv
financial_model*
cap_table*
term_sheet*
*investor*
*valuation*

# IDE and OS
.idea/
.vscode/
.DS_Store
Thumbs.db
```

## Compliance Labels
- `compliance::passed` — MR cleared all compliance checks
- `compliance::review-required` — MR has HIGH findings needing review
- `compliance::blocked` — MR has CRITICAL findings and cannot merge

## Team Contacts
- **Compliance Officer:** Tag in blocking issues for resolution
- **Legal Counsel:** Required reviewer for any license exception requests
- **CFO/Finance:** Required reviewer if financial data is detected

## Coding Conventions
- Python 3.11+, type hints required
- All dependencies pinned to exact versions
- SPDX license headers in all source files
- No vendored/copied third-party code without license review
