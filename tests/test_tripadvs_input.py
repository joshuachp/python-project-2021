from pathlib import Path
from src.sentiment_analysis.tripadvs_input import TripAdvisorFile


def test_read_csv_file():
    trip_advisor = TripAdvisorFile(Path('assets/trip_advisor_reviews.csv'))
    assert len(trip_advisor.data[0]) == 4
