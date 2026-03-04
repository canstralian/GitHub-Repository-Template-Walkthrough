# CLAUDE.md — AI Assistant Guide

This file provides context for AI assistants (such as Claude Code) working in this repository.

## Repository Purpose

This is a **GitHub Repository Template Walkthrough** — a reference skeleton demonstrating Purple Team-aligned security practices integrated throughout the Software Development Life Cycle (SDLC). It is designed to be forked and customized as the starting point for new projects that treat security as a first-class concern rather than an afterthought.

Key philosophy: **offensive discovery informs defensive hardening** at every SDLC stage.

---

## Repository Structure

```
.
├── .github/
│   └── ISSUE_TEMPLATE/
│       ├── bug_report.md        # Standard bug report template
│       └── feature_request.md   # Feature request template
├── .gitignore                   # Python-primary, with JS/TS and tooling exclusions
├── .semgrep.yml                 # Custom SAST rules (Python + JS/TS + secrets)
├── LICENSE                      # Project license
├── README.md                    # Project overview and setup guide
└── SECURITY.md                  # Vulnerability disclosure policy
```

### Conventional directories (not yet created — add when implementing a real project):

| Directory   | Purpose |
|-------------|---------|
| `/src`      | Application source code |
| `/tests`    | Unit and integration tests |
| `/docs`     | Architecture diagrams and threat models |
| `/.github/workflows/` | GitHub Actions CI/CD pipelines |

---

## SDLC Stages and Their Artifacts

This template enforces a 6-stage SDLC. AI assistants should respect these stage boundaries:

| Stage | Owner Artifacts |
|-------|----------------|
| **Planning** | GitHub Issues, Project Boards |
| **Design** | `/docs` — threat models, architecture diagrams |
| **Implementation** | `/src` — source code following `.editorconfig` standards |
| **Testing** | `/tests` — unit tests; GitHub Actions for SAST/DAST |
| **Deployment** | GitHub Actions CI/CD; branch protection on `main` |
| **Maintenance** | Dependabot; telemetry; log review |

---

## Security Tooling

### Semgrep (`.semgrep.yml`)

Custom SAST rules are defined locally and run via `semgrep scan --config auto .`. Current rule coverage:

**Python — HIGH severity:**
- `python.no-eval-or-exec` — blocks `eval()` / `exec()`
- `python.no-pickle-deserialization` — blocks `pickle.load(s)` on untrusted data
- `python.yaml-load-requires-safe-loader` — enforces `yaml.safe_load()`
- `python.subprocess-shell-true` — flags `shell=True` subprocess calls

**Python — MEDIUM severity:**
- `python.sql-string-concat-in-execute` — flags string-formatted SQL (injection risk)

**JavaScript / TypeScript — HIGH severity:**
- `js.no-eval-or-new-function` — blocks `eval()` and `new Function()`
- `js.child-process-exec` — flags all `child_process` exec/spawn calls

**GitHub Actions — MEDIUM severity:**
- `github-actions.unpinned-action-ref` — flags `@main`, `@master`, `@HEAD` action refs

**Secrets detection — HIGH/CRITICAL:**
- `secrets.aws-access-key-id` — detects AWS AKIA key patterns
- `secrets.private-key-block` — detects PEM private key blocks

**All rules exclude:** `node_modules/`, `dist/`, `build/`, `.venv/`, `venv/`, `__pycache__/`, `vendor/`, `coverage/`

> When writing or reviewing code, do not introduce patterns that would trigger these rules. If a flagged pattern is genuinely needed, add an explicit inline suppression comment with justification.

---

## Development Conventions

### Branching

- Feature branches: `feature/issue-<number>` (e.g., `feature/issue-42`)
- Claude/AI branches: `claude/<description>-<session-id>`
- Never push directly to `main`. All changes go through a PR with passing CI checks.

### Commit Style

Write concise, imperative commit messages describing *why* the change was made:
```
Add SAST rule for SQL injection via f-string
Fix: enforce yaml.safe_load across all loaders
```

### Pull Requests

Every PR must pass all branch protection status checks before merging:
- CodeQL analysis
- Semgrep scan
- Unit tests

### Secrets Management

- Never commit `.env` files (excluded by `.gitignore`)
- Store secrets in GitHub Secrets for CI/CD use
- Rotate any credentials that appear in git history immediately

---

## Pre-commit Hooks

Install pre-commit hooks to catch issues before they reach the repository:

```bash
pip install pre-commit
pre-commit install
```

This enforces baseline code quality and prevents secret leakage at commit time.

---

## Local Security Testing

### Defensive (SAST)

```bash
semgrep scan --config auto .
```

### Offensive sweep (DAST via OWASP ZAP)

Requires a locally running server (default port 8080):

```bash
docker run -t owasp/zap2docker-stable zap-baseline.py -t http://host.docker.internal:8080
```

---

## Issue Templates

| Template | Use case |
|----------|----------|
| `bug_report.md` | Reproducing bugs with steps, environment, and screenshots |
| `feature_request.md` | Proposing new features with problem/solution/alternatives |

Security vulnerabilities must **not** be reported via public GitHub issues. See `SECURITY.md`.

---

## Security Policy Summary (`SECURITY.md`)

- Supported version: **1.1.x** (1.0.x and below are unsupported)
- Report privately via email (not public issues)
- Required report fields: description, impact, steps to reproduce, suggested fix
- Response SLA: acknowledgment within 48 hours, coordinated disclosure after patch

---

## `.gitignore` Coverage

The `.gitignore` is Python-primary and also covers:
- Build artifacts: `build/`, `dist/`, `*.egg-info/`
- Virtual environments: `.venv/`, `venv/`, `env/`
- Test/coverage output: `.pytest_cache/`, `htmlcov/`, `coverage.xml`
- Secrets: `.env`, `.envrc`
- Package manager lock alternatives: `Pipfile.lock`, `poetry.lock`, `pdm.lock`, `pixi.lock` (commented out — uncomment to ignore)
- Editor tooling: `.ruff_cache/`, `.mypy_cache/`, `.pytype/`
- AI editor configs: `.cursorignore`, `.cursorindexingignore`

---

## Key Constraints for AI Assistants

1. **Do not add patterns** that trigger `.semgrep.yml` rules (eval, pickle, shell=True, raw SQL formatting, hardcoded secrets, unpinned Actions).
2. **Do not commit secrets** — check `.gitignore` before staging any configuration files.
3. **Respect SDLC boundaries** — design changes belong in `/docs`, code in `/src`, tests in `/tests`.
4. **Pin GitHub Actions** by SHA or version tag, never `@main`/`@master`/`@HEAD`.
5. **Use parameterized queries** for all database interactions.
6. **Branch naming** for AI work: `claude/<short-description>-<session-id>`.
7. **All pushes** go to the designated feature branch; never force-push or push directly to `main`.
