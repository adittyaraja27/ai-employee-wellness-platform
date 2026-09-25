from emotion.labels import EMOTION_LABELS


def analyze_emotional_state(emotion_scores, intensity_result):
    """
    Analyze the user's overall emotional state.

    Parameters:
        emotion_scores (dict):
            Emotion probabilities from the transformer model.

        intensity_result (dict):
            Result from calculate_intensity().

    Returns:
        dict containing dominant emotion, secondary emotions,
        mixed state, polarity, intensity and severity.
    """

    if not emotion_scores:
        raise ValueError("Emotion scores cannot be empty")

    dominant_emotion = intensity_result["dominant_emotion"]
    intensity = intensity_result["intensity"]
    severity = intensity_result["severity"]

    # Emotions that are strong enough to be considered present
    detected_emotions = {
        emotion: score
        for emotion, score in emotion_scores.items()
        if score >= 0.50
    }

    # Remove dominant emotion to identify secondary emotions
    secondary_emotions = {
        emotion: score
        for emotion, score in detected_emotions.items()
        if emotion != dominant_emotion
    }

    # Positive and negative emotion groups
    positive_emotions = {"joy", "surprise"}
    negative_emotions = {"sadness", "anger", "fear", "disgust"}

    positive_score = max(
        [emotion_scores[e] for e in positive_emotions],
        default=0
    )

    negative_score = max(
        [emotion_scores[e] for e in negative_emotions],
        default=0
    )

    # Determine emotional polarity
    if positive_score >= 0.50 and negative_score >= 0.50:
        polarity = "Mixed"
    elif positive_score >= 0.50:
        polarity = "Positive"
    elif negative_score >= 0.50:
        polarity = "Negative"
    else:
        polarity = "Neutral"

    # Mixed emotional state means multiple strong emotions
    is_mixed = len(detected_emotions) > 1

    if is_mixed:
        emotional_state = "Mixed emotional state"
    elif polarity == "Positive":
        emotional_state = "Positive emotional state"
    elif polarity == "Negative":
        emotional_state = "Negative emotional state"
    else:
        emotional_state = "Neutral emotional state"

    return {
        "dominant_emotion": dominant_emotion,
        "secondary_emotions": secondary_emotions,
        "is_mixed": is_mixed,
        "polarity": polarity,
        "emotional_state": emotional_state,
        "intensity": intensity,
        "severity": severity
    }