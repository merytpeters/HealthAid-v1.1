# HealthAid (v1.1)

Comprehensive health dashboard and organization management platform.

This repository contains a FastAPI backend (with Alembic migrations) and a Vite + React TypeScript frontend. It includes a Docker Compose setup for local development and convenience scripts for environment/secret generation and migrations.

---

## Table of contents

- Project overview
- Tech stack
- Architecture & layout
- Quick start (dev)
	- Backend
	- Frontend
	- Docker (all-in-one)
- Configuration & environment variables
- Database migrations (Alembic)
- Running tests
- Development notes & helpful scripts
- Contract, edge cases & troubleshooting
- Contributing
- License

---

## Project overview

HealthAid is a web application that provides organization and dashboard management for healthcare-related workflows. The backend is implemented with FastAPI and persistent storage managed via SQLAlchemy + Alembic migrations. The frontend is a modern React + TypeScript app bootstrapped with Vite.

This repository collects both backend and frontend code to make local development and deployment simple.
This project is an improvement of [Version 1](https://github.com/merytpeters/Healthaid).

## Features (planned / in development)

HealthAid aims to provide a personal health management suite with the following features:

- Dashboard for personal health metrics (vitals, trends, charts, custom widgets).
- Symptom checker to help users triage symptoms and suggest possible actions or next steps.
- Drug–drug and drug–food interaction checker to identify potential interactions and provide guidance.
- Health journal / notes for tracking moods, symptoms, medications, and lifestyle changes over time.
- First-aid guide powered by AI: conversational guidance for common first-aid scenarios and step-by-step instructions.
- User and organization management (roles, dashboards, admin tools).

These features may be implemented incrementally. Some components (for example the AI-powered first-aid guide) will rely on external AI services or local models — configuration details will be added to the backend docs when those components are implemented.

### Privacy & safety notes

- HealthAid deals with sensitive health-related information. Treat all health data as private: store it securely and minimize retention where possible.
- The AI first-aid guidance is intended to assist, not replace, professional medical advice. Provide clear disclaimers in the UI and logs.
- If you plan to deploy this publicly, ensure you review local regulations (HIPAA, GDPR, etc.) and implement appropriate security controls (encryption at rest/in transit, access controls, audit logging).

## Tech stack

- Backend: Python 3.12+, FastAPI
- Migrations: Alembic
- Frontend: React + TypeScript, Vite
- Dev tools: pytest for tests, uvicorn for running the FastAPI app locally
- Containerization/orchestration: Docker & docker-compose

## Repository layout

Top-level layout (important folders/files):

- `backend/` — FastAPI server, DB session helpers, Alembic config and migrations
	- `main.py` — application entry (ASGI) used by uvicorn
	- `run.py` — convenience runner
	- `requirements.txt` — Python dependencies for backend
	- `secret_gen.py` — helper to generate secret(s) required by the app
	- `alembic/` — migration config and `versions/` with migration files
- `frontend/healthaid-frontend/` — Vite + React TypeScript frontend
- `docker-compose.yml` — multi-service dev or demo composition
- `tests/` — backend tests (pytest)

There is also a virtualenv folder `healthaid_venv/` checked into the repo — you can either use this or create your own venv locally.

## Quick start (development)

Prerequisites

- macOS (works on Linux/Windows with minor adjustments)
- Python 3.12 (project uses 3.12 in the provided virtualenv)
- Node.js + npm or yarn (for frontend)
- Docker & docker-compose (optional but recommended for full-stack run)

If you prefer to use the included virtualenv, skip the `python -m venv` step and activate `healthaid_venv` instead.

1) Backend: create/activate virtualenv and install

```zsh
# create a venv (skip if you want to use the provided `healthaid_venv`)
python3 -m venv .venv
source .venv/bin/activate

# or activate provided venv
source healthaid_venv/bin/activate

pip install -r backend/requirements.txt
```

2) Database and migrations

The backend uses Alembic for DB migrations. Configure your DB connection string via environment variables (see next section). Then run:

```zsh
# run migrations
cd backend
alembic upgrade head
```

3) Start backend (dev)

From repository root (with your venv active):

