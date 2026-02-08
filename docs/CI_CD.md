# CI/CD (GitHub Actions)

This repo ships with GitHub Actions workflows under `.github/workflows/`.

## CI (Pull Requests + Push)

`ci.yml` runs:

- `ruff format --check .`
- `ruff check .`
- `mypy diagnostics_lab`
- `pytest`

## Docker Build Check

`docker-build.yml` verifies the Docker image builds on PRs and pushes.

## CD: Docker Image Publishing (GHCR)

`release.yml` publishes a Docker image to GitHub Container Registry when you push a tag like `v0.1.0`.

Image name convention:

- `ghcr.io/<owner>/<repo>/diagnostics-lab-api:<tag>`

### Required GitHub Settings

- Repository permissions: allow GitHub Actions to write packages
- (Optional) protect `main` and require status checks

### Release Steps

```bash
git tag -a v0.1.0 -m "v0.1.0"
git push origin v0.1.0
```

## Docs Deployment (GitHub Pages)

`docs.yml` builds MkDocs and deploys to GitHub Pages on push to `main`.

### Enable Pages

In GitHub repo settings:

- Pages: Source = GitHub Actions

## Dependency Updates

`dependabot.yml` can keep Python deps and GitHub actions updated automatically.
