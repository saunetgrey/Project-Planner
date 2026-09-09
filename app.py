"""Development and WSGI entry point for the planner."""

from planner.web import app


if __name__ == "__main__":
    app.run(debug=True)
