# Test Coverage Analysis

> **Date:** 2026-03-07
> **Scope:** Full repository audit — security rules, CI/CD workflows, template completeness

---

## Executive Summary

This repository is a security-first project template. It ships strong **static analysis infrastructure** (Semgrep, Pyre) but has **zero automated test coverage** of that infrastructure itself. There is also no unit-test framework, no integration tests, and no coverage measurement. The gaps below are ordered by severity.

---

## 1. Critical Gaps

### 1.1 Semgrep Custom Rules Are Untested

**File:** `.semgrep.yml`

The ten custom security rules (Python, JS/TS, GitHub Actions, Secrets) have never been validated. Without test cases:

- A rule could be **syntactically valid but semantically wrong** — silently missing real vulnerabilities (false negatives).
- A rule could **fire on safe code** — generating alert fatigue that trains developers to ignore warnings (false positives).

**Fix implemented:** `tests/semgrep/` directory with four test fixture files and a `# ruleid:` / `# ok:` annotation for every rule. CI workflow `.github/workflows/test-semgrep-rules.yml` runs `semgrep --test` on every push that touches `.semgrep.yml` or the test fixtures.

---

### 1.2 No Unit-Test Framework or Test Directory

**Files missing:** `/tests/__init__.py`, `pytest.ini` / `jest.config.js`, `requirements-dev.txt`

The README promises "unit tests in `/tests`" (line 24) but no test directory, framework, or configuration exists. When implementation code is added there is nothing to test it against.

**Recommended additions:**

```
# Python
tests/
  __init__.py
  unit/
  integration/
pytest.ini               # or pyproject.toml [tool.pytest.ini_options]
.coveragerc              # enforce minimum coverage threshold

# Node.js / TypeScript
jest.config.js
package.json             # devDependencies: jest, @types/jest, ts-jest
```

**Minimum pytest configuration (`pytest.ini`):**

```ini
[pytest]
testpaths = tests
addopts   = --cov=src --cov-report=term-missing --cov-fail-under=80
```

---

### 1.3 CI/CD Has No Test Execution Step

**Files:** `.github/workflows/pyre.yml`, `.github/workflows/semgrep.yml`

Both workflows run static analysis only. There is no workflow that:
- Installs dependencies
- Runs unit tests
- Publishes a coverage report
- Fails the build below a coverage threshold

**Recommended workflow addition:**

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<sha>
      - uses: actions/setup-python@<sha>
        with: { python-version: "3.11" }
      - run: pip install -r requirements.txt -r requirements-dev.txt
      - run: pytest               # exits non-zero if coverage < threshold
      - uses: codecov/codecov-action@<sha>   # or upload SARIF to Security tab
```

---

## 2. Semgrep Rule Quality Issues

### 2.1 `python.yaml-load-requires-safe-loader` — Incorrect Rule Logic

**File:** `.semgrep.yml` lines 39-55

```yaml
patterns:
  - pattern: yaml.load(...)
  - pattern-not: yaml.safe_load(...)
```

The `pattern-not: yaml.safe_load(...)` clause is redundant: `yaml.load()` and `yaml.safe_load()` are different identifiers and can never both match on the same node. The rule will therefore flag **every** call to `yaml.load()` regardless of whether a safe `Loader=` keyword is passed.

**Corrected rule:**

```yaml
patterns:
  - pattern: yaml.load($STREAM, ...)
  - pattern-not: yaml.load($STREAM, Loader=yaml.SafeLoader, ...)
  - pattern-not: yaml.load($STREAM, Loader=yaml.FullLoader, ...)
```

This correctly flags `yaml.load(stream)` and `yaml.load(stream, Loader=yaml.UnsafeLoader)` while allowing `yaml.load(stream, Loader=yaml.SafeLoader)`.

---

### 2.2 Missing High-Value Security Rules

The following OWASP Top-10 / CWE-aligned patterns are absent:

| Pattern | CWE | Severity | Language |
|---|---|---|---|
| `random.random()` / `random.randint()` in security context | CWE-330 | HIGH | Python |
| `hashlib.md5()` / `hashlib.sha1()` | CWE-327 | MEDIUM | Python |
| `open(user_input)` without path sanitisation | CWE-22 | HIGH | Python |
| `requests.get(user_input)` / `urllib.request.urlopen(user_input)` | CWE-918 (SSRF) | HIGH | Python |
| `xml.etree.ElementTree.parse(...)` / `lxml.etree` | CWE-611 (XXE) | HIGH | Python |
| `innerHTML = userInput` | CWE-79 (XSS) | HIGH | JS/TS |
| `__proto__` / `prototype` assignment from user data | CWE-1321 (Prototype Pollution) | HIGH | JS/TS |
| Unsafe `RegExp(userInput)` | CWE-1333 (ReDoS) | MEDIUM | JS/TS |
| `process.env` secrets logged via `console.log` | CWE-532 | MEDIUM | JS/TS |

**Example rule addition (path traversal):**

```yaml
- id: python.path-traversal
  message: "User-controlled path passed to open(). Sanitize with os.path.realpath() and validate the result starts within your expected base directory."
  severity: HIGH
  languages: [python]
  patterns:
    - pattern: open($PATH, ...)
    - pattern-either:
        - pattern-where-python: "isinstance($PATH, ast.Name)"  # variable, not literal
  # A simpler approximation that catches common cases:
  pattern-either:
    - pattern: open($USER_INPUT + $REST, ...)
    - pattern: open(f"...{$USER_INPUT}...", ...)
    - pattern: open("...".format($USER_INPUT), ...)