```zsh
# run with uvicorn (reload enabled for development)
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Open: http://localhost:8000

API docs are available at `/docs` (Swagger UI) and `/redoc` (ReDoc) when the server is running.

4) Frontend: start dev server

```zsh
cd frontend/healthaid-frontend
npm install
npm run dev
```

By default the Vite dev server runs on port 5173; the frontend will talk to the backend API (update the base API URL in `src` if needed).

5) Full stack with Docker Compose (optional)

With Docker installed you can run the full stack via docker-compose:

```zsh
docker-compose up --build
```

This will build images and start services defined in `docker-compose.yml`. Check the file for ports and service names.

## Configuration & environment variables

The backend reads configuration values from environment variables. Typical settings:

- DATABASE_URL — SQLAlchemy / Alembic DB URL
- SECRET_KEY — application secret used for session/auth signing
- OTHER settings — check `backend/app/core/config.py` for authoritative list

Create a `.env` file in the `backend/` folder (if you prefer) and load it in your shell or use a tool like `direnv`.

Example `.env` (replace placeholders):

```text
DATABASE_URL=postgresql://user:password@localhost:5432/healthaid_db
SECRET_KEY=some-long-random-secret
```

There is a `backend/secret_gen.py` script that can help generate secure secrets for you; run it and copy the value to your env.

## Database migrations (Alembic)

- New migration (after changing models):

```zsh
cd backend
alembic revision --autogenerate -m "describe change"
alembic upgrade head
```

- Migration files are under `backend/alembic/versions/`.

Be careful when editing migrations; follow your team's branching/migration workflow to avoid conflicts.

## Running tests

Backend tests use `pytest` and are located in `tests/`.

```zsh
source .venv/bin/activate   # or `healthaid_venv` activation
pytest -q
```

Add tests for new features and aim for small, focused unit and integration tests.

## Helpful developer scripts and files

- `backend/secret_gen.py` — generate application secrets
- `backend/run.py` — alternate script to run or bootstrap the app (see file)
- `docker-compose.yml` — multi-service configuration for local/dev

## Contract (tiny)

- Inputs: environment variables (DATABASE_URL, SECRET_KEY, other optional configuration), an operational database accessible by the app, and typical HTTP requests from the frontend.
- Outputs: an HTTPS/HTTP API (JSON) serving authentication, organizations, dashboards, and admin endpoints; a built frontend bundle when `npm run build` is invoked.
- Error modes: server returns HTTP error codes for invalid requests, DB connection failures if environment/DB not available, and migration mismatches if DB schema not in sync.

Success criteria: backend starts, Alembic migrations apply, frontend connects to backend, tests pass for touched areas.

## Likely edge cases to consider

- Missing environment variables or an unreachable DB
- Concurrent migrations (avoid by coordinating schema work)
- Large payloads from clients or slow endpoints (paginated responses recommended)
- Authentication/authorization mistakes — ensure role checks are exhaustive

## Troubleshooting

- If the backend fails to start: check `DATABASE_URL`, `SECRET_KEY`, and ensure postgres (or your DB) is reachable.
- Alembic errors: inspect migration files in `backend/alembic/versions/` and the DB. Rolling back may be necessary for partial upgrades.
- Frontend CORS / API URL: verify the frontend is pointing to the correct backend host/port. Adjust dev proxy or base URL if required.

## Contributing (by Permission Only)

1. Fork and create a feature branch.
2. Add tests for new behavior. Keep commits focused.
3. Update or create Alembic migration if models change.
4. Open a PR to `main` with a clear description and testing notes.

Coding style: follow existing project conventions. Use `ruff`, `black`, or other configured linters/formatters if available in the project.

## Quality gates (notes)

- Build: Not applicable for README-only changes. For code changes, verify package installs (`pip install -r backend/requirements.txt`) and backend starts.
- Lint/Typecheck: Run project linters if present (e.g., `ruff`, `black`) before merging code changes.
- Tests: Run `pytest` and ensure new tests cover added functionality. Aim to keep the test run fast and stable.

## License & contact

This project is proprietary software. See the `LICENSE` file in the repository root for the full copyright and license notice.

Summary: Copyright (c) 2026 merytpeters — All Rights Reserved. This repository is not open source and no rights to copy, modify, distribute, or use the software are granted except by a written license from the copyright holder.

For licensing enquiries or to request permission to use or commercialize the Software, please open an issue or contact the repository owner directly.

