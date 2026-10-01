from collections import Counter

TREND_THRESHOLD = 0.05


def _average(values):
    if not values:
        return 0.0
    return sum(values) / len(values)


def _get_emotion_scores(record):
    """
    Get all emotion scores from a history record.

    Falls back to the dominant emotion/intensity for older
    or simplified history records.
    """
    emotion_data = record.get("emotions", {})
    scores = emotion_data.get("emotions", {})

    if scores:
        return scores

    dominant_emotion = record["emotional_state"]["dominant_emotion"]
    intensity = record["intensity"]["intensity"]

    return {
        dominant_emotion: intensity
    }


def _get_trend_direction(older_values, recent_values):
    """
    Compare older and recent average emotion scores.
    """
    if not older_values or not recent_values:
        return "Insufficient data"

    older_average = _average(older_values)
    recent_average = _average(recent_values)

    change = recent_average - older_average

    if change > TREND_THRESHOLD:
        return "Increasing"

    if change < -TREND_THRESHOLD:
        return "Decreasing"

    return "Stable"


def analyze_emotional_trends(history_records):

    if not history_records:
        return {
            "total_analyses": 0,
            "emotion_frequency": {},
            "average_intensity": {},
            "dominant_emotion": None,
            "trend_direction": {}
        }

    # History is normally chronological because UserHistory
    # appends new records. Keep that order.
    records = history_records

    # ---------------------------------------------------------
    # 1. Emotion frequency
    # ---------------------------------------------------------

    emotion_frequency = Counter()

    for record in records:
        dominant_emotion = record["emotional_state"]["dominant_emotion"]
        emotion_frequency[dominant_emotion] += 1

    # ---------------------------------------------------------
    # 2. Average intensity by dominant emotion
    # ---------------------------------------------------------

    intensity_values = {}

    for record in records:
        dominant_emotion = record["emotional_state"]["dominant_emotion"]
        intensity = record["intensity"]["intensity"]

        if dominant_emotion not in intensity_values:
            intensity_values[dominant_emotion] = []

        intensity_values[dominant_emotion].append(intensity)

    average_intensity = {}

    for emotion, values in intensity_values.items():
        average_intensity[emotion] = _average(values)

    # ---------------------------------------------------------
    # 3. Overall dominant emotion
    # ---------------------------------------------------------

    dominant_emotion = emotion_frequency.most_common(1)[0][0]

    # ---------------------------------------------------------
    # 4. Trend direction
    # ---------------------------------------------------------

    trend_direction = {}

    # Split history into older and recent sections.
    split_index = len(records) // 2

    if split_index == 0:
        trend_direction = {
            emotion: "Insufficient data"
            for emotion in emotion_frequency
        }
    else:
        older_records = records[:split_index]
        recent_records = records[split_index:]

        emotions = set()

        for record in records:
            scores = _get_emotion_scores(record)
            emotions.update(scores.keys())

        for emotion in emotions:

            older_values = []
            recent_values = []

            for record in older_records:
                scores = _get_emotion_scores(record)
                older_values.append(scores.get(emotion, 0.0))

            for record in recent_records:
                scores = _get_emotion_scores(record)
                recent_values.append(scores.get(emotion, 0.0))

            trend_direction[emotion] = _get_trend_direction(
                older_values,
                recent_values
            )

    return {
        "total_analyses": len(records),
        "emotion_frequency": dict(emotion_frequency),
        "average_intensity": average_intensity,
        "dominant_emotion": dominant_emotion,
        "trend_direction": trend_direction
    }