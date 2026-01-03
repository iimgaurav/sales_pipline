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

Running tests locally

Install dev dependencies and run tests:

```powershell
pip install -r requirements.txt
pytest -q
```

Setting repository secrets

The scheduled run and deploy workflows require repository secrets for database and deploy credentials. Add these in GitHub: Repository -> Settings -> Secrets and variables -> Actions -> New repository secret.

Recommended secrets:
- `SQL_SERVER`, `SQL_DATABASE`, `SQL_USER`, `SQL_PASSWORD`, `SQL_DRIVER`
- `DEPLOY_HOST`, `DEPLOY_USER`, `DEPLOY_PATH`, `DEPLOY_PRIVATE_KEY`, `DEPLOY_PORT`

If you have the GitHub CLI (`gh`) installed and authenticated, you can set a secret from your terminal:

```powershell
gh secret set SQL_PASSWORD --body "your-db-password"
```


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



📦 Sales Data Pipeline — Production-Grade Python ETL

Overview

This repository contains a production-ready, end-to-end data engineering pipeline built using Python and SQL Server, following enterprise ETL best practices.

The pipeline ingests raw sales order data, validates and transforms it, and loads it into SQL Server using a staging → fact table architecture with incremental loading, auditing, CI/CD, and secure deployment.

This project is designed to demonstrate real-world data engineering skills, not just scripting.

Business Problem

Sales order data arrives as flat files and must be:

Validated for quality and structure

Transformed into analytics-ready format

Loaded safely into SQL Server

Rerunnable without creating duplicate data

Automated and monitored

  High-Level Architecture
  
  
                       Raw CSV
                        ↓
                     Python ETL (VS Code)
                      ├── Extract
                      ├── Validate
                      ├── Transform
                      ├── Load
                      ├── Logging & Auditing
                        ↓
                     SQL Server
                      ├── Staging Tables
                      ├── Fact Tables
                      └── Incremental Loads
                     
                     Project Structure
                     sales_pipeline/
                     │
                     ├── data/
                     │   ├── raw/         # Incoming source files
                     │   ├── processed/   # Valid & transformed data
                     │   └── rejected/    # Invalid records for audit
                     │
                     ├── logs/             # Pipeline execution logs
                     │
                     ├── src/
                     │   ├── extract.py   # Raw data ingestion
                     │   ├── validate.py  # Data validation & rejection
                     │   ├── transform.py # Business transformations
                     │   ├── load.py      # SQL Server loading
                     │   └── main.py      # Pipeline orchestration
                     │
                     ├── .github/
                     │   └── workflows/
                     │       ├── ci.yml
                     │       ├── scheduled_run.yml
                     │       └── deploy.yml
                     │
                     └── README.md

Pipeline Flow (Step by Step)
1. Extract — Raw Ingestion

Reads CSV data from source

Validates file existence and record count

No transformations applied

Why: Raw data must remain unchanged for traceability.

2. Validate — Data Quality Gate

Checks critical columns for nulls

Enforces data types (int, float, date)

Segregates invalid records into a rejected dataset

Why: Bad data should never reach analytical systems.

3. Transform — Business Logic (Silver Layer)

Standardizes text fields (country, status, deal size)

Adds derived columns:

order_year

order_month

revenue_bucket

Adds audit metadata

Why: Analytical systems require consistent, enriched data.

4. Load — SQL Server Integration

Loads data into staging tables via Python

SQL Server handles movement into fact tables

Enforces duplicate prevention logic

Why: Separation of ingestion and business logic improves reliability.

5. Incremental Load & Idempotency

Each run is tagged with a unique batch_id

Staging table is truncated before load

Fact table insert uses NOT EXISTS to prevent duplicates

Result:
The pipeline can be safely rerun without data corruption.

SQL Design
Staging Table

Accepts raw transformed data

No primary keys or constraints

Fact Table

Optimized for analytics

Contains audit columns

Duplicate-safe inserts

CI/CD & Automation
Continuous Integration

Flake8 linting

Unit tests

Triggered on push and pull requests

Scheduling

Daily automated run via GitHub Actions

Runs at 02:00 UTC

Deployment

SSH-based deployment workflow

Secure secrets managed via GitHub Actions

Security & Configuration

All sensitive values are managed using GitHub Actions Secrets:

SQL Access

SQL_SERVER

SQL_DATABASE

SQL_USER

SQL_PASSWORD

Deployment

DEPLOY_HOST

DEPLOY_USER

DEPLOY_PATH

DEPLOY_PRIVATE_KEY

DEPLOY_PORT

No secrets are hardcoded in the repository.

Failure & Recovery Strategy
Scenario	Handling
Empty source file	Pipeline fails early
Invalid records	Redirected to rejected dataset
Partial load failure	Safe rerun using staging
Duplicate data risk	Prevented via incremental logic
How to Run Locally
pip install -r requirements.txt
python src/main.py

Key Engineering Takeaways

Validation before transformation

Staging before fact tables

Incremental loads are mandatory

Auditability enables trust

Automation is part of data engineering

Why This Project Matters

This pipeline reflects how production data systems are actually built, combining:

Data Engineering

Software Engineering

DevOps Practices

It is designed to be maintainable, scalable, and interview-ready.
