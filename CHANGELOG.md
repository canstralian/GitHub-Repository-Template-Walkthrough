# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.0] - 2026-03-07

### Added
- `CLAUDE.md` with project guidelines for Claude Code Action workflow integration
- `CHANGELOG.md` to track version history (this file)
- `.env.example` template for environment variable documentation
- Placeholder directories: `docs/`, `src/`, `tests/` with `.gitkeep` files
- Refactored `claude-action.yml` with improved workflow configuration
- Refactored `pyre.yml` for Python 3.11 static type checking
- Updated `semgrep.yml` with optimized SAST scanning configuration

### Changed
- GitHub Actions workflows updated to use latest stable action versions
- Claude Code Action pinned to `anthropics/claude-code-action@v1`
- Pyre and Semgrep actions pinned to specific commit SHAs for supply-chain security

### Fixed
- `claude-action.yml` now correctly references `CLAUDE.md` which is present in the repository
- Workflow configurations aligned with current GitHub Actions runner standards

## [1.0.0] - 2026-03-04

### Added
- Initial repository template structure
- `README.md` with Purple Team-aligned SDLC walkthrough
- `SECURITY.md` with vulnerability reporting policy
- `.semgrep.yml` with 10 custom SAST rules covering Python, JavaScript, GitHub Actions, and secrets
- `.gitignore` with comprehensive patterns for Python, Node.js, IDE, and OS artifacts
- GitHub Issue Templates: bug report and feature request
- GitHub Actions workflow: Semgrep SAST scanning
- GitHub Actions workflow: Pyre Python type checking
- GitHub Actions workflow: Claude Code Action for AI-assisted development
- MIT License

[Unreleased]: https://github.com/canstralian/GitHub-Repository-Template-Walkthrough/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/canstralian/GitHub-Repository-Template-Walkthrough/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/canstralian/GitHub-Repository-Template-Walkthrough/releases/tag/v1.0.0
