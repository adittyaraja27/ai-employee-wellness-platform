from emotion.labels import EMOTION_LABELS


def analyze_emotional_state(
    emotion_scores,
    intensity_result,
    sentiment_result
):
    """
    Analyze the user's overall emotional state.

    Surprise is treated as context-dependent:
        Surprise + Joy      -> Positive
        Surprise + Negative -> Negative
        Surprise alone      -> Ambiguous

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

    # ---------------------------------------------------------
    # 1. Detect emotions that are strong enough to be present
    # ---------------------------------------------------------

    detected_emotions = {
        emotion: score
        for emotion, score in emotion_scores.items()
        if score >= 0.50
    }

    # ---------------------------------------------------------
    # 2. Identify secondary emotions
    # ---------------------------------------------------------

    secondary_emotions = {
        emotion: score
        for emotion, score in detected_emotions.items()
        if emotion != dominant_emotion
    }

    # ---------------------------------------------------------
    # 3. Define emotional groups
    # ---------------------------------------------------------

    positive_emotions = {"joy"}

    negative_emotions = {
        "sadness",
        "anger",
        "fear",
        "disgust"
    }

    surprise_emotion = "surprise"

    # ---------------------------------------------------------
    # 4. Calculate strongest positive / negative evidence
    # ---------------------------------------------------------

    positive_score = max(
        [emotion_scores[e] for e in positive_emotions],
        default=0
    )

    negative_score = max(
        [emotion_scores[e] for e in negative_emotions],
        default=0
    )

    surprise_score = emotion_scores.get(
        surprise_emotion,
        0
    )

    # ---------------------------------------------------------
    # 5. Determine emotional polarity
    # ---------------------------------------------------------

    positive_present = positive_score >= 0.50
    negative_present = negative_score >= 0.50
    surprise_present = surprise_score >= 0.50

    # Both positive and negative emotions are strong.
    # Surprise does not change this.
    if positive_present and negative_present:
        polarity = "Mixed"

    # Positive emotion, optionally accompanied by surprise.
    elif positive_present:
        polarity = "Positive"

    # Negative emotion, optionally accompanied by surprise.
    elif negative_present:
        polarity = "Negative"

    # Surprise without a positive or negative emotion.
    elif surprise_present:
        sentiment = sentiment_result.get("sentiment", "").lower()

        if sentiment == "positive":
            polarity = "Positive"
        elif sentiment == "negative":
            polarity = "Negative"
        else:
            polarity = "Ambiguous"
    else:
        polarity = "Neutral"

    # ---------------------------------------------------------
    # 6. Determine whether the emotional state is mixed
    # ---------------------------------------------------------

    # Surprise + Joy is NOT mixed.
    # Surprise + Fear is NOT mixed.
    # Mixed means genuine positive + negative emotion together.
    is_mixed = (
        positive_present
        and negative_present
    )

    # ---------------------------------------------------------
    # 7. Generate human-readable emotional state
    # ---------------------------------------------------------

    if polarity == "Positive":
        emotional_state = "Positive emotional state"

    elif polarity == "Negative":
        emotional_state = "Negative emotional state"

    elif polarity == "Mixed":
        emotional_state = "Mixed emotional state"

    elif polarity == "Ambiguous":
        emotional_state = "Ambiguous emotional state"

    else:
        emotional_state = "Neutral emotional state"

    # ---------------------------------------------------------
    # 8. Return complete result
    # ---------------------------------------------------------

    return {
        "dominant_emotion": dominant_emotion,
        "secondary_emotions": secondary_emotions,
        "is_mixed": is_mixed,
        "polarity": polarity,
        "emotional_state": emotional_state,
        "intensity": intensity,
        "severity": severity
    }