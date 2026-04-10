import json
import os
from Show import Show
from datetime import date

class ShowApp:
    def __init__(self):
        self.shows = []
        self.load_shows()

    def add_show(self, name, episodes, minutes, hours):
        self.shows.append(Show(name, episodes, hours, minutes))
        self.save_shows()

    def complete_show(self, index):
        show = self.shows[index]
        today = date.today().isoformat()

        if show.last_completed_date != today:
            show.days_completed += 1
            show.last_completed_date = today

        if show.days_completed >= show.total_days:
            self.shows.pop(index)

        self.save_shows()

    def delete_show(self, index):
        self.shows.pop(index)
        self.save_shows()

    def save_shows(self):
        data = []
        for s in self.shows:
            data.append({
                "name": s.name,
                "number_of_episodes": s.number_of_episodes,
                "minutes_per_episode": s.minutes_per_episode,
                "hours_per_day": s.hours_per_day,
                "days_completed": s.days_completed,
                "last_completed_date": s.last_completed_date
            })

        with open("shows.json", "w") as f:
            json.dump(data, f, indent=4)

    def load_shows(self):
        if not os.path.exists("shows.json"):
            return

        with open("shows.json", "r") as f:
            data = json.load(f)

        for item in data:
            s = Show(
                item["name"],
                item["number_of_episodes"],
                item["hours_per_day"],
                item["minutes_per_episode"]
            )
            s.days_completed = item["days_completed"]
            s.last_completed_date = item.get("last_completed_date")
            self.shows.append(s)
