class Task:
    def __init__(self, name, total_hours, total_days):
        self.name = name
        self.total_hours = total_hours
        self.total_days = total_days
        self.days_completed = 0
        self.last_completed_date = None

    @property
    def days_remaining(self):
        return self.total_days - self.days_completed

    @property
    def hours_per_day(self):
        return self.total_hours / self.total_days if self.total_days else 0
