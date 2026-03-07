# Threat Model

> **Stage:** Design — update this document before the Implementation phase begins.

## 1. Scope

| Item | Description |
|------|-------------|
| System | _[Insert system name and brief description]_ |
| Version | _[e.g., v1.0.0]_ |
| Author(s) | _[Names / handles]_ |
| Last Updated | _[YYYY-MM-DD]_ |

## 2. Assets & Trust Boundaries

List the assets worth protecting and draw the trust boundary around them.

| Asset | Classification | Trust Boundary |
|-------|---------------|----------------|
| _[e.g., User credentials]_ | _[Critical/High/Medium/Low]_ | _[e.g., DB layer]_ |

## 3. Threat Actors

| Actor | Motivation | Capability |
|-------|-----------|------------|
| _[e.g., External attacker]_ | _[e.g., Data theft]_ | _[Low/Medium/High]_ |

## 4. Attack Surface & STRIDE Analysis

For each component, enumerate threats using the STRIDE model.

| Component | Threat (STRIDE) | Description | Mitigations |
|-----------|----------------|-------------|-------------|
| _[e.g., Login endpoint]_ | _[e.g., Spoofing]_ | _[Description]_ | _[e.g., MFA, rate limiting]_ |

> **STRIDE:** Spoofing · Tampering · Repudiation · Information Disclosure · Denial of Service · Elevation of Privilege

## 5. Risk Register

| ID | Threat | Likelihood | Impact | Risk Level | Status |
|----|--------|-----------|--------|------------|--------|
| T-001 | _[Threat description]_ | _[L/M/H]_ | _[L/M/H/C]_ | _[Low/Medium/High/Critical]_ | _[Open/Mitigated]_ |

## 6. Mitigations & Controls

| Control | Type | Addresses |
|---------|------|-----------|
| _[e.g., Semgrep SAST scan]_ | _[Preventive/Detective/Corrective]_ | _[e.g., T-001, T-003]_ |

## 7. Residual Risk Sign-off

- [ ] Security lead reviewed
- [ ] All Critical/High risks mitigated or accepted with justification
- [ ] Threat model incorporated into sprint planning
