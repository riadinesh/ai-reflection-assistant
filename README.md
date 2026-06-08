# AI Reflection Assistant

A personal growth tool for tracking daily reflections against your big-picture goals. Every Sunday, it generates a weekly AI summary and emails it to you — covering what you accomplished, goals you made progress on, and next steps for the week ahead.

> 🔗 **Live site:** https://my-reflection-app.com/  <!-- replace with your real Vercel/custom domain -->

<img width="1631" height="882" alt="Screenshot 2026-06-05 at 4 30 15 PM" src="https://github.com/user-attachments/assets/f4841d55-ad97-40ff-9351-bf9be5d66604" />

## Problem Statement

It's easy to go through a busy week without pausing to reflect on what you accomplished or how you moved toward your goals. This tool creates a lightweight habit of daily reflection and closes the loop every Sunday with an AI-generated summary.

## Features

- Set big-picture goals and write short daily reflections each week
- Navigate between weeks to review or backfill reflections
- Generate an AI weekly summary (narrative recap, goals worked on, suggested next steps)
- Automatically sends the weekly summary by email every Sunday
- Account auth (signup/login) with per-user data isolation

## Tech Stack & Architecture

| Layer | Tech | Hosting |
|-------|------|---------|
| Frontend | React + TypeScript + Vite | Vercel |
| Backend | FastAPI (Python) | Render |
| Database | PostgreSQL | Neon |
| AI | Anthropic Claude | — |
| Email | Resend (custom verified domain) | — |

The Vite frontend (Vercel) calls the FastAPI API (Render), which persists data in Neon Postgres, generates summaries with Claude, and delivers weekly emails through Resend.

## Run Locally

### Requirements

- Python 3.11+
- Node.js 20+
- A PostgreSQL database (a free [Neon] project works great)
- [Anthropic API key]
- [Resend]

### 1. Clone the repo

```bash
git clone https://github.com/your-username/ai-reflection-assistant.git
cd ai-reflection-assistant
```

### 2. Configure the backend

Create `backend/.env`:

```
DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require
SECRET_KEY=your_long_random_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ANTHROPIC_API_KEY=your_anthropic_api_key
RESEND_API_KEY=your_resend_api_key
RESEND_FROM=Reflections <you@yourdomain.com>
FRONTEND_URL=http://localhost:5173
```

Then run it:

```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend runs at http://localhost:8000 (interactive API docs at `/docs`).

### 3. Configure the frontend

Create `frontend/.env`:

```
VITE_API_URL=http://localhost:8000
```

Then run it:

```bash
cd frontend
npm install && npm run dev
```

Frontend runs at http://localhost:5173.

## Deployment

The app is split across managed platforms:

- **Frontend → Vercel** — Root Directory `frontend`; set `VITE_API_URL` to your deployed backend URL.
- **Backend → Render** — Root Directory `backend`; Start Command `uvicorn app.main:app --host 0.0.0.0 --port $PORT`; set all `backend/.env` variables, plus `FRONTEND_URL` = your Vercel domain (for CORS).
- **Database → Neon** — use the pooled connection string as `DATABASE_URL`.
- **Email → Resend** — verify your domain and set `RESEND_FROM` to an address on it.

## Scheduling the Weekly Summary

Add a cron job to run the summary every Sunday at 8pm:

```bash
chmod +x backend/run_summarize.sh
printf '0 20 * * 0 /absolute/path/to/backend/run_summarize.sh\n' | crontab -
```

Logs are written to `/tmp/reflections.log` and `/tmp/reflections-error.log`.
