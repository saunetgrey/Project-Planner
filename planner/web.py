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


def render_show_page(edit_show=None):
    sort_by, order = show_sort_options()
    service_filter = request.args.get(
        "service", request.cookies.get("shows_service", "")
    )
    service_options = {}
    for show in show_app.shows:
        label = (show.streaming_service or "").strip()
        key = "service:" + label.casefold() if label else "unspecified"
        service_options.setdefault(key, label or "Not specified")
    # Keep a selected service available even after its last show is removed.
    if service_filter and service_filter not in service_options:
        if service_filter.startswith("service:"):
            service_options[service_filter] = service_filter[len("service:"):]
        elif service_filter == "unspecified":
            service_options[service_filter] = "Not specified"
        else:
            service_filter = ""

    today = date.today()
    visible_shows = []
    for show in show_app.shows:
        service = (show.streaming_service or "").strip()
        key = "service:" + service.casefold() if service else "unspecified"
        if not service_filter or key == service_filter:
            visible_shows.append(show)
    visible_shows.sort(key=SORT_KEYS[sort_by], reverse=order == "desc")
    total_minutes = sum(show.total_time_spent for show in visible_shows
                        if show.last_completed_date != today)
    favourite_shows = [show for show in visible_shows if show.is_favourite]
    favourite_minutes = sum(show.total_time_spent for show in favourite_shows
                            if show.last_completed_date != today)
    response = make_response(render_template(
        "shows.html",
        shows=visible_shows,
        edit_show=edit_show,
        today=today,
        sort_by=sort_by,
        order=order,
        service_filter=service_filter,
        service_options=sorted(service_options.items(), key=lambda item: item[1].casefold()),
        total_hours=total_minutes // 60,
        remaining_minutes=total_minutes % 60,
        total_rows=len(visible_shows),
        favourite_rows=len(favourite_shows),
        favourite_hours=favourite_minutes // 60,
        favourite_minutes=favourite_minutes % 60,
    ))
    if "sort_by" in request.args or "order" in request.args:
        response.set_cookie("shows_sort_by", sort_by, max_age=31536000, samesite="Lax")
        response.set_cookie("shows_order", order, max_age=31536000, samesite="Lax")
    if "service" in request.args:
        response.set_cookie("shows_service", service_filter, max_age=31536000, samesite="Lax")
    return response


@app.route("/shows")
def shows():
    show_app.load_shows()
    return render_show_page()


@app.route("/add_show", methods=["POST"])
def add_show():
    name = request.form["name"]
    streaming_service = request.form.get("streaming_service", "").strip() or None
    episodes = int(request.form["episodes"])
    minutes = int(request.form["minutes"])
    episodes_per_day = int(request.form["episodes_per_day"])

    edit_id = request.form.get("edit_id")

    if edit_id:
        show_app.update_show(edit_id, name, episodes, minutes, episodes_per_day, streaming_service)
    else:
        show_app.add_show(name, episodes, minutes, episodes_per_day, streaming_service)

    return redirect(url_for("shows"))


@app.route('/complete_show/<int:show_id>')
def complete_show(show_id):
    show_app.complete_show(show_id)
    return redirect(url_for("shows"))


@app.route("/delete_show/<int:show_id>")
def delete_show(show_id):
    show_app.delete_show(show_id)
    return redirect(url_for("shows"))


@app.route("/favourite_show/<int:show_id>", methods=["POST"])
def favourite_show(show_id):
    show_app.toggle_favourite(show_id)
    return redirect(url_for("shows", sort_by=request.form.get("sort_by"),
                            order=request.form.get("order", "desc")))


@app.route("/edit_show/<int:show_id>")
def edit_show(show_id):
    show_app.load_shows()

    show = next((s for s in show_app.shows if s.id == show_id), None)
    if show is None:
        return redirect(url_for("shows"))
    return render_show_page(edit_show=show)
