# Project Planner

A small Flask planner for estimating nutrition needs and keeping track of TV shows. Show data is stored in PostgreSQL in NEON, with a responsive web interface built using CSS and JavaScript. Nutrition calculations do not require a database connection and do not save measurements.

## Features

- Track calories on the home page (`/`) using weight, height, age, sex used for equations, activity level, waist, neck, and (for the female equation) hip measurements.
- Estimate body fat, fat and lean mass, maintenance calories, and daily/weekly protein, carbs, and fat.
- View current BMI and its screening category (adult categories for ages 20+).
- Optionally enter a desired weight to estimate daily protein at 1.6 g/kg of goal weight. This separate planning estimate does not change the current-weight calorie and macro tables.
- Compare 0.25 and 0.5 kg/week fat-loss scenarios, with screening for overly restrictive plans.
- Add, edit, and delete shows.
- Set episodes remaining, minutes per episode, and episodes to watch each day.
- Mark a day's viewing complete once per day; finished shows are removed automatically.
- Sort by episodes, episode length, daily pace, or days remaining.
- See the planned watch time remaining for today.

The repository also includes a JSON-backed task planner model, service, and template. These are retained for future development and are **not currently connected to web routes**.

## Getting started

Use Python 3.11 and pip. The show planner also requires access to the existing PostgreSQL database with SSL enabled and the `shows` table already created.

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

This step is needed only for the show planner.

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

Open **http://127.0.0.1:5000/** for Track calories, or **http://127.0.0.1:5000/shows** for the show planner. The app connects to the database only when a show operation needs it.

The local command enables Flask's development debugger. On a Unix host, the existing WSGI entry point can be served with:

```sh
gunicorn app:app
```

## Project structure

```text
.
├── app.py                  # Development / WSGI entry point
├── planner/
│   ├── web.py              # Flask application, nutrition and show routes
│   ├── db.py               # PostgreSQL connection helper
│   ├── models/             # Show and task data models
│   ├── services/           # Nutrition calculations, persistence and progress
│   ├── static/             # Shared styles, nutrition styles and JavaScript
│   └── templates/          # Jinja page templates
├── .env.example            # Configuration reference
├── .python-version         # Python version for development
└── requirements.txt        # Pinned Python dependencies
```

## Development notes

- Run commands from the repository root.
- The task service reads and writes `tasks.json` in the working directory; this local data is ignored by Git.
- Check nutrition calculations at `/`. With a configured database, check adding, editing, sorting, completing, and deleting shows at `/shows`.
- Nutrition estimates use Mifflin–St Jeor and historical Navy circumference equations. The page documents the activity factors, macro choices, limits, and source links. The fixed energy-deficit calculation is a rough scenario, not a dynamic weight-loss prediction or a guarantee of fat loss.
- The app currently has no authentication and uses one shared show list. Keep that in mind when choosing where to host it.
