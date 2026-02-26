# AI Reflection Assistant

A personal growth tool for tracking daily reflections against your big-picture goals. Every Sunday, it generates a weekly AI summary and emails it to you — covering what you accomplished, goals you made progress on, and next steps for the week ahead.

## Problem Statement

It's easy to go through a busy week without pausing to reflect on what you accomplished or how you moved toward your goals. This tool creates a lightweight habit of daily reflection and closes the loop every Sunday with an AI-generated summary.

## Requirements

- Python 3.11+
- Node.js 20+
- [Anthropic API key](https://console.anthropic.com/)
- [Resend account + API key](https://resend.com/) with a verified domain

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/your-username/ai-reflection-assistant.git
cd ai-reflection-assistant
```

### 2. Configure environment variables

Create `backend/.env` with the following:

```
ANTHROPIC_API_KEY=your_anthropic_api_key
RESEND_API_KEY=your_resend_api_key
EMAIL=you@yourdomain.com
```

### 3. Run with Docker

```bash
docker compose up --build
```

- Frontend: http://localhost:5173
- Backend: http://localhost:8000

### 4. Run locally (alternative)

**Backend:**
```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install && npm run dev
```

## Scheduling the Weekly Summary

Add a cron job to run the summary every Sunday at 8pm:

```bash
chmod +x backend/run_summarize.sh
printf '0 20 * * 0 /absolute/path/to/backend/run_summarize.sh\n' | crontab -
```

Logs are written to `/tmp/reflections.log` and `/tmp/reflections-error.log`.
