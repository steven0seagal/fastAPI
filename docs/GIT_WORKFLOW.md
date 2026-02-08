# Git Workflow

## Branching

Recommended default:

- `main`: always green; protected branch
- `feature/<topic>`: feature branches merged via PR
- `fix/<topic>`: bugfix branches merged via PR

## Pull Requests

Suggested PR rules:

- CI must pass (lint, typecheck, tests)
- Review required (if this is a team repo)
- Squash merge to keep history clean (optional)

## Releases

This repo’s default CD pipeline is tag-based:

- Create an annotated tag like `v0.1.0`
- Push the tag
- GitHub Actions builds and publishes a Docker image to GHCR

See `docs/CI_CD.md`.

## Commit Messages

Optional but recommended: Conventional Commits (helps automate changelogs/releases):

- `feat: add sample rejection reasons`
- `fix: handle duplicate barcode correctly`
- `docs: expand CI/CD docs`
