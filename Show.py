import math

class Show:
    def __init__(self, name, number_of_episodes, hours_per_day, minutes_per_episode):
        self.name = name
        self.number_of_episodes = number_of_episodes
        self.hours_per_day = hours_per_day
        self.minutes_per_episode = minutes_per_episode
        self.days_completed = 0
        self.last_completed_date = None
        self.completed = False

    @property
    def total_days(self):
        total_minutes = self.number_of_episodes * self.minutes_per_episode
        total_hours = total_minutes / 60
        return math.ceil(total_hours / self.hours_per_day)

    @property
    def days_remaining(self):
        return max(0, self.total_days - self.days_completed)
