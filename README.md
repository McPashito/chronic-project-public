# Chronic Project

English · [Español](README.es.md)

Full-stack glucose tracking app built with FastAPI, PostgreSQL and Vue.

Chronic Project is a full-stack academic web application for glucose tracking.

It was developed as a DAW final project and is being prepared as a public portfolio project for a junior backend / full-stack developer profile. The goal is to show a realistic web application with authentication, protected data, PostgreSQL persistence, business rules, responsive frontend views and demo data that can be deployed and tested.

> This is an academic project. It is not a certified medical product and must not be used as medical advice, diagnosis or treatment software.

## Project Background

Chronic Project started from a common problem in chronic care: patients often need to record health measurements, keep information organized and bring a readable history to follow-up appointments.

The original idea was broader and included chronic conditions such as diabetes, hypertension and dyslipidemia. For this version, the scope was intentionally reduced to the glucose tracking module. This made it possible to build a complete and coherent MVP while keeping the architecture ready for future modules such as blood pressure, medication, appointments or reports.

The development followed an incremental approach: first a simple working version, then a technically correct version, and finally a clearer and more usable interface.

## Main Features

- Backend user registration endpoint and login with JWT.
- Public demo self-registration can be disabled by environment variable.
- Password hashing with Passlib/bcrypt.
- Password length validation from 8 to 72 characters.
- Login rate limiting for repeated failed attempts.
- Protected private routes.
- Glucose record CRUD.
- User-owned records: each user can only access their own glucose records.
- Date filters and moment-of-day filters.
- Dashboard and summary cards.
- Standard/Premium demo account logic:
  - Standard users can only access recent history.
  - Premium users can access full history.
- User profile and password change.
- Dark mode in the private area.
- Responsive frontend for desktop, tablet and mobile.
- API/Pydantic validation errors normalized into readable frontend messages.
- Backend test suite for authentication, users, glucose records and ownership rules.
- Demo data scripts for local testing and portfolio deployment.

## Tech Stack

**Backend**

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic
- PostgreSQL
- JWT authentication
- Passlib/bcrypt

**Frontend**

- Vue.js
- Vite
- Vue Router
- JavaScript
- HTML and CSS

**Database**

- PostgreSQL

## Project Structure