```

---

### 2.3 Secrets Rules Do Not Cover Common Patterns

The two current secrets rules detect AWS keys and PEM private-key blocks. Missing patterns:

- Generic high-entropy strings assigned to `password`, `secret`, `token`, `api_key` variables
- GitHub personal access tokens (`ghp_...`)
- Slack webhook URLs (`hooks.slack.com/services/...`)
- Database connection strings with embedded credentials
- JWT secrets hardcoded in source

---

## 3. CI/CD Workflow Gaps

### 3.1 `pyre.yml` — Type Errors Do Not Block Merges

Pyre uploads a SARIF report but the workflow step does not fail if type errors are found. A PR with type errors can be merged.

**Fix:** Add `|| exit 1` or configure Pyre's exit code handling:

```yaml
- name: Run Pyre
  run: |
    pyre check
    # pyre exits non-zero on type errors; let that propagate
```

### 3.2 `semgrep.yml` — No Minimum-Rule Coverage Enforcement

Semgrep scans the code but does not enforce a minimum number of rules executed. If someone deletes `.semgrep.yml`, the workflow still passes (using `auto` config).

**Fix:** Ensure the local config is always used:

```yaml
- run: semgrep --config .semgrep.yml --error .
```

### 3.3 `claude-action.yml` — Pinned to Non-SHA Action Refs

The workflow uses `anthropics/claude-code-action@v1`. Per the project's own Semgrep rule (`github-actions.unpinned-action-ref`), all actions should be pinned to a full SHA.

**Fix:**

```yaml
- uses: anthropics/claude-code-action@<full-sha>  # v1
```

### 3.4 `claude-action.yml` — `allowedTools` Restricts to npm Only

The Claude Code action restricts tools to `npm install`, `npm test`, `git push`. If the project uses Python, there is no equivalent `pip install`, `pytest`, or `python` permission.

**Fix:** Expand `allowedTools` based on the project's actual runtime, and document permitted commands in `CLAUDE.md`.

---

## 4. Template Completeness Gaps

### 4.1 No Validation That Placeholders Are Filled

`README.md` contains unfilled template placeholders:
- `[Insert Project Name]` (line 1)
- `[Provide a brief description...]` (line 17)
- `[Your Runtime/Language — e.g., Node.js v20+, Python 3.11+]` (line 32)

A CI check (or a `pre-commit` hook) should fail if these strings still exist in the file.

**Example pre-commit hook (`scripts/check_placeholders.sh`):**

```bash
#!/usr/bin/env bash
set -euo pipefail
if grep -rE '\[Insert |TODO:|FIXME:|your-org|your-repo' README.md; then
  echo "ERROR: Unfilled template placeholders detected in README.md"
  exit 1
fi
```

### 4.2 No `CLAUDE.md` Exists

`claude-action.yml` references `CLAUDE.md` (`"Please analyze the request and follow the project guidelines in CLAUDE.md"`) but the file does not exist. Claude Code will operate without project-specific context.

**Fix:** Create `CLAUDE.md` documenting:
- Project structure and conventions
- Permitted commands and tools
- Security constraints (e.g., never commit secrets, always run Semgrep before pushing)
- Branch and PR naming conventions

---

## 5. Recommended Prioritised Action Plan

| Priority | Area | Action |
|---|---|---|
| P0 | Semgrep rule testing | Run `semgrep --test` in CI (implemented in this PR) |
| P0 | Unit test framework | Add `pytest.ini`, `tests/` structure, and a CI test step |
| P1 | Semgrep rule bugs | Fix `yaml-load` rule logic (see §2.1) |
| P1 | Missing OWASP rules | Add path-traversal, SSRF, XSS, insecure-random rules |
| P1 | Pyre enforcement | Make Pyre failures block merges |
| P2 | Secrets rule expansion | Add GitHub PAT, Slack webhook, hardcoded-password patterns |
| P2 | Coverage threshold | Enforce ≥ 80 % line coverage in CI |
| P2 | Placeholder validation | Add pre-commit hook or CI step |
| P3 | `CLAUDE.md` | Document project conventions for the Claude Code agent |
| P3 | Action SHA pinning | Pin `anthropics/claude-code-action` to a full commit SHA |

---

## Files Added in This Analysis

```
tests/semgrep/
  test_python_security.py   — True-positive + true-negative fixtures for all 5 Python rules
  test_js_security.js       — True-positive + true-negative fixtures for both JS rules
  test_github_actions.yml   — Fixtures for the unpinned-action-ref rule
  test_secrets.txt          — Fixtures for AWS key + private-key-block rules (fake values only)

.github/workflows/
  test-semgrep-rules.yml    — CI workflow: runs semgrep --test on every rule change

docs/
  test-coverage-analysis.md — This document
```
