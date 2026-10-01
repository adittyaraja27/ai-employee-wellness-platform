from recommendation.trend_analyzer import analyze_emotional_trends
from recommendation.user_state import determine_user_state


history_records = [
    {
        "timestamp": "2026-09-20T10:00:00",
        "emotions": {
            "emotions": {
                "fear": 0.40,
                "joy": 0.60,
                "anger": 0.20
            }
        },
        "intensity": {
            "intensity": 0.40
        },
        "emotional_state": {
            "dominant_emotion": "joy"
        }
    },
    {
        "timestamp": "2026-09-21T10:00:00",
        "emotions": {
            "emotions": {
                "fear": 0.45,
                "joy": 0.55,
                "anger": 0.25
            }
        },
        "intensity": {
            "intensity": 0.45
        },
        "emotional_state": {
            "dominant_emotion": "fear"
        }
    },
    {
        "timestamp": "2026-09-22T10:00:00",
        "emotions": {
            "emotions": {
                "fear": 0.60,
                "joy": 0.50,
                "anger": 0.30
            }
        },
        "intensity": {
            "intensity": 0.60
        },
        "emotional_state": {
            "dominant_emotion": "fear"
        }
    },
    {
        "timestamp": "2026-09-23T10:00:00",
        "emotions": {
            "emotions": {
                "fear": 0.70,
                "joy": 0.45,
                "anger": 0.30
            }
        },
        "intensity": {
            "intensity": 0.70
        },
        "emotional_state": {
            "dominant_emotion": "fear"
        }
    },
    {
        "timestamp": "2026-09-24T10:00:00",
        "emotions": {
            "emotions": {
                "fear": 0.80,
                "joy": 0.40,
                "anger": 0.30
            }
        },
        "intensity": {
            "intensity": 0.80
        },
        "emotional_state": {
            "dominant_emotion": "fear"
        }
    }
]


trend_result = analyze_emotional_trends(history_records)

user_state = determine_user_state(trend_result)


print("\nUser State Tracking\n")

print("Dominant emotion:", user_state["dominant_emotion"])
print("Trend:", user_state["trend"])
print("Average intensity:", user_state["average_intensity"])
print("Intensity level:", user_state["intensity_level"])
print("Emotional pattern:", user_state["emotional_pattern"])
print("Overall state:", user_state["state"])