```text
chronic-project/
|-- backend/
|   |-- app/
|   |   |-- api/routes/
|   |   |-- core/
|   |   |-- db/
|   |   |-- models/
|   |   `-- schemas/
|   |-- alembic/
|   |-- scripts/
|   |-- alembic.ini
|   `-- requirements.txt
|-- frontend/
|   |-- src/
|   |   |-- components/
|   |   |-- layouts/
|   |   |-- router/
|   |   |-- services/
|   |   `-- views/
|   |-- package.json
|   `-- vite.config.js
`-- README.md
```

## Local Setup

### 1. Clone The Repository

```bash
git clone <repository-url>
cd chronic-project
```

### 2. Backend Setup

```bash
cd backend
python -m venv .venv
```

Activate the virtual environment.

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a local `.env` file using the example:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Configure your local PostgreSQL connection in `backend/.env`.

Apply database migrations:

```bash
alembic upgrade head
```

Run the backend:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

### 3. Frontend Setup

Open a second terminal:

```bash
cd frontend
npm install
```

Create a local `.env` file using the example:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Run the frontend:

```bash
npm run dev
```

The frontend will usually be available at:

```text
http://localhost:5173
```

## Environment Variables

### Backend

See `backend/.env.example`.

```env
DATABASE_URL=postgresql://user:password@localhost:5432/chronic_project_db
SECRET_KEY=change-this-secret-key
ALLOW_PUBLIC_REGISTRATION=true
```

`ALLOW_PUBLIC_REGISTRATION` can be set to `false` in a public demo deployment to
block `POST /auth/register` while keeping local development and tests able to use
the registration flow.

### Frontend

See `frontend/.env.example`.

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Real `.env` files are intentionally ignored by Git and must not be committed.

## Demo Data

The project includes demo seed scripts to make local testing and portfolio deployment easier.

Public self-registration is intentionally disabled in the deployed portfolio demo because the
application deals with health-related data. This avoids collecting real personal or medical data
from visitors. The backend still includes the registration endpoint as part of the authentication
flow, and developers can test it locally with their own database and environment variables.
In production, the deployed backend should set `ALLOW_PUBLIC_REGISTRATION=false`.

From the `backend` folder, after running migrations:

```bash
python scripts/seed_demo_data.py
```

This creates:

- demo standard users;
- demo premium users;
- old glucose records without `moment_of_day`;
- newer glucose records with `moment_of_day`;
- varied glucose values so the UI can show low, in-range, elevated and high states.

Demo credentials:

```text
standard1@demo.com / Demo1234!
premium1@demo.com  / Demo1234!
```

Available demo accounts:

```text
standard1@demo.com ... standard10@demo.com
premium1@demo.com  ... premium10@demo.com
```

The seed scripts are designed for demo environments. They should not be used with real user data.

## Useful Backend Commands

Run migrations:

```bash
alembic upgrade head
```

Create demo data:

```bash
python scripts/seed_demo_data.py
```

Refresh only newer demo glucose records:

```bash
python scripts/seed_new_glucose_records.py
```

Run the API:

```bash
uvicorn app.main:app --reload
```

Run backend tests:

```bash
pytest
```

## Useful Frontend Commands

Install dependencies:

```bash
npm install
```

Run development server:

```bash
npm run dev
```

Build for production:

```bash
npm run build
```

## API Overview

Main public endpoints:

- `GET /`
- `GET /health`
- `POST /auth/register`
- `POST /auth/login`

Main protected endpoints:

- `GET /users/me`
- `PUT /users/edit_user`
- `PUT /users/change_password`
- `POST /glucose-records/`
- `GET /glucose-records/`
- `GET /glucose-records/summary`
- `GET /glucose-records/{record_id}`
- `PUT /glucose-records/{record_id}`
- `DELETE /glucose-records/{record_id}`

Authentication uses a JWT bearer token:

```text
Authorization: Bearer <token>
```

Login uses OAuth2 form data, so the frontend sends the email in the `username` field.

## Technical Decisions

### User-Owned Records

The frontend never sends `user_id` when creating glucose records. The backend obtains the current user from the JWT token and assigns ownership server-side.

All glucose record queries filter by the authenticated user, preventing one user from accessing another user's data.

### `moment_of_day` As An Evolutionary Field

The project originally stored glucose records without `moment_of_day`. Later, the field was added through an Alembic migration.

The database allows `moment_of_day` to be `NULL` so old records remain valid. New records require `moment_of_day` through Pydantic validation.

This keeps backwards compatibility while improving data quality for future records.

### Standard/Premium Demo Logic

The application includes simple account-type logic:

- Standard users can consult recent records.
- Premium users can consult the full history.

There are no real payments. This is a portfolio feature to demonstrate business rules and authorization logic.

### Demo Registration Policy

The backend includes a real registration endpoint and keeps it enabled by default for local development and automated tests.

For the public portfolio deployment, registration is disabled with `ALLOW_PUBLIC_REGISTRATION=false`. This prevents visitors from creating accounts or entering real health-related data through Swagger or direct API calls. Demo access is provided through seeded accounts with artificial data.

### Validation And Error Messages

The backend validates passwords, glucose values, dates and request payloads with Pydantic. The frontend normalizes API validation errors so users see readable messages instead of raw objects.

### Visual Simplicity

The UI intentionally prioritizes readable cards, filtered tables and clear forms instead of complex charts. This keeps the interface accessible and easier to use for a broad audience.

Charts and exports are left as future improvements.

## Deployment Notes

Current public deployment:

- Frontend: Vercel - https://chronic-project-public.vercel.app
- Backend: Render - https://chronic-project-public.onrender.com
- Database: Neon PostgreSQL

Required environment variable names, without values:

- Render backend: `DATABASE_URL`, `SECRET_KEY`
- Vercel frontend: `VITE_API_BASE_URL`

Backend production command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Before first use in a deployment database:

```bash
alembic upgrade head
python scripts/seed_demo_data.py
```

Demo data can be refreshed manually from a local environment configured with the public database URL:

```bash
python scripts/seed_new_glucose_records.py
```

An automatic daily Render Cron Job was considered, but it is not enabled in the free portfolio deployment because it adds platform cost. The refresh script is kept ready for that scenario.

If the deployed frontend uses a new domain, the backend CORS configuration must allow that origin.

More details: [Deployment Guide](docs/deployment.md).

## Current Limitations

- This is not a medical device or certified health application.
- No real payment system is implemented.
- Password recovery by email is not implemented.
- Charts and CSV/PDF exports are future improvements.
- Frontend automated tests are not included yet; the frontend is verified with production builds and manual checks.
- Demo data is artificial and only intended for testing and presentation.
- Public self-registration is disabled in the deployed demo to avoid collecting real health-related data.

## Future Improvements

- GitHub Actions for backend tests and frontend build checks.
- Frontend unit tests for API error formatting and key form behavior.
- Password recovery flow.
- Chart-based glucose trends.
- CSV/PDF export.
- Extend the same module pattern to other chronic-care measurements, such as blood pressure or lipid-related records.
- Evolve the project into a unified chronic-care tracking application while keeping each module simple and independently maintainable.
- More flexible account roles.
- Deployment pipeline and CI checks.
- More detailed accessibility audit.
