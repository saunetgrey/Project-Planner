import math

class Show:
    def __init__(self, name, number_of_episodes, episodes_per_day, minutes_per_episode):
        self.id = None
        self.name = name
        self.number_of_episodes = number_of_episodes
        self.episodes_per_day = episodes_per_day
        self.minutes_per_episode = minutes_per_episode
        self.remaining_episodes = number_of_episodes
        self.days_completed = 0
        self.last_completed_date = None
        self.is_favourite = False

    @property
    def completed(self):
        return self.remaining_episodes <= 0

    @property
    def total_days(self):
        return math.ceil(self.number_of_episodes / self.episodes_per_day)

    @property
    def days_remaining(self):
        return math.ceil(self.remaining_episodes / self.episodes_per_day)

    @property
    def total_time_spent(self):
        return self.minutes_per_episode * min(self.episodes_per_day, max(0, self.remaining_episodes))
