# CLAUDE.md — Project Guidelines

This file provides instructions for Claude Code when operating in this repository via the Claude Code Action workflow.

## Repository Purpose

This is a **Purple Team-aligned GitHub repository template**. It provides a security-first SDLC skeleton for projects that integrate offensive and defensive security practices throughout the development lifecycle.

## Project Structure

```
/
├── docs/          # Threat models and architecture documentation
├── src/           # Application source code
├── tests/         # Unit and integration tests
├── .github/
│   ├── workflows/ # CI/CD pipelines (Semgrep, Pyre, Claude)
│   └── ISSUE_TEMPLATE/
├── .semgrep.yml   # Custom SAST rules
├── .env.example   # Environment variable template
├── CHANGELOG.md   # Version history
├── SECURITY.md    # Vulnerability reporting policy
└── LICENSE        # MIT License
```

## Development Workflow

1. All work happens on feature branches — never commit directly to `main`.
2. Branch naming: `feature/<issue-number>-short-description` or `fix/<issue-number>-short-description`.
3. Pull Requests require all CI checks to pass before review.
4. Commit messages should be descriptive and reference the related issue where applicable.

## CI/CD Pipelines

| Workflow | Trigger | Purpose |
|---|---|---|
| `semgrep.yml` | Push/PR to main, weekly schedule | SAST scanning |
| `pyre.yml` | Push/PR to main | Python static type checking |
| `claude-action.yml` | `@claude` mentions in issues/PRs | AI-assisted code review |

## Security Practices

- Run `semgrep scan --config .semgrep.yml .` locally before pushing.
- Never commit secrets or credentials — `.gitignore` and Semgrep rules enforce this.
- Report vulnerabilities privately per `SECURITY.md`.
- All dependencies must be pinned to specific versions in CI.

## Allowed Claude Tools (via claude-action.yml)

- `Bash(npm install)` — install Node.js dependencies
- `Bash(npm test)` — run tests
- `Bash(git push:*)` — push branches

## Notes

- This is a template repository. Replace placeholder text in `README.md` with project-specific content when using this template.
- `SECURITY.md` contains a placeholder email (`security@example.com`) — update it with a real contact before publishing.
- Add actual source code to `src/` and tests to `tests/` when implementing a project from this template.
