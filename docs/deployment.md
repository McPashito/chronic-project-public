# Deployment Guide

This document describes the public portfolio deployment for Chronic Project.

No real secrets are stored in this repository. Environment variable names are documented, but their values must only be configured in the deployment platforms or local ignored files.

## Public Services

- Frontend: Vercel
- Backend API: Render
- Database: Neon PostgreSQL

Current public URLs:

- Frontend: https://chronic-project-public.vercel.app
- Backend: https://chronic-project-public.onrender.com
- API documentation: https://chronic-project-public.onrender.com/docs

Render free instances can spin down after inactivity, so the first request may take longer than usual.

## Environment Variables

Render backend:

```env
DATABASE_URL=
SECRET_KEY=
ALLOW_PUBLIC_REGISTRATION=false
```

Vercel frontend:

```env
VITE_API_BASE_URL=
```

Do not commit `.env`, `.env.public`, database URLs, passwords, JWT secrets or production tokens.

`ALLOW_PUBLIC_REGISTRATION=false` is recommended for the public portfolio demo so visitors cannot create real accounts through Swagger or direct API calls. Local development can keep the default value enabled.

## Backend Deployment

Render service configuration:

```text
Root Directory: backend
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

The deployed frontend origin must be present in the FastAPI CORS allowlist.

## Frontend Deployment

Vercel project configuration:

```text
Root Directory: frontend
Framework Preset: Vite
Build Command: npm run build
Output Directory: dist
```

`VITE_API_BASE_URL` must point to the Render backend base URL, without a trailing endpoint.

## Database Setup

After creating a fresh Neon database, run migrations and seed demo data from the backend environment:

```bash
python -m alembic upgrade head
python scripts/seed_demo_data.py
```

The seed scripts create demo users and artificial glucose records for presentation and testing.

The public demo is intended to be tested with seeded demo accounts only. Do not enter real personal or health-related data.

## Demo Data Refresh

The project includes a script that keeps recent demo records available:

```bash
python scripts/seed_new_glucose_records.py
```

For local maintenance, an ignored `backend/.env.public` file can be used with the public Neon `DATABASE_URL`. The normal `backend/.env` can remain configured for local development.

Example manual workflow from `backend`:

```powershell
Copy-Item .env.public .env
python scripts\seed_new_glucose_records.py
Copy-Item .env.local .env
```

If `.env.local` is not used, restore the local `.env` manually after the refresh.

An automatic Render Cron Job was considered with this command:

```bash
python scripts/seed_new_glucose_records.py
```

It is not enabled in the current free portfolio deployment because Render Cron Jobs add platform cost. The script remains ready if scheduled refresh becomes necessary later.
