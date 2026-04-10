from flask import Flask, render_template, request, redirect, url_for
from task_app import TaskApp
from show_app import ShowApp

app = Flask(__name__)

task_app = TaskApp()
show_app = ShowApp()


# ================= TASK ROUTES =================
@app.route("/")
@app.route("/tasks")
def tasks():
    return render_template("tasks.html", tasks=task_app.tasks)


@app.route("/add_task", methods=["POST"])
def add_task():
    name = request.form["name"]
    hours = int(request.form["hours"])
    days = int(request.form["days"])

    task_app.add_task(name, hours, days)
    return redirect(url_for("tasks"))


@app.route("/complete_task/<int:index>")
def complete_task(index):
    task_app.complete_task(index)
    return redirect(url_for("tasks"))


@app.route("/delete_task/<int:index>")
def delete_task(index):
    task_app.delete_task(index)
    return redirect(url_for("tasks"))


# ================= SHOW ROUTES =================
@app.route("/shows")
def shows():
    sort_by = request.args.get("sort_by")
    order = request.args.get("order", "desc")

    shows = show_app.shows.copy()

    if sort_by:
        reverse = True if order == "desc" else False

        if sort_by == "episodes":
            shows.sort(key=lambda x: x.number_of_episodes, reverse=reverse)

        elif sort_by == "minutes":
            shows.sort(key=lambda x: x.minutes_per_episode, reverse=reverse)

        elif sort_by == "hours":
            shows.sort(key=lambda x: x.hours_per_day, reverse=reverse)

        elif sort_by == "days":
            shows.sort(key=lambda x: x.days_remaining, reverse=reverse)

    return render_template("shows.html", shows=shows)


@app.route("/add_show", methods=["POST"])
def add_show():
    name = request.form["name"]
    episodes = int(request.form["episodes"])
    minutes = int(request.form["minutes"])
    hours = int(request.form["hours"])

    edit_index = request.form.get("edit_index")

    if edit_index is not None and edit_index != "":
        show = show_app.shows[int(edit_index)]
        show.name = name
        show.number_of_episodes = episodes
        show.minutes_per_episode = minutes
        show.hours_per_day = hours
        show_app.save_shows()
    else:
        show_app.add_show(name, episodes, minutes, hours)

    return redirect(url_for("shows"))


@app.route('/complete_show/<int:index>')
def complete_show(index):
    show_app.complete_show(index)
    return redirect(url_for("shows"))


@app.route("/delete_show/<int:index>")
def delete_show(index):
    show_app.delete_show(index)
    return redirect(url_for("shows"))

@app.route("/edit_show/<int:index>")
def edit_show(index):
    show = show_app.shows[index]
    return render_template("shows.html", shows=show_app.shows, edit_index=index, edit_show=show)

if __name__ == "__main__":
    app.run(debug=True)
