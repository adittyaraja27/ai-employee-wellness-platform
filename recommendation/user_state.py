def determine_user_state(trend_result):
    """
    Convert emotional trend analysis into a simplified
    current user state.
    """

    if trend_result["total_analyses"] == 0:
        return {
            "dominant_emotion": None,
            "trend": None,
            "average_intensity": 0.0,
            "state": "No data"
        }

    dominant_emotion = trend_result["dominant_emotion"]

    average_intensity = trend_result["average_intensity"].get(
        dominant_emotion,
        0.0
    )

    trend = trend_result["trend_direction"].get(
        dominant_emotion,
        "Insufficient data"
    )

    if average_intensity >= 0.75:
        intensity_level = "High"
    elif average_intensity >= 0.50:
        intensity_level = "Moderate"
    else:
        intensity_level = "Low"

    negative_emotions = {
        "sadness",
        "anger",
        "fear",
        "disgust"
    }

    positive_emotions = {
        "joy",
        "surprise"
    }

    if dominant_emotion in negative_emotions:
        emotional_pattern = "Negative"
    elif dominant_emotion in positive_emotions:
        emotional_pattern = "Positive"
    else:
        emotional_pattern = "Neutral"

    return {
        "dominant_emotion": dominant_emotion,
        "trend": trend,
        "average_intensity": round(average_intensity, 4),
        "intensity_level": intensity_level,
        "emotional_pattern": emotional_pattern,
        "state": f"{intensity_level} {emotional_pattern} State"
    }