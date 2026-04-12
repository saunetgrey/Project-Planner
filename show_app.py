import json
import os
from Show import Show
from datetime import date

class ShowApp:
    def __init__(self):
        self.shows = []
        self.load_shows()

    def add_show(self, name, episodes, minutes, episodes_per_day):
        self.shows.append(Show(name, episodes, episodes_per_day, minutes))
        self.save_shows()

    def complete_show(self, index):
        show = self.shows[index]
        today = date.today().isoformat()

        if show.last_completed_date != today:
            show.days_completed += 1
            show.last_completed_date = today

            show.remaining_episodes -= show.episodes_per_day
            if show.remaining_episodes < 0:
                show.remaining_episodes = 0

        if show.remaining_episodes == 0:
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
                "remaining_episodes": s.remaining_episodes,
                "minutes_per_episode": s.minutes_per_episode,
                "episodes_per_day": s.episodes_per_day,
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
                item["remaining_episodes"],
                item["episodes_per_day"],
                item["minutes_per_episode"]
            )
            s.days_completed = item["days_completed"]
            s.last_completed_date = item.get("last_completed_date")
            self.shows.append(s)
