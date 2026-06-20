# GitHub Deployment Guide - FAGE Character Generator

This guide covers deploying the FAGE Character Generator via GitHub, including repository setup, CI/CD, and various deployment platforms.

---

## Table of Contents

1. [GitHub Repository Setup](#github-repository-setup)
2. [Deployment Options](#deployment-options)
3. [GitHub Actions CI/CD](#github-actions-cicd)
4. [Platform-Specific Deployment](#platform-specific-deployment)
5. [Environment Secrets](#environment-secrets)
6. [Best Practices](#best-practices)

---

## GitHub Repository Setup

### 1. Create .gitignore (if not exists)

```bash
# Create comprehensive .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
backend/venv/
backend/env/
backend/.venv
backend/.env
pip-log.txt
.pytest_cache/
.coverage
htmlcov/

# Node.js
frontend/node_modules/
frontend/.cache/
frontend/npm-debug.log*
frontend/yarn-debug.log*
frontend/yarn-error.log*
frontend/pnpm-debug.log*

# Build outputs
frontend/dist/
backend/generated_pdfs/*.pdf
backend/storage/characters/*.json

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
Desktop.ini

# Environment files
.env
.env.local
.env.*.local

# Logs
*.log

# Temporary files
*.tmp
*.temp

# Old files
.old-project-files/

# Claude artifacts
.claude/
EOF
```

### 2. Initialize Git Repository

```bash
# If not already initialized
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: FastAPI + Vue.js FAGE Character Generator

- Complete backend with FastAPI
- Vue.js 3 frontend with Element Plus
- Docker multi-stage build
- PDF export via PyPDFForm (fillable AcroForm)
- Comprehensive documentation"

# Create main branch (if using older Git)
git branch -M main
```

### 3. Create GitHub Repository

**Option A: Via GitHub CLI**
```bash
# Install GitHub CLI: https://cli.github.com/
gh auth login
gh repo create FAGE-pyGenerator --public --source=. --remote=origin --push
```

**Option B: Via GitHub Web**
1. Go to https://github.com/new
2. Repository name: `FAGE-pyGenerator`
3. Description: "Fantasy AGE Character Generator - FastAPI + Vue.js"
4. Choose Public or Private
5. **DON'T** initialize with README (you already have one)
6. Click "Create repository"

### 4. Push to GitHub

```bash
# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/FAGE-pyGenerator.git

# Push to GitHub
git push -u origin main
```

### 5. Create Release Tags

```bash
# Tag the current version
git tag -a v2.0.0 -m "Version 2.0.0 - Initial FastAPI/Vue.js release"

# Push tags
git push --tags
```

---

## Deployment Options

### Option 1: Railway.app (Recommended - Easiest)

**Why Railway:**
- ✅ Free tier available ($5 credit/month)
- ✅ Automatic Docker deployment
- ✅ Built-in PostgreSQL/Redis if needed
- ✅ Custom domains
- ✅ Zero configuration needed

**Steps:**

1. **Create `railway.toml` in project root:**
```toml
[build]
builder = "DOCKERFILE"
dockerfilePath = "Dockerfile"

[deploy]
startCommand = "cd /app/backend && python -m uvicorn main:app --host 0.0.0.0 --port $PORT"
healthcheckPath = "/health"
healthcheckTimeout = 300
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10
```

2. **Deploy:**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Deploy
railway up

# Open in browser
railway open
```

3. **Set environment variables in Railway dashboard:**
   - `PORT` (auto-set by Railway)
   - `CORS_ORIGINS` - Add your Railway URL
   - `LOG_LEVEL=INFO`

### Option 2: Fly.io (Good for global deployment)

**Why Fly.io:**
- ✅ Free tier (3 small VMs)
- ✅ Global edge deployment
- ✅ Built-in PostgreSQL
- ✅ Custom domains

**Steps:**

1. **Create `fly.toml` in project root:**
```toml
app = "fage-generator"
primary_region = "ewr"  # or nearest region

[build]
  dockerfile = "Dockerfile"

[env]
  PORT = "8080"
  LOG_LEVEL = "INFO"

[http_service]
  internal_port = 8080
  force_https = true
  auto_stop_machines = "stop"
  auto_start_machines = true
  min_machines_running = 1
  processes = ["app"]

[[http_service.checks]]
  interval = "10s"
  timeout = "5s"
  grace_period = "30s"
  method = "GET"
  path = "/health"

[[vm]]
  memory = "1gb"
  cpu_kind = "shared"
  cpus = 1
```

2. **Deploy:**
```bash
# Install Fly CLI
# Windows: Use installer from https://fly.io/docs/hands-on/install-flyctl/
# Mac: brew install flyctl
# Linux: curl -L https://fly.io/install.sh | sh

# Login
fly auth login

# Launch app (creates app and fly.toml)
fly launch --no-deploy

# Edit fly.toml as shown above

# Deploy
fly deploy

# Open app
fly open
```

### Option 3: Render.com (Simple, reliable)

**Why Render:**
- ✅ Free tier for web services
- ✅ Auto-deploy from GitHub
- ✅ Built-in PostgreSQL
- ✅ Easy SSL

**Steps:**

1. **Create `render.yaml` in project root:**
```yaml
services:
  - type: web
    name: fage-generator
    env: docker
    dockerfilePath: ./Dockerfile
    dockerContext: .
    healthCheckPath: /health
    envVars:
      - key: PORT
        value: 8000
      - key: LOG_LEVEL
        value: INFO
      - key: PYTHON_VERSION
        value: 3.11
    autoDeploy: true
```

2. **Deploy:**
   - Push code to GitHub
   - Go to https://render.com/
   - Click "New +" → "Web Service"
   - Connect GitHub repository
   - Render auto-detects Dockerfile
   - Click "Create Web Service"

### Option 4: Google Cloud Run (Scalable, serverless)

**Why Cloud Run:**
- ✅ Pay-per-use (very cheap for low traffic)
- ✅ Automatic scaling to zero
- ✅ Fast cold starts
- ✅ Integration with GCP services

**Steps:**

```bash
# Install Google Cloud SDK
# https://cloud.google.com/sdk/docs/install

# Login
gcloud auth login

# Set project
gcloud config set project YOUR_PROJECT_ID

# Build and push to Container Registry
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/fage-generator

# Deploy
gcloud run deploy fage-generator \
  --image gcr.io/YOUR_PROJECT_ID/fage-generator \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 1Gi

# Get URL
gcloud run services describe fage-generator --platform managed --region us-central1 --format 'value(status.url)'
```

### Option 5: DigitalOcean App Platform

**Why DigitalOcean:**
- ✅ $5/month basic plan
- ✅ Automatic scaling
- ✅ Built-in databases
- ✅ Simple interface

**Steps:**
1. Push to GitHub
2. Go to https://cloud.digitalocean.com/apps
3. Click "Create App"
4. Connect GitHub repository
5. Select Dockerfile deployment
6. Configure:
   - Name: fage-generator
   - Region: Nearest to users
   - Size: Basic ($5/month)
7. Add environment variables
8. Deploy

---

## GitHub Actions CI/CD

### Create Continuous Integration Pipeline

**File**: `.github/workflows/ci.yml`

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test-backend:
    name: Test Backend
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Cache Python dependencies
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('backend/requirements.txt') }}

      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt

      - name: Run tests
        run: |
          cd backend
          pytest --cov=. --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./backend/coverage.xml

  test-frontend:
    name: Test Frontend
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json

      - name: Install dependencies
        run: |
          cd frontend
          npm ci

      - name: Build frontend
        run: |
          cd frontend
          npm run build

      - name: Run tests (if configured)
        run: |
          cd frontend
          # npm run test

  build-docker:
    name: Build Docker Image
    runs-on: ubuntu-latest
    needs: [test-backend, test-frontend]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          file: ./Dockerfile
          push: false
          tags: fage-generator:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  lint:
    name: Lint Code
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install linting tools
        run: |
          pip install flake8 black

      - name: Run flake8
        run: |
          cd backend
          flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

      - name: Run black (check only)
        run: |
          cd backend
          black --check .
```

### Create Deployment Pipeline

**File**: `.github/workflows/deploy.yml`

```yaml
name: Deploy to Production

on:
  push:
    tags:
      - 'v*'

jobs:
  deploy-railway:
    name: Deploy to Railway
    runs-on: ubuntu-latest
    if: startsWith(github.ref, 'refs/tags/')

    steps:
      - uses: actions/checkout@v4

      - name: Install Railway CLI
        run: npm install -g @railway/cli

      - name: Deploy to Railway
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
        run: railway up

  deploy-fly:
    name: Deploy to Fly.io
    runs-on: ubuntu-latest
    if: startsWith(github.ref, 'refs/tags/')

    steps:
      - uses: actions/checkout@v4

      - name: Setup Fly.io CLI
        uses: superfly/flyctl-actions/setup-flyctl@master

      - name: Deploy to Fly.io
        env:
          FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
        run: flyctl deploy --remote-only

  create-release:
    name: Create GitHub Release
    runs-on: ubuntu-latest
    if: startsWith(github.ref, 'refs/tags/')

    steps:
      - uses: actions/checkout@v4

      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          files: |
            README.md
            DOCKER-DEPLOYMENT.md
          generate_release_notes: true
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

## Environment Secrets

### Setting up Secrets in GitHub

1. Go to your repository on GitHub
2. Click "Settings" → "Secrets and variables" → "Actions"
3. Click "New repository secret"

**Required secrets for deployment:**

| Secret Name | Value | Used For |
|-------------|-------|----------|
| `RAILWAY_TOKEN` | Railway API token | Railway deployment |
| `FLY_API_TOKEN` | Fly.io API token | Fly.io deployment |
| `DOCKER_USERNAME` | Docker Hub username | Docker Hub push |
| `DOCKER_PASSWORD` | Docker Hub token | Docker Hub push |
| `DIGITALOCEAN_TOKEN` | DO API token | DigitalOcean deployment |

**How to get tokens:**

**Railway Token:**
```bash
railway login
railway whoami --token
```

**Fly.io Token:**
```bash
fly auth token
```

**Docker Hub Token:**
1. Go to https://hub.docker.com/settings/security
2. Click "New Access Token"
3. Copy the token

---

## Best Practices

### 1. Branch Protection

Set up branch protection for `main`:
- Go to Settings → Branches
- Add branch protection rule for `main`
- Enable:
  - Require pull request reviews
  - Require status checks to pass (CI)
  - Require branches to be up to date

### 2. Semantic Versioning

Use semantic versioning for tags:
```bash
git tag -a v2.0.0 -m "Major release: FastAPI + Vue.js"
git tag -a v2.0.1 -m "Bug fix: PDF generation"
git tag -a v2.1.0 -m "New feature: Dark mode"
```

### 3. Changelog

Create `CHANGELOG.md`:
```markdown
# Changelog

## [2.0.0] - 2026-01-28

### Added
- Complete rewrite with FastAPI + Vue.js
- Docker multi-stage build
- PDF export via PyPDFForm (fillable AcroForm)
- Comprehensive documentation

### Changed
- Migrated from R/Shiny to modern stack
- Improved UI with Element Plus

### Removed
- R/Shiny dependencies
- Java runtime requirements
```

### 4. Repository Settings

**Add these files to your repository:**

**`CODE_OF_CONDUCT.md`**:
```markdown
# Code of Conduct

Be respectful and professional in all interactions.
```

**`CONTRIBUTING.md`**:
```markdown
# Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

See [DEVELOPMENT.md](DEVELOPMENT.md) for setup instructions.
```

**`LICENSE`**:
```
MIT License

Copyright (c) 2026 [Your Name]

[Full MIT license text]
```

### 5. GitHub Repository Topics

Add topics to your repository for discoverability:
- `fastapi`
- `vuejs`
- `docker`
- `character-generator`
- `fantasy-age`
- `rpg`
- `tabletop-rpg`
- `pdf-generation`

---

## Quick Start Deployment

### Fastest: Railway (5 minutes)

```bash
# 1. Push to GitHub
git push origin main

# 2. Install Railway CLI
npm install -g @railway/cli

# 3. Login and deploy
railway login
railway init
railway up

# Done! Your app is live
railway open
```

### Alternative: Fly.io (10 minutes)

```bash
# 1. Push to GitHub
git push origin main

# 2. Install and login
# (Install from https://fly.io/docs/hands-on/install-flyctl/)
fly auth login

# 3. Launch
fly launch
# Follow prompts, choose region

# 4. Deploy
fly deploy

# Done!
fly open
```

---

## Troubleshooting

### CI/CD Fails

**Build fails on GitHub Actions:**
- Check workflow logs in "Actions" tab
- Verify all dependencies are in requirements.txt
- Ensure frontend builds without errors

**Docker build timeout:**
- Use GitHub's large runners (paid)
- Or build on deployment platform directly

### Deployment Issues

**Port binding errors:**
- Ensure app uses `$PORT` environment variable
- Platforms inject their own port

**CORS errors:**
- Add deployment URL to `CORS_ORIGINS` in config
- Update environment variables on platform

---

## Monitoring & Maintenance

### After Deployment

1. **Setup monitoring:**
   - Railway: Built-in metrics
   - Fly.io: Built-in metrics + logs
   - External: Sentry for error tracking

2. **Setup alerts:**
   - Health check failures
   - High error rates
   - High memory/CPU usage

3. **Regular updates:**
   ```bash
   # Update dependencies
   pip install --upgrade -r requirements.txt
   npm update

   # Commit and push
   git add .
   git commit -m "chore: Update dependencies"
   git push
   ```

4. **Backup data:**
   - Export character data regularly
   - Store in separate location

---

## Summary

**Recommended deployment path:**

1. ✅ Push code to GitHub
2. ✅ Deploy to Railway (easiest)
3. ✅ Setup GitHub Actions for CI
4. ✅ Configure domain (optional)
5. ✅ Setup monitoring

**Your app will be live in < 10 minutes with Railway!**

For questions or issues, see [README.md](README.md) or create a GitHub issue.

---

**Last Updated**: 2026-01-28
