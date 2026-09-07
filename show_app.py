from Show import Show
from datetime import date
from db import get_connection


class ShowApp:
    def __init__(self):
        self.shows = []
        self.load_shows()

    def load_shows(self):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM shows")
        rows = cur.fetchall()

        self.shows = []

        for row in rows:
            s = Show(
                row[1],
                row[2],
                row[4],
                row[3]
            )
            s.id = row[0]
            s.days_completed = row[5]
            s.last_completed_date = row[6]
            self.shows.append(s)

        cur.close()
        conn.close()

    def add_show(self, name, episodes, minutes, episodes_per_day):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO shows (name, remaining_episodes, minutes_per_episode, episodes_per_day)
            VALUES (%s, %s, %s, %s)
        """, (name, episodes, minutes, episodes_per_day))

        conn.commit()
        cur.close()
        conn.close()

    def update_show(self, show_id, name, episodes, minutes, episodes_per_day):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE shows
            SET name=%s,
                remaining_episodes=%s,
                minutes_per_episode=%s,
                episodes_per_day=%s
            WHERE id=%s
        """, (name, episodes, minutes, episodes_per_day, show_id))

        conn.commit()
        cur.close()
        conn.close()

    def delete_show(self, show_id):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("DELETE FROM shows WHERE id=%s", (show_id,))

        conn.commit()
        cur.close()
        conn.close()

    def complete_show(self, show_id):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM shows WHERE id=%s", (show_id,))
        row = cur.fetchone()

        if not row:
            return

        remaining_episodes = row[2]
        episodes_per_day = row[4]
        days_completed = row[5]
        last_completed_date = row[6]

        today = date.today()

        if last_completed_date != today:
            days_completed += 1
            last_completed_date = today
            remaining_episodes -= episodes_per_day

            if remaining_episodes < 0:
                remaining_episodes = 0

        cur.execute("""
            UPDATE shows
            SET remaining_episodes=%s,
                days_completed=%s,
                last_completed_date=%s
            WHERE id=%s
        """, (remaining_episodes, days_completed, last_completed_date, show_id))

        if remaining_episodes == 0:
            cur.execute("DELETE FROM shows WHERE id=%s", (show_id,))

        conn.commit()
        cur.close()
        conn.close()
