# Sales Data Validation Pipeline

![CI](https://github.com/iimgaurav/sales_pipline/actions/workflows/ci.yml/badge.svg)

Small ETL/validation pipeline. This repo contains scripts to extract, validate, transform and load sales data into SQL Server.

Getting started

Prerequisites
- Python 3.10+ (3.11 recommended)
- ODBC Driver 17 for SQL Server (if you will load to SQL Server)
- Git

Install dependencies
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Configuration
Set these environment variables (defaults are shown):

- `SQL_SERVER` — default `BUNY`
- `SQL_DATABASE` — default `sales_dw`
- `SQL_DRIVER` — default `ODBC Driver 17 for SQL Server`
- `SQL_TRUSTED` — default `yes` (Windows Authentication)
- `SQL_USER`, `SQL_PASSWORD` — when using SQL authentication

Run locally
```powershell
python src/main.py
```

Deployment to GitHub
1. Initialize repo and commit files:
```bash
git init
git add .
git commit -m "Initial pipeline commit"
```
2. Create a remote on GitHub and push:
```bash
git remote add origin git@github.com:YOUR_USER/YOUR_REPO.git
git branch -M main
git push -u origin main
```

CI
A simple workflow is included at `.github/workflows/ci.yml` that installs dependencies and runs a smoke import.

Deployment (via GitHub Actions)

The repository includes a deploy workflow at `.github/workflows/deploy.yml` which copies files to a remote host over SSH and starts the pipeline in a virtual environment.

Set these GitHub Secrets in your repository settings before using the deploy workflow:
- `DEPLOY_HOST` — remote host IP or hostname
- `DEPLOY_USER` — SSH user
- `DEPLOY_PATH` — target directory on remote host
- `DEPLOY_PRIVATE_KEY` — private SSH key (no passphrase recommended for automation)
- `DEPLOY_PORT` — (optional) SSH port, default `22`

To add a secret: Repository -> Settings -> Secrets and variables -> Actions -> New repository secret.

Notes
- The pipeline writes fallback CSVs to `sales_data_pipeline/failed_load/` if DB load fails.
- Keep database credentials out of source control; use GitHub Secrets for CI if needed.