from planner.models.show import Show
from datetime import date
from planner.db import get_connection


class ShowApp:
    def __init__(self):
        self.shows = []

    def load_shows(self):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, name, remaining_episodes, minutes_per_episode,
                   episodes_per_day, days_completed, last_completed_date,
                   streaming_service, is_favourite
            FROM shows
        """)
        rows = cur.fetchall()

        self.shows = []

        for row in rows:
            s = Show(
                row[1],
                row[2],
                row[4],
                row[3],
                row[7]
            )
            s.id = row[0]
            s.days_completed = row[5]
            s.last_completed_date = row[6]
            s.is_favourite = row[8]
            self.shows.append(s)

        cur.close()
        conn.close()

    def toggle_favourite(self, show_id):
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE shows SET is_favourite = NOT is_favourite WHERE id=%s",
                    (show_id,),
                )
            conn.commit()
        finally:
            conn.close()

    def add_show(self, name, episodes, minutes, episodes_per_day, streaming_service=None):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO shows (name, remaining_episodes, minutes_per_episode, episodes_per_day, streaming_service)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, episodes, minutes, episodes_per_day, streaming_service))

        conn.commit()
        cur.close()
        conn.close()

    def update_show(self, show_id, name, episodes, minutes, episodes_per_day, streaming_service=None):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE shows
            SET name=%s,
                remaining_episodes=%s,
                minutes_per_episode=%s,
                episodes_per_day=%s,
                streaming_service=%s
            WHERE id=%s
        """, (name, episodes, minutes, episodes_per_day, streaming_service, show_id))

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
            cur.close()
            conn.close()
            return

        remaining_episodes = row[2]
        episodes_per_day = row[4]
        days_completed = row[5]
        last_completed_date = row[6]

        today = date.today()

        if remaining_episodes > 0 and last_completed_date != today:
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

        conn.commit()
        cur.close()
        conn.close()
