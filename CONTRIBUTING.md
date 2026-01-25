# Contributing to HealthAid

Thank you for your interest in contributing. HealthAid is currently proprietary software (see `LICENSE`) and contributions are by invitation or under explicit written license from the copyright owner.

This document explains how contributors should report issues, request features, and — where authorized — submit code changes. If you do not have explicit permission to contribute, please open issues or feature requests rather than PRs.

## Quick summary

- Repository status: proprietary, All Rights Reserved (see `LICENSE`).
- Contributions: allowed only with prior written permission from the repository owner.
- To propose changes: open an issue describing the problem or feature; maintainers will respond with next steps.

## How to propose a change (recommended flow)

1. Search existing issues and pull requests to avoid duplicates.
2. Open a new issue describing the bug, feature request, or improvement. Include:
   - A short descriptive title
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Minimal code or screenshots if helpful
   - Environment info (OS, Python/node versions, DB used)
3. Maintainers will review and reply with guidance. If they request a code contribution, they will provide a license/CLA path and desired branch/issue reference.

## Pull requests (only when invited)

If you've been invited to submit a PR, please follow these conventions:

- Branch naming: `feature/<short-descriptor>`, `bugfix/<short-descriptor>`, or `hotfix/<short-descriptor>`.
- Small, focused commits with clear messages.
- Include tests for new behavior or bug fixes.
- Run linters and formatters before opening the PR.

Suggested local checks before creating a PR:

```zsh
# activate your venv
source .venv/bin/activate
pip install -r backend/requirements.txt

# run backend tests
pytest -q

ruff check . || true
# black --check .
```

## Coding style and tests

- Follow the project's existing coding conventions.
- For Python backend: prefer clear typing, small functions, and include unit tests for new logic.
- For frontend: follow existing TypeScript and React patterns used in `frontend/healthaid-frontend`.

## Database migrations

- If your change touches database models, create an Alembic migration under `backend/alembic/versions/`.
- Coordinate with maintainers to avoid concurrent migration conflicts.

## Security reporting

If you discover a security vulnerability, DO NOT open a public issue. Instead contact the repository owner directly with details so the issue can be handled privately. Include steps to reproduce and suggested remediation, if possible.

## Licensing and contributor agreements

This repository is proprietary. By default, contributions are not accepted unless a written license or contributor agreement is provided by the copyright holder. If maintainers request code from you, they will provide guidance on licensing or a Contributor License Agreement (CLA).

## Communication

- For general questions, open an issue.
- For private or legal/licensing matters, contact the repository owner directly.

## Thank you

We appreciate interest and contributions. If you want to help but need a permissive path forward, contact the owner to discuss contributor licensing and a workflow that works for both parties.
