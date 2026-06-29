# Chronic Project Frontend

Vue/Vite frontend for Chronic Project.

The full project setup, demo credentials, deployment notes and limitations are documented in the root README files:

- `../README.md`
- `../README.es.md`

## Commands

```bash
npm install
npm run dev
npm run build
```

The frontend reads the backend URL from:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Use `frontend/.env.example` as the local environment template. Do not commit real `.env` files.
