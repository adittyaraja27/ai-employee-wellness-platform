from emotion.labels import EMOTION_LABELS


def calculate_intensity(emotion_scores):
    """
    Calculate the overall emotional intensity from emotion probabilities.

    Parameters:
        emotion_scores (dict):
            Dictionary containing emotion probabilities.

    Returns:
        dict containing:
            - dominant_emotion
            - intensity
            - severity
    """

    if not emotion_scores:
        raise ValueError("Emotion scores cannot be empty")

    # Find the emotion with the highest probability
    dominant_emotion = max(
        emotion_scores,
        key=emotion_scores.get
    )

    intensity = emotion_scores[dominant_emotion]

    # Convert intensity into a severity level
    if intensity >= 0.75:
        severity = "High"
    elif intensity >= 0.50:
        severity = "Moderate"
    else:
        severity = "Low"

    return {
        "dominant_emotion": dominant_emotion,
        "intensity": float(intensity),
        "severity": severity
    }