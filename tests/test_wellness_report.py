from reports.wellness_report import (
    generate_wellness_report,
    generate_recommendation_csv
)


emotional_history = [
    {
        "timestamp": "2026-10-04T10:00:00",
        "emotions": {
            "emotions": {
                "sadness": 0.82,
                "fear": 0.61,
                "joy": 0.10
            }
        },
        "intensity": {
            "intensity": 0.82,
            "severity": "High"
        },
        "emotional_state": {
            "state": "Negative",
            "dominant_emotion": "sadness"
        }
    },
    {
        "timestamp": "2026-10-04T12:00:00",
        "emotions": {
            "emotions": {
                "joy": 0.78,
                "sadness": 0.12,
                "fear": 0.08
            }
        },
        "intensity": {
            "intensity": 0.78,
            "severity": "High"
        },
        "emotional_state": {
            "state": "Positive",
            "dominant_emotion": "joy"
        }
    }
]


recommendation_history = [
    {
        "timestamp": "2026-10-04T10:05:00",
        "recommendation_id": "breathing_01",
        "viewed": True,
        "accepted": True,
        "rejected": False,
        "rating": 5
    },
    {
        "timestamp": "2026-10-04T12:05:00",
        "recommendation_id": "gratitude_01",
        "viewed": True,
        "accepted": False,
        "rejected": True,
        "rating": 2
    }
]


trend_data = {
    "total_analyses": 2,
    "emotion_frequency": {
        "sadness": 1,
        "joy": 1
    },
    "average_intensity": {
        "sadness": 0.82,
        "joy": 0.78
    },
    "dominant_emotion": "sadness",
    "trend_direction": {
        "sadness": "Decreasing",
        "joy": "Increasing"
    }
}


def test_generate_wellness_report():
    report = generate_wellness_report(
        emotional_history,
        recommendation_history,
        trend_data
    )

    assert "Mood Mentor Wellness Report" in report
    assert "Total analyses: 2" in report
    assert "Dominant emotion: Sadness" in report
    assert "Helpful feedback: 1" in report
    assert "Not helpful feedback: 1" in report
    assert "Average rating: 3.50/5" in report
    assert "breathing_01" in report
    assert "gratitude_01" in report
    assert "Original user-entered mood text is not included." in report


def test_generate_recommendation_csv():
    csv_data = generate_recommendation_csv(
        recommendation_history
    )

    assert "recommendation_id" in csv_data
    assert "breathing_01" in csv_data
    assert "gratitude_01" in csv_data
