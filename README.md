# Project Planner

A small Flask planner for keeping track of TV shows and a daily viewing schedule. Show data is stored in PostgreSQL in NEON, with a responsive web interface built using CSS, and JavaScript.

## Features

- Add, edit, and delete shows.
- Set episodes remaining, minutes per episode, and episodes to watch each day.
- Mark a day's viewing complete once per day; finished shows are removed automatically.
- Sort by episodes, episode length, daily pace, or days remaining.
- See the planned watch time remaining for today.

The repository also includes a JSON-backed task planner model, service, and template. These are retained for future development and are **not currently connected to web routes**.

## Getting started

Use Python 3.11, pip, and access to the existing PostgreSQL database with SSL enabled and the `shows` table already created.

### 1. Install dependencies

From the repository root:

```sh
python -m venv .venv
```

Activate the virtual environment:

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

```sh
# macOS / Linux
source .venv/bin/activate
```

Then install the pinned dependencies:

```sh
python -m pip install -r requirements.txt
```

### 2. Configure the database

Set the connection URL for your existing database in the same terminal you will use to run the app:

```powershell
# Windows PowerShell
$env:DATABASE_URL = "postgresql://username:password@hostname:5432/planner"
```

```sh
# macOS / Linux
export DATABASE_URL="postgresql://username:password@hostname:5432/planner"
```

`.env.example` documents the required configuration. The app does not load `.env` files automatically. Database connections use `sslmode=require`, so the server must support SSL. The app uses the existing `shows` table; it does not create the database or tables.

### 3. Run locally

```sh
python app.py
```

Open **http://127.0.0.1:5000/shows**. The root URL (`/`) has no route. The database must be available before startup because the app loads shows during initialization.

The local command enables Flask's development debugger. On a Unix host, the existing WSGI entry point can be served with:

```sh
gunicorn app:app
```

## Project structure

```text
.
├── app.py                  # Development / WSGI entry point
├── planner/
│   ├── web.py              # Flask application and show routes
│   ├── db.py               # PostgreSQL connection helper
│   ├── models/             # Show and task data models
│   ├── services/           # Persistence and progress tracking
│   ├── static/style.css    # Web styles
│   └── templates/          # Jinja page templates
├── .env.example            # Configuration reference
├── .python-version         # Python version for development
└── requirements.txt        # Pinned Python dependencies
```

## Development notes

- Run commands from the repository root.
- The task service reads and writes `tasks.json` in the working directory; this local data is ignored by Git.
- There is currently no automated test suite. With a configured database, smoke-test adding, editing, sorting, completing, and deleting a show at `/shows`.
- The app currently has no authentication and uses one shared show list. Keep that in mind when choosing where to host it.
