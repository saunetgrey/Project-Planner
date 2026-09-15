from datetime import date
from flask import Flask, make_response, render_template, request, redirect, url_for
from planner.services.shows import ShowApp
from planner.services.nutrition import calculate_plan, ACTIVITIES

app = Flask(__name__)

show_app = ShowApp()

SORT_KEYS = {
    "episodes": lambda show: show.number_of_episodes,
    "minutes": lambda show: show.minutes_per_episode,
    "ep/day": lambda show: show.episodes_per_day,
    "days": lambda show: show.days_remaining,
}


def show_sort_options():
    sort_by = request.args.get("sort_by", request.cookies.get("shows_sort_by", "episodes"))
    order = request.args.get("order", request.cookies.get("shows_order", "desc"))
    if sort_by not in SORT_KEYS:
        sort_by = "episodes"
    if order not in ("asc", "desc"):
        order = "desc"
    return sort_by, order


@app.route("/", methods=["GET", "POST"])
def calories():
    result = None
    error = None
    if request.method == "POST":
        try:
            result = calculate_plan(request.form)
        except ValueError as exc:
            error = str(exc)
    return render_template(
        "calories.html", result=result, error=error,
        values=request.form, activities=ACTIVITIES,
    ), 400 if error else 200


@app.route("/shows")
def shows():
    show_app.load_shows()

    sort_by, order = show_sort_options()

    shows = show_app.shows
    shows.sort(key=SORT_KEYS[sort_by], reverse=order == "desc")

    today = date.today()

    total_minutes = sum(
        show.total_time_spent
        for show in shows
        if show.last_completed_date != today
    )
    total_hours = total_minutes // 60
    remaining_minutes = total_minutes % 60
    total_rows = len(show_app.shows)

    response = make_response(render_template(
        "shows.html",
        shows=shows,
        today=date.today(),
        sort_by=sort_by,
        order=order,
        total_hours=total_hours,
        total_rows=total_rows,
        remaining_minutes=remaining_minutes
    ))
    if "sort_by" in request.args or "order" in request.args:
        response.set_cookie("shows_sort_by", sort_by, max_age=31536000, samesite="Lax")
        response.set_cookie("shows_order", order, max_age=31536000, samesite="Lax")
    return response


@app.route("/add_show", methods=["POST"])
def add_show():
    name = request.form["name"]
    episodes = int(request.form["episodes"])
    minutes = int(request.form["minutes"])
    episodes_per_day = int(request.form["episodes_per_day"])

    edit_id = request.form.get("edit_id")

    if edit_id:
        show_app.update_show(edit_id, name, episodes, minutes, episodes_per_day)
    else:
        show_app.add_show(name, episodes, minutes, episodes_per_day)

    return redirect(url_for("shows"))


@app.route('/complete_show/<int:show_id>')
def complete_show(show_id):
    show_app.complete_show(show_id)
    return redirect(url_for("shows"))


@app.route("/delete_show/<int:show_id>")
def delete_show(show_id):
    show_app.delete_show(show_id)
    return redirect(url_for("shows"))


@app.route("/edit_show/<int:show_id>")
def edit_show(show_id):
    show_app.load_shows()

    sort_by, order = show_sort_options()
    show_app.shows.sort(key=SORT_KEYS[sort_by], reverse=order == "desc")

    show = next((s for s in show_app.shows if s.id == show_id), None)
    if show is None:
        return redirect(url_for("shows"))

    today = date.today()

    total_minutes = sum(
        show.total_time_spent
        for show in show_app.shows
        if show.last_completed_date != today
    )

    total_hours = total_minutes // 60
    remaining_minutes = total_minutes % 60
    total_rows = len(show_app.shows)

    return render_template(
        "shows.html",
        shows=show_app.shows,
        edit_show=show,
        sort_by=sort_by,
        order=order,
        total_hours=total_hours,
        total_rows=total_rows,
        remaining_minutes=remaining_minutes,
        today=today
    )


