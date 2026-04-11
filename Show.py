import math

class Show:
    def __init__(self, name, number_of_episodes, episodes_per_day, minutes_per_episode):
        self.name = name
        self.number_of_episodes = number_of_episodes
        self.episodes_per_day = episodes_per_day
        self.minutes_per_episode = minutes_per_episode
        self.days_completed = 0
        self.last_completed_date = None
        self.completed = False

    @property
    def total_days(self):
        return math.ceil(self.number_of_episodes / self.episodes_per_day)

    @property
    def days_remaining(self):
        return max(0, self.total_days - self.days_completed)
