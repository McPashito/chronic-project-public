# AGENTS.md — Chronic Project

## Project overview

Chronic Project is a full-stack web application for glucose tracking.

It was originally developed as a DAW final project and may be prepared as a public portfolio project for a junior backend/full-stack developer profile.

Main stack:

- Backend: Python, FastAPI, Pydantic, SQLAlchemy, Alembic, PostgreSQL, JWT, Passlib/bcrypt.
- Frontend: Vue.js, JavaScript, Vite, Vue Router, HTML and CSS.
- Database: PostgreSQL.
- Tooling: Swagger UI, GitHub, VS Code.
- Deployment target: backend on a cloud platform such as Render/Railway/Fly.io, frontend on Vercel/Netlify, database on Neon/Supabase.

Main implemented areas may include:

- User registration.
- Login with JWT.
- Hashed passwords.
- Protected routes.
- Glucose CRUD.
- User-owned records.
- Date and moment-of-day filters.
- Dashboard/summary.
- Standard/premium user logic.
- User profile.
- Password change.
- Dark mode.
- Responsive design.

If the current repository only contains the backend or only contains the frontend, apply only the relevant instructions.

---

## Purpose of this file

This file gives AI coding agents and future collaborators stable project instructions.

It is safe to keep this file public if desired. It does not contain private strategy, personal notes, secrets or internal portfolio planning.

Private strategy and learning notes belong in `.codex-private.md`, which must not be committed.

---

## Core working principles

When working on this repository:

1. Make small, safe, reviewable changes.
2. Do not rename files, routes, functions, variables, components or CSS classes without explicit approval.
3. Do not change the project architecture unless explicitly requested.
4. Do not invent features that are not present in the codebase.
5. Do not introduce new dependencies without explaining why they are needed.
6. Do not create or modify database migrations unless explicitly requested.
7. Do not modify authentication, authorization or user-data isolation casually.
8. Do not touch real `.env` files, secrets, tokens or credentials.
9. Avoid broad automatic formatting that creates noisy diffs.
10. If the task is ambiguous, audit first and ask before editing.

The goal is not to make the project perfect. The goal is to keep it stable, understandable, presentable and realistic for a junior portfolio.

---

## Expected AI workflow

Before editing files:

1. Inspect the relevant files.
2. Explain what you found.
3. Describe the proposed change.
4. List the files you expect to modify.
5. Ask for approval if the change is broad, risky or ambiguous.

When editing files:

1. Keep the scope narrow.
2. Preserve existing naming unless explicitly approved otherwise.
3. Avoid unrelated code movement.
4. Avoid unrelated visual redesign.
5. Keep the app runnable.

After editing files:

1. Summarize what changed.
2. List modified files.
3. Explain how to test the change.
4. Mention commands or tests run.
5. Mention anything that could not be verified.

---

## Backend commands

Typical local backend command:

```bash
uvicorn app.main:app --reload
```

Install backend dependencies:

```bash
pip install -r requirements.txt
```

Run tests if tests exist:

```bash
pytest
```

Do not overwrite `.env`. Use `.env.example` for documentation.

---

## Frontend commands

Typical local frontend commands:

```bash
npm install
npm run dev
npm run build
```

If linting or tests exist, use the project-defined commands from `package.json`.

Do not modify production environment variables directly. Use `.env.example` for documentation.

---

## Security rules

This project handles health-related data in an academic context, so security-sensitive areas must be treated carefully.

Do not expose:

- `.env` files.
- Secret keys.
- Database URLs.
- Real passwords.
- JWT secrets.
- Production tokens.
- Private credentials.
- Real user health data.

Use demo users only when they are intentionally created for demonstration.

Authentication and authorization rules:

- Passwords must remain hashed.
- JWT must not contain medical data.
- Protected routes must continue to filter data by authenticated user.
- A user must never be able to access another user's glucose records.
- Do not weaken 401/403/404 behavior without explicit approval.

---

## Documentation style

When creating or editing documentation:

- Be clear and honest.
- Do not oversell the project.
- Describe it as an academic full-stack project with realistic architecture.
- Do not present it as a certified medical product.
- Mention limitations clearly.
- Prefer concise technical explanations.
- Avoid marketing exaggeration.

Recommended README focus:

1. What the project does.
2. Stack.
3. Main features.
4. Architecture.
5. Installation.
6. Environment variables.
7. Demo users.
8. Screenshots.
9. Technical decisions.
10. Future improvements.

---

## Portfolio preparation rules

If preparing this project for portfolio use, prioritize:

1. Stable local execution.
2. Visual polish for main screens.
3. Responsive and ultrawide checks.
4. Strong README.
5. Safe `.env.example` files.
6. Screenshots.
7. Demo or video link.
8. Basic tests.
9. GitHub Actions only after the app is stable.

Avoid:

- Large refactors.
- New major features.
- Cosmetic rewrites that risk breaking the app.
- Experimental public commits.
- Unnecessary complexity.

---

## Visual polish rules

For frontend visual improvements:

1. Prefer layout constraints, max-widths, spacing and responsive adjustments over structural rewrites.
2. Do not redesign the application unless explicitly requested.
3. Do not change the color palette unless explicitly requested.
4. Do not remove dark mode support.
5. Check desktop, ultrawide, tablet and mobile portrait.
6. Avoid mobile landscape unless explicitly requested.
7. Preserve existing component names and file names.

---

## Teaching mode

The user wants to learn how to work with AI coding agents.

When proposing changes, explain:

- What problem is being solved.
- Why the change is useful.
- What files are affected.
- How to review the diff.
- How to test the result.
- How to commit the change cleanly.

Use a practical junior-friendly style.

The AI proposes.
The user reviews.
The user decides.
