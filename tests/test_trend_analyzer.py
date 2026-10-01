from recommendation.trend_analyzer import analyze_emotional_trends


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


result = analyze_emotional_trends(history_records)


print("\nEmotional Trend Analysis\n")

print("Total analyses:", result["total_analyses"])

print("\nEmotion frequency:")
for emotion, count in result["emotion_frequency"].items():
    print(f"  {emotion}: {count}")

print("\nAverage intensity:")
for emotion, intensity in result["average_intensity"].items():
    print(f"  {emotion}: {intensity:.2f}")

print("\nDominant emotion:", result["dominant_emotion"])

print("\nTrend direction:")
for emotion, direction in result["trend_direction"].items():
    print(f"  {emotion}: {direction}")