import json
import os
from datetime import date
from Task import Task

class TaskApp:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def add_task(self, name, hours, days):
        task = Task(name, hours, days)
        self.tasks.append(task)
        self.save_tasks()

    def complete_task(self, index):
        task = self.tasks[index]
        today = date.today().isoformat()

        if task.last_completed_date != today:
            task.days_completed += 1
            task.last_completed_date = today

        if task.days_completed >= task.total_days:
            self.tasks.pop(index)

        self.save_tasks()

    def delete_task(self, index):
        self.tasks.pop(index)
        self.save_tasks()

    def save_tasks(self):
        data = []
        for t in self.tasks:
            data.append({
                "name": t.name,
                "total_hours": t.total_hours,
                "total_days": t.total_days,
                "days_completed": t.days_completed,
                "last_completed_date": t.last_completed_date
            })

        with open("tasks.json", "w") as f:
            json.dump(data, f, indent=4)

    def load_tasks(self):
        if not os.path.exists("tasks.json"):
            return

        with open("tasks.json", "r") as f:
            data = json.load(f)

        for item in data:
            t = Task(item["name"], item["total_hours"], item["total_days"])
            t.days_completed = item["days_completed"]
            t.last_completed_date = item.get("last_completed_date")
            self.tasks.append(t)