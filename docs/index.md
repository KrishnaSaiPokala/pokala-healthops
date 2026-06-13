# Technical Documentation Appendix

The public front door for this project is the Next.js platform case-study site. This MkDocs area is the engineering appendix: architecture notes, runbooks, evidence links, security boundary, and implementation status.

## Project thesis

Pokala HealthOps is a no-PHI healthcare interface reliability platform. It models a realistic operational failure class: synthetic ORU-style lab messages fail terminology mapping, enter a dead-letter queue, receive remediation, replay safely, pass warehouse checks, and produce an evidence package.

## What this docs site is for

- Architecture and system boundaries
- Incident runbooks
- Evidence and replay verification notes
- Security/no-PHI posture
- Local platform stack notes
- Development and validation commands

## What the flagship site is for

The Next.js site presents the project as a recruiter-readable, staff-engineer style platform case study: reliability control plane, failure model, replay safety, cloud-native local stack, observability, and evidence-driven incident closure.

## Boundary

This is a synthetic portfolio system. It does not claim HIPAA certification, real EHR integration, production hospital deployment, or real patient data processing.
