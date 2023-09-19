# generate_matches.py

from datetime import datetime, timedelta
from website import db
from website.models import Match
from website import create_app

app = create_app()

def add_matches_for_pitch(pitch_id):
    start_time = datetime.strptime("11:00", "%H:%M").time()
    end_time = datetime.strptime("23:00", "%H:%M").time()
    matches_per_day = 12
    days_in_year = 365

    for day in range(days_in_year):
        current_date = datetime.now() + timedelta(days=day)
        for _ in range(matches_per_day):
            for hour in range(start_time.hour, end_time.hour + 1):
                match_time = datetime(current_date.year, current_date.month, current_date.day, hour)
                new_match = Match(pitch_id=pitch_id, date=match_time.date(), time=match_time.time(), max_players=12)
                db.session.add(new_match)
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        add_matches_for_pitch(pitch_id=1)  # Replace 1 with the actual pitch ID
