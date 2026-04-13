from datetime import date
from flask import Flask, render_template, request, redirect, url_for
from show_app import ShowApp

app = Flask(__name__)

show_app = ShowApp()


@app.route("/shows")
def shows():
    show_app.load_shows()  # 🔥 IMPORTANT

    sort_by = request.args.get("sort_by")
    order = request.args.get("order", "desc")

    shows = show_app.shows

    if sort_by:
        reverse = True if order == "desc" else False

        if sort_by == "episodes":
            shows.sort(key=lambda x: x.number_of_episodes, reverse=reverse)

        elif sort_by == "minutes":
            shows.sort(key=lambda x: x.minutes_per_episode, reverse=reverse)

        elif sort_by == "ep/day":
            shows.sort(key=lambda x: x.episodes_per_day, reverse=reverse)

        elif sort_by == "days":
            shows.sort(key=lambda x: x.days_remaining, reverse=reverse)

    return render_template(
        "shows.html",
        shows=shows,
        today=date.today(),
        sort_by=sort_by,
        order=order
    )


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

    show = next((s for s in show_app.shows if s.id == show_id), None)

    return render_template(
        "shows.html",
        shows=show_app.shows,
        edit_show=show
    )


if __name__ == "__main__":
    app.run(debug=True